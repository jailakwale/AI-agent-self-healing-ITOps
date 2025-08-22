from agents.recovery_agent import RecoveryAgent
from core.state import ActionPlan

def test_recovery_dry_run_allowed():
    agent = RecoveryAgent(["restart_pod"], dry_run=True)
    plan = ActionPlan(incident_type="DEGRADED", recommended_action="restart_pod", rationale="test", confidence=0.9)
    res = agent.execute("web-api", plan)
    assert res.success
    assert res.action == "restart_pod"

def test_recovery_blocked_action():
    agent = RecoveryAgent(["restart_pod"], dry_run=True)
    plan = ActionPlan(incident_type="DEGRADED", recommended_action="rollback_deploy", rationale="test", confidence=0.9)
    res = agent.execute("web-api", plan)
    assert not res.success
