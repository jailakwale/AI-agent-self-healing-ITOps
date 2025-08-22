from pydantic import BaseModel, Field
from typing import Literal, Optional

class AnalysisSchema(BaseModel):
    incident_type: Literal["NONE","DEGRADED","SERVICE_DOWN"]
    recommended_action: Optional[Literal["restart_pod","rollback_deploy","none"]] = "none"
    rationale: str = Field(..., min_length=5)
    confidence: float = Field(..., ge=0.0, le=1.0)
