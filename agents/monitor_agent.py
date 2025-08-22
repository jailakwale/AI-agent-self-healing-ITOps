from core.state import IncidentData
from integrations.monitoring_prometheus import MockPrometheusClient
from core.utils.logger import logger

class MonitorAgent:
    def __init__(self, thresholds: dict, prometheus=None):
        self.thresholds = thresholds
        self.prom = prometheus or MockPrometheusClient()

    def run(self, service: str) -> IncidentData:
        metrics = self.prom.query_service_metrics(service)
        incident = IncidentData(
            service=service,
            error_rate=metrics["error_rate"],
            latency_ms=metrics["latency_ms"],
            pod_status=metrics["pod_status"],
            details={"raw": metrics}
        )
        logger.info(f"[Monitor] {service} metrics: {metrics}\n")
        return incident
