import random
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class MockPrometheusClient:
    seed: int = 42
    def query_service_metrics(self, service: str) -> Dict[str, Any]:
        random.seed(self.seed)
        # Simulate occasional incident
        roll = random.random()
        if roll < 0.33:
            return {"error_rate": 0.12, "latency_ms": 1200, "pod_status": "CrashLoopBackOff"}
        elif roll < 0.66:
            return {"error_rate": 0.07, "latency_ms": 900, "pod_status": "NotReady"}
        else:
            return {"error_rate": 0.01, "latency_ms": 220, "pod_status": "Healthy"}

# Placeholder for real client
class PrometheusClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
    def query_service_metrics(self, service: str) -> Dict[str, Any]:
        # TODO: Implement real Prometheus /api/v1/query_range calls
        raise NotImplementedError("Real Prometheus integration not configured")
