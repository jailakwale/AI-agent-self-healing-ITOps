import os, json, time

class MockTicketingClient:
    def __init__(self, outdir: str = "./runtime/tickets"):
        self.outdir = outdir
        os.makedirs(self.outdir, exist_ok=True)
    def create_ticket(self, title: str, body: str) -> str:
        tid = f"TCK-{int(time.time())}"
        with open(os.path.join(self.outdir, f"{tid}.json"), "w") as f:
            json.dump({"title": title, "body": body}, f, indent=2)
        return tid
