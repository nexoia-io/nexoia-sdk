<!-- Badges (add your own) -->
<p align="center">
  <!-- example: <img src="https://img.shields.io/badge/build-passing-brightgreen"> -->
</p>

<h1 align="center">NexoIA SDK 🚀</h1>
<p align="center">
  Unifying multiple AI model APIs (OpenAI, DeepSeek & more) under one simple, pluggable interface.<br>
  <em>Open-source • Developer-first • Built for orchestration</em>
</p>



## ✨ Why NexoIA SDK?
```
| Pain | How NexoIA helps |
|------|------------------|
| **Different vendors, different SDKs** | Use **one** Pythonic interface for all. |
| **Credentials scattered** | Centralised secrets & auth (env, vault, YAML). |
| **Vendor lock-in worries** | Swap providers on the fly; route by cost, latency or accuracy. |
| **Need fast onboarding for teammates** | Consistent patterns & docs, zero cognitive overhead. |

```

## 📂 Package layout
```text
ai_models/
├── base_model.py # Abstract base class every provider inherits
├── openia.py # OpenAI wrapper
├── deepseek.py # DeepSeek wrapper
└── ... # Your next provider :)
nexoia/
└── client.py # High-level orchestration + routing logic
examples/
tests/

```


---

## ⚡ Quick start

```bash
# 1. Install (editable mode while hacking)
git clone https://github.com/nexoia-io/nexoia-sdk.git
cd nexoia-sdk
pip install -e .

# 2. Set credentials (env vars or ~/.config/nexoia.yml)
export OPENAI_API_KEY="sk-..."
export DEEPSEEK_API_KEY="ds-..."

# 3. Call any provider with the same API
python - <<'PY'
from nexoia import Client

client = Client(default="openai:gpt-3.5-turbo")

answer = client.chat("Summarise the last flight of Voyager 1 in two sentences.")
print(answer.text)
PY

