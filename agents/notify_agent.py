from core.state import IncidentData, ActionPlan, ExecutionResult, ValidationReport
from integrations.slack_client import MockSlackClient
from integrations.ticketing_client import MockTicketingClient

class NotifyAgent:
    def __init__(self, channel: str = "#ops-alerts", slack=None, ticket=None):
        self.slack = slack or MockSlackClient(channel=channel)
        self.ticket = ticket or MockTicketingClient()

    def notify(self, incident: IncidentData, plan: ActionPlan, result: ExecutionResult, validation: ValidationReport):
        title = f"[Self-Heal] {incident.service} - {plan.incident_type}"
        body = (
            f"Incident: {incident.model_dump()}\n"
            f"Plan: {plan.model_dump()}\n"
            f"Execution: {result.model_dump()}\n"
            f"Validation: {validation.model_dump()}\n"
        )
        self.slack.post(f"{title}\nValidation passed: {validation.passed}")
        if not validation.passed:
            tid = self.ticket.create_ticket(title, body)
            self.slack.post(f"Escalated to human. Ticket: {tid}", level="warn")
