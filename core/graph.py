from typing import Dict, Any
from langgraph.graph import StateGraph, END
from core.state import SupervisorState
from core.utils.logger import logger

class SupervisorGraph:
    def __init__(self, monitor, analysis, recovery, validation, notifier, thresholds, max_attempts: int = 2):
        self.monitor = monitor
        self.analysis = analysis
        self.recovery = recovery
        self.validation = validation
        self.notifier = notifier
        self.thresholds = thresholds
        self.max_attempts = max_attempts

        self.graph = StateGraph(SupervisorState)

        self.graph.add_node("monitor", self._monitor_node)
        self.graph.add_node("analyze", self._analysis_node)
        self.graph.add_node("recover", self._recovery_node)
        self.graph.add_node("validate", self._validate_node)
        self.graph.add_node("notify", self._notify_node)

        self.graph.set_entry_point("monitor")
        self.graph.add_edge("monitor", "analyze")
        self.graph.add_edge("analyze", "recover")
        self.graph.add_edge("recover", "validate")
        self.graph.add_edge("validate", "notify")
        self.graph.add_edge("notify", END)

        self.app = self.graph.compile()

    def _monitor_node(self, state: SupervisorState) -> SupervisorState:
        inc = self.monitor.run(state.incident.service if state.incident else "web-api")
        state.incident = inc
        state.history.append({"monitor": inc.model_dump()})
        return state

    def _analysis_node(self, state: SupervisorState) -> SupervisorState:
        plan = self.analysis.classify(state.incident)
        state.plan = plan
        state.history.append({"analysis": plan.model_dump()})
        return state

    def _recovery_node(self, state: SupervisorState) -> SupervisorState:
        res = self.recovery.execute(state.incident.service, state.plan)
        state.exec_result = res
        state.history.append({"recovery": res.model_dump()})
        return state

    def _validate_node(self, state: SupervisorState) -> SupervisorState:
        attempts = 1
        rep = self.validation.validate(state.incident.service, state.incident, attempts=attempts)
        # Retry once if failed and we took an action
        while not rep.passed and attempts < self.max_attempts:
            attempts += 1
            rep = self.validation.validate(state.incident.service, state.incident, attempts=attempts)
        state.validation = rep
        state.history.append({"validation": rep.model_dump()})
        return state

    def _notify_node(self, state: SupervisorState) -> SupervisorState:
        self.notifier.notify(state.incident, state.plan, state.exec_result, state.validation)
        state.history.append({"notify": {"done": True}})
        logger.info("[Supervisor] Flow complete.\n")
        return state

    def run(self, service: str = "web-api") -> Dict[str, Any]:
        # Provide all required fields for IncidentData
        initial = SupervisorState(incident={
            "service": service,
            "error_rate": 0.0,
            "latency_ms": 0.0,
            "pod_status": "Healthy",
            "details": {}
        })
        logger.info("[Supervisor] Starting run for service: %s", service)
        final = self.app.invoke(initial)
        return final
