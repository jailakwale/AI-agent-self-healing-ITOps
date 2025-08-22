from typing import Dict, Any
from core.state import ActionPlan, ExecutionResult
from integrations.k8s_client import MockKubernetesClient
from core.utils.logger import logger

class RecoveryAgent:
    def __init__(self, allowed: list, dry_run: bool = True, k8s=None):
        self.allowed = set(allowed)
        self.dry_run = dry_run
        self.k8s = k8s or MockKubernetesClient()

    def execute(self, service: str, plan: ActionPlan) -> ExecutionResult:
        action = plan.recommended_action or "none"
        if action not in self.allowed:
            return ExecutionResult(action=action, success=False, message="Action not allowed")

        if self.dry_run:
            logger.info(f"[Recovery][DRY-RUN] Would perform {action} on {service}\n")
            return ExecutionResult(action=action, success=True, message="Dry-run success")

        if action == "restart_pod":
            res = self.k8s.restart_pod(service)
            return ExecutionResult(action=action, success=True, message="Pod restarted", data=res)
        elif action == "rollback_deploy":
            res = self.k8s.rollback_deploy(service)
            return ExecutionResult(action=action, success=True, message="Deployment rolled back", data=res)
        else:
            return ExecutionResult(action=action, success=False, message="No action taken")
