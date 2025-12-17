<!-- Badges (add your own) -->
<p align="center">
  <!-- example: <img src="https://img.shields.io/badge/build-passing-brightgreen"> -->
</p>

<h1 align="center">NexoIA SDK 🚀</h1>
<p align="center">
  Unifying multiple AI model APIs (OpenAI, DeepSeek & more) under one simple, pluggable interface.<br>
  <em>Open-source • Developer-first • Built for orchestration</em>
  <strong>Founder by <a href="https://www.linkedin.com/in/jonathan-parra-935b09133/">Jonathan Parra</a></strong>
</p>


---
## ✨ Why NexoIA SDK?

| Pain | How NexoIA helps |
|------|------------------|
| **Different vendors, different SDKs** | Use **one** Pythonic interface for all. |
| **Credentials scattered** | Centralised secrets & auth (env, vault, YAML). |
| **Vendor lock-in worries** | Swap providers on the fly; route by cost, latency or accuracy. |
| **Need fast onboarding for teammates** | Consistent patterns & docs, zero cognitive overhead. |

---

## 📂 Package layout
```text
nexoia/
└── clients/ # High-level orchestration + routing logic
    └── base.py # Abstract base class every provider inherits
    └── deepseek_client.py # OpenAI wrapper
    └── openai_client.py # DeepSeek wrapper
    └── claude_client.py # Claude wrapper
    └── gemini_client.py # Claude wrapper
└── compat/
    └── openai.py
    └── deepseek.py
    └── claude.py
    └── gemini.py
└── config.py
└── exceptions.py
└── patcher.py
└── registry.py
tests/
└── test_config.py
└── test_deepseek_client.py
└── test_exception.py
└── test_openai_client.py
└── test_patcher.py
└── test_registry.py
examples/

```


---

## ⚡ Quick start

```bash
# 1. Install
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
```

## 🔌 Add a new provider in 3 files

1. **clients/clients.py** – subclass `BaseModel`, implement `.chat()` / `.complete()`.
2. **nexoia/providers.yml** – register the provider (or use `entry_points`).
3. **tests/test_mycoolapi.py** – add a minimal pytest ensuring the wrapper works.

Submit a pull request—boom, the community benefits!

---

## 🛠️ Roadmap

- WebAssembly runtime for in-browser inference  
- TypeScript client  
- Built-in cost tracker & billing reports  
- CLI: `nexoia chat "hello world"`

> Vote or propose new items on the **Issues** tab!

---

## 🤝 Contributing

We love pull requests and new issues:

```bash
# Fork the repo & create your branch
git checkout -b feat/my-feature

# Write tests (pytest) & run linters
pre-commit run --all-files
```
---

## 🧪 Testing

NexoIA includes an automated test suite designed to validate:

- Correct integration of each provider (OpenAI, Claude, Gemini, etc.)
- Compliance with the contract defined by `BaseLLMClient`
- Proper behavior of the compatibility layer (`nexoia.compat.*`)
- Correct request routing without performing real external API calls

⚠️ **Tests do not perform real requests to external providers.**  
All external dependencies are fully mocked to ensure:

- Fast execution
- Deterministic and reproducible results
- No dependency on real credentials or network access

---

### Running the tests

Install the project in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```
For a concise output:
```bash
pytest -q
```

---

## 💬 Community

- **Page**: [@nexoia_io](https://nexoia.cl)
- **Discord**: *coming soon*  
- **X/Twitter**: [@nexoia_io](https://twitter.com/nexoia_io)
- **YouTube**: [@nexoia_io](https://www.youtube.com/@NexoIA-io)   
- **GitHub Discussions**: start a topic if you’re stuck or have an idea.

---

## ⚖️ License

Apache&nbsp;2.0 — free for personal & commercial use.  
Copyright © 2025 **NexoIA**

> *“AI for everyone, powered by everyone.”* ✨


