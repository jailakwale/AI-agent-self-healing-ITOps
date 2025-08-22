# Enterprise Self-Healing ITOps Agent (LangGraph)

A **fully runnable**, educational, enterprise-style project that demonstrates a **self-healing ITOps agent** built with **LangGraph**. It simulates a high-value scenario: **web service degradation/outage** detected via monitoring, analyzed for root cause, **auto-remediated** (restart/rollback), **validated**, and **notified** to Slack — all orchestrated by an **Agent Supervisor** graph with **structured outputs, retries, and memory**.

> Designed with toggles to connect to real AWS/EKS/Prometheus/Slack/Pinecone

---

## 🔥 Why This Project
- **High business impact**: Minimizes downtime (big $$ savings).
- **Agentic patterns**: Supervisor–worker graph, tool use, memory, self-healing, validation, fallbacks.
- **Enterprise integrations**: (Mocked) Prometheus, Kubernetes, AWS, Slack, ticketing; optional Pinecone, LangSmith.
- **Production-readiness**: Modular code, typed contracts, tests, config-driven, extensible.

---

## 🧱 Architecture

**Scenario**: A critical web API service is intermittently failing (5xx spikes / pod crash). The agent:
1. **MonitorAgent**: Pulls metrics (error rate, latency, pod health) from *Prometheus* (mock).  
2. **AnalysisAgent**: Classifies incident (e.g., `SERVICE_DOWN`, `DEGRADED`) and recommends action.  
3. **RecoveryAgent**: Executes remediation (restart pod / rollback deployment) via *Kubernetes* (mock).  
4. **ValidationAgent**: Re-checks metrics to confirm recovery; else escalate.  
5. **NotifyAgent**: Sends Slack updates / opens ticket (mock).  
6. **Supervisor** (LangGraph): Orchestrates the flow, handles retries, fallbacks, and memory updates.

```
+----------------+      +----------------+      +----------------+
| MonitorAgent   | ---> | AnalysisAgent  | ---> | RecoveryAgent  |
+----------------+      +----------------+      +----------------+
        |                       |                        |
        v                       v                        v
   IncidentData           ActionPlan                ExecutionResult
        \______________________|______________________________/
                               v
                        +----------------+      +----------------+
                        | ValidationAgent| ---> | NotifyAgent   |
                        +----------------+      +----------------+
                                   |
                                   v
                               SUPERVISOR (LangGraph)
```

---

## 🧩 Tech Stack

- **LangGraph** for agent orchestration
- **LangChain** + **OpenAI function calling schemas** (or any LLM you prefer)
- **Pydantic** for structured outputs
- **Tenacity** for retries
- **Mock integrations** (Prometheus, Kubernetes, Slack, Ticketing)
- **Vector memory**: local FAISS (default) or **Pinecone** (optional)
- **Observability**: built-in logging; **LangSmith** optional

---

## 🚀 Quickstart (Offline Demo)

1. **Python 3.10+** recommended.
2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the demo scenario (generates a synthetic incident and self-heals it):
   ```bash
   python main.py
   ```
4. Run tests:
   ```bash
   pytest -q
   ```

You’ll see console logs for detection, analysis, remediation (restart), validation, and Slack-style notifications.

---

## 🔧 Configuration

All settings in `config/settings.yaml`:

- **mode**: `mock` or `real` — choose integrations
- **llm.model**: set a local model or OpenAI model (you can run with mock analyzer if no API key)
- **memory.use_pinecone**: toggle Pinecone; fallback is local FAISS
- **routing**: thresholds for error rate/latency to trigger incidents
- **recovery**: actions permitted (`restart_pod`, `rollback_deploy`)

Environment variables (optional):
```
OPENAI_API_KEY=...            # if using real LLM
LANGCHAIN_TRACING_V2=true     # if using LangSmith
LANGCHAIN_API_KEY=...
PINECONE_API_KEY=...
SLACK_BOT_TOKEN=...
```

---

## 📁 Repository Layout

```
enterprise-self-healing-itops-agent/
├─ main.py
├─ requirements.txt
├─ README.md
├─ config/
│  ├─ settings.yaml
├─ core/
│  ├─ graph.py
│  ├─ state.py
│  ├─ schemas.py
│  ├─ memory.py
│  ├─ utils/
│  │  ├─ logger.py
│  │  ├─ retry.py
├─ integrations/
│  ├─ monitoring_prometheus.py
│  ├─ k8s_client.py
│  ├─ slack_client.py
│  ├─ ticketing_client.py
│  ├─ memory_vector.py
├─ agents/
│  ├─ monitor_agent.py
│  ├─ analysis_agent.py
│  ├─ recovery_agent.py
│  ├─ validation_agent.py
│  ├─ notify_agent.py
├─ tests/
│  ├─ test_end_to_end.py
│  ├─ test_analysis_rules.py
│  ├─ test_recovery_paths.py
├─ runtime/
│  ├─ tickets/     # generated at runtime
│  ├─ vector/      # local FAISS index
└─ readme_assets/
   ├─ graph.png    # placeholder
```

---

## 🛡️ Safety & Guardrails

- **Dry-run** mode prevents destructive actions — enabled by default in `settings.yaml`.
- **Policy checks**: `recovery` actions gated by allowlist.
- **Structured outputs** to avoid free-form LLM hallucinations in control paths.
- **Circuit breaker**: Escalates to human if repeated validation fails.

---
