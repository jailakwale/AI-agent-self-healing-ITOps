from typing import Dict, Any

class MockKubernetesClient:
    def __init__(self):
        # maintain simple in-memory state
        self.deployments = {"web-api": {"version":"v2.3.1","pods":3,"status":"Degraded"}}

    def restart_pod(self, service: str) -> Dict[str, Any]:
        self.deployments.setdefault(service, {"version":"v1.0.0","pods":1,"status":"Healthy"})
        self.deployments[service]["status"] = "Restarted"
        return {"service": service, "result":"restarted"}

    def rollback_deploy(self, service: str, target_version: str = "v2.3.0") -> Dict[str, Any]:
        self.deployments.setdefault(service, {"version":"v1.0.0","pods":1,"status":"Healthy"})
        self.deployments[service]["version"] = target_version
        self.deployments[service]["status"] = "RolledBack"
        return {"service": service, "result":"rolled_back", "version": target_version}

# Placeholder for real client via Kubernetes Python SDK
class KubernetesClient:
    def __init__(self, kubeconfig: str = None, namespace: str = "default"):
        self.namespace = namespace
    def restart_pod(self, service: str) -> Dict[str, Any]:
        raise NotImplementedError("Real Kubernetes integration not configured")
    def rollback_deploy(self, service: str, target_version: str) -> Dict[str, Any]:
        raise NotImplementedError("Real Kubernetes integration not configured")
