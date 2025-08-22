from typing import Optional

class MockSlackClient:
    def __init__(self, channel: str = "#ops-alerts"):
        self.channel = channel
    def post(self, message: str, level: str = "info"):
        print(f"[SLACK:{self.channel}][{level.upper()}] {message}")

# Placeholder for real Slack client (slack_sdk)
class SlackClient:
    def __init__(self, bot_token: str, channel: str):
        from slack_sdk import WebClient
        self.client = WebClient(token=bot_token)
        self.channel = channel
    def post(self, message: str, level: str = "info"):
        self.client.chat_postMessage(channel=self.channel, text=f"[{level.upper()}] {message}")
