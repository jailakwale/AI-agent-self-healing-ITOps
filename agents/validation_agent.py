from core.state import IncidentData, ValidationReport
from integrations.monitoring_prometheus import MockPrometheusClient
from core.utils.logger import logger

class ValidationAgent:
    def __init__(self, thresholds: dict, prometheus=None):
        self.thresholds = thresholds
        self.prom = prometheus or MockPrometheusClient(seed=99)  # different seed post-fix

    def validate(self, service: str, before: IncidentData, attempts: int = 1) -> ValidationReport:
        metrics = self.prom.query_service_metrics(service)
        passed = (metrics["error_rate"] < self.thresholds.get("error_rate_threshold", 0.05) and
                  metrics["latency_ms"] < self.thresholds.get("latency_threshold_ms", 800) and
                  metrics["pod_status"] == "Healthy")
        rep = ValidationReport(
            passed=passed,
            post_error_rate=metrics["error_rate"],
            post_latency_ms=metrics["latency_ms"],
            notes="Validation after remediation",
            attempts=attempts
        )
        logger.info(f"[Validation] {service} metrics post-fix: {metrics} -> passed={passed}\n")
        return rep
