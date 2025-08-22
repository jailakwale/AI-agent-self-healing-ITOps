from agents.analysis_agent import AnalysisAgent
from core.state import IncidentData

def test_analysis_rules_service_down():
    thresholds = {"error_rate_threshold":0.05, "latency_threshold_ms":800}
    agent = AnalysisAgent(thresholds)
    inc = IncidentData(service="web-api", error_rate=0.01, latency_ms=200, pod_status="CrashLoopBackOff")
    plan = agent.classify(inc)
    assert plan.incident_type == "SERVICE_DOWN"
    assert plan.recommended_action == "restart_pod"
