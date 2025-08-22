import yaml
from core.graph import SupervisorGraph
from agents.monitor_agent import MonitorAgent
from agents.analysis_agent import AnalysisAgent
from agents.recovery_agent import RecoveryAgent
from agents.validation_agent import ValidationAgent
from agents.notify_agent import NotifyAgent

def load_settings():
    with open("config/settings.yaml") as f:
        return yaml.safe_load(f)

def build_app(cfg):
    thresholds = {
        "error_rate_threshold": cfg["routing"]["error_rate_threshold"],
        "latency_threshold_ms": cfg["routing"]["latency_threshold_ms"],
    }
    monitor = MonitorAgent(thresholds)
    analysis = AnalysisAgent(thresholds, provider=cfg["llm"]["provider"])
    recovery = RecoveryAgent(cfg["recovery"]["allowed_actions"], dry_run=cfg.get("dry_run", True))
    validation = ValidationAgent(thresholds)
    notifier = NotifyAgent(channel=cfg["notify"]["slack_channel"])
    return SupervisorGraph(monitor, analysis, recovery, validation, notifier, thresholds, max_attempts=cfg["routing"]["max_attempts"])

if __name__ == "__main__":
    cfg = load_settings()
    app = build_app(cfg)
    result = app.run(service="web-api")
    print("\n=== FINAL STATE ===")
    print(result)
