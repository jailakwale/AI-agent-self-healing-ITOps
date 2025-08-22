from typing import Literal, Optional, List, Dict, Any
from pydantic import BaseModel, Field

IncidentType = Literal["NONE","DEGRADED","SERVICE_DOWN"]

class IncidentData(BaseModel):
    service: str
    error_rate: float
    latency_ms: float
    pod_status: str = "Healthy"  # Healthy | CrashLoopBackOff | NotReady
    details: Dict[str, Any] = Field(default_factory=dict)

class ActionPlan(BaseModel):
    incident_type: IncidentType = "NONE"
    recommended_action: Optional[Literal["restart_pod","rollback_deploy","none"]] = "none"
    rationale: str = ""
    confidence: float = 0.0

class ExecutionResult(BaseModel):
    action: str
    success: bool
    message: str = ""
    data: Dict[str, Any] = Field(default_factory=dict)

class ValidationReport(BaseModel):
    passed: bool
    post_error_rate: float
    post_latency_ms: float
    notes: str = ""
    attempts: int = 0

class SupervisorState(BaseModel):
    iteration: int = 0
    incident: Optional[IncidentData] = None
    plan: Optional[ActionPlan] = None
    exec_result: Optional[ExecutionResult] = None
    validation: Optional[ValidationReport] = None
    history: List[Dict[str, Any]] = Field(default_factory=list)
