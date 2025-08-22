import os, json, random
from typing import Dict, Any
from integrations.memory_vector import LocalFAISS

class IncidentMemory:
    def __init__(self, path: str = "./runtime/vector"):
        os.makedirs(path, exist_ok=True)
        self.index = LocalFAISS()
        # Prime with a couple of mock incidents
        self.index.add("svc_down", [1.0]*384)
        self.index.add("degraded", [0.5]*384)

    def recall_similar(self, incident: Dict[str, Any]):
        # Use a simple embedding proxy
        vector = [incident.get("error_rate",0)*10] + [0]*383
        return self.index.search(vector, k=3)

    def store(self, incident: Dict[str, Any]):
        vector = [incident.get("error_rate",0)*10] + [0]*383
        self.index.add(f"inc_{random.randint(1000,9999)}", vector)
