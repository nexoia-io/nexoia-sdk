<!-- Badges (add your own) -->
<p align="center">
  <!-- example: <img src="https://img.shields.io/badge/build-passing-brightgreen"> -->
</p>

<h1 align="center">NexoIA SDK 🚀</h1>
<p align="center">
  Unifying multiple AI model APIs (OpenAI, DeepSeek & more) under one simple, pluggable interface.<br>
  <em>Open-source • Developer-first • Built for orchestration</em>
</p>

```

## ✨ Why NexoIA SDK?

| Pain | How NexoIA helps |
|------|------------------|
| **Different vendors, different SDKs** | Use **one** Pythonic interface for all. |
| **Credentials scattered** | Centralised secrets & auth (env, vault, YAML). |
| **Vendor lock-in worries** | Swap providers on the fly; route by cost, latency or accuracy. |
| **Need fast onboarding for teammates** | Consistent patterns & docs, zero cognitive overhead. |

```

## 📂 Package layout

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
