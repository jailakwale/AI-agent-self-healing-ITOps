from core.state import IncidentData, ActionPlan
from core.schemas import AnalysisSchema
from core.utils.logger import logger

class AnalysisAgent:
    def __init__(self, thresholds: dict, provider: str = "mock"):
        self.thresholds = thresholds
        self.provider = provider  # 'mock' or 'openai' (future)

    def classify(self, incident: IncidentData) -> ActionPlan:
        # Rule-based (deterministic) analysis for demo; can be replaced by LLM with AnalysisSchema
        er_t = self.thresholds.get("error_rate_threshold", 0.05)
        lt_t = self.thresholds.get("latency_threshold_ms", 800)

        if incident.pod_status == "CrashLoopBackOff":
            plan = ActionPlan(incident_type="SERVICE_DOWN", recommended_action="restart_pod",
                              rationale="Pod in CrashLoopBackOff", confidence=0.95)
        elif incident.error_rate >= er_t or incident.latency_ms >= lt_t:
            plan = ActionPlan(incident_type="DEGRADED", recommended_action="restart_pod",
                              rationale="Elevated error/latency thresholds exceeded", confidence=0.8)
        else:
            plan = ActionPlan(incident_type="NONE", recommended_action="none",
                              rationale="Within thresholds", confidence=0.9)

        # Structured validation
        AnalysisSchema(**plan.model_dump())
        logger.info(f"[Analysis] Classified incident: {plan.model_dump()}\n")
        return plan
