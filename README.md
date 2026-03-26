<!-- Badges (add your own) -->
<p align="center">
  <!-- example: <img src="https://img.shields.io/badge/build-passing-brightgreen"> -->
</p>

<h1 align="center">NexoIA SDK 🚀</h1>
<p align="center">
  A unified SDK for orchestrating multiple LLM providers with a consistent interface.
</p>
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
    └── deepseek_client.py # DeepSeek wrapper
    └── openai_client.py # OpenAI wrapper 
    └── claude_client.py # Claude wrapper
    └── gemini_client.py # Gemini wrapper
└── compat/
    └── openai.py
    └── deepseek.py
    └── claude.py
    └── gemini.py
└── config.py
└── exceptions.py
└── patcher.py
└── registry.py
└── types.py
tests/
└── test_claude_client.py
└── test_compat_claude.py
└── test_config.py
└── test_deepseek_client.py
└── test_exception.py
└── test_gemini_client.py
└── test_openai_client.py
└── test_patcher.py
└── test_registry.py
└── test_types.py
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
from nexoia.clients.openai_client import OpenAIClient

client = OpenAIClient(api_key="...")

resp = client.generate("Summarise the last flight of Voyager 1 in two sentences.")
print(resp.text)
PY
```
---

## ✨ Unified Response Model (LLMResponse)

NexoIA standardizes responses across all providers using a single interface.

Instead of returning plain text, all clients now return a structured object:

```python
from nexoia.clients.openai_client import OpenAIClient

client = OpenAIClient(api_key="...")

resp = client.generate("Hello world", model="gpt-3.5-turbo")

print(resp.text)        # Generated text
print(resp.provider)    # openai, anthropic, gemini, deepseek
print(resp.model)       # Model used
print(resp.usage)       # Token usage (if available)
print(resp.raw)         # Raw provider response
```

## 🔌 Add a new provider in 3 files

1. **clients/clients.py** – subclass `BaseModel`, implement `.chat()` / `.complete()`.
2. **nexoia/providers.yml** – register the provider (or use `entry_points`).
3. **tests/test_mycoolapi.py** – add a minimal pytest ensuring the wrapper works.

Submit a pull request—boom, the community benefits!

---

## 🛠️ Roadmap

### 🔹 Core Platform

- [x] Unified response model (`LLMResponse`)
- [ ] Streaming support across providers
- [ ] Async client support
- [ ] Standardized tool/function calling

---

### 🔹 Orchestration

- [ ] Multi-provider routing (latency, cost, fallback)
- [ ] Model selection strategies
- [ ] Consensus / multi-model voting

---

### 🔹 Observability & Cost

- [ ] Built-in cost tracker (based on `usage`)
- [ ] Token usage analytics
- [ ] Request tracing & logging

---

### 🔹 Developer Experience

- [ ] CLI: `nexoia chat "hello world"`
- [ ] TypeScript client
- [ ] Improved config system (profiles, environments)

---

### 🔹 Runtime & Edge

- [ ] WebAssembly runtime for in-browser inference
- [ ] Edge-compatible execution

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
## 🔑 Provider Identification (`PROVIDER_SLUG`)

Each LLM client in **NexoIA SDK** defines a stable provider identifier using the `PROVIDER_SLUG` attribute.

### What is `PROVIDER_SLUG`?

`PROVIDER_SLUG` is a **human-readable, stable identifier** for a provider (e.g. `openai`, `anthropic`, `gemini`).

It is used to:
- Resolve API keys from configuration files
- Enable clean provider routing and registries
- Decouple configuration from internal class names

### Why not use the class name?

Relying on `ClassName.lower()` (for example `geminiclient`) introduces several problems:
- Configuration keys become unintuitive and error-prone
- Renaming a class breaks existing configurations
- Provider routing logic becomes brittle

Using `PROVIDER_SLUG` avoids these issues entirely.

### Example

```python
class GeminiClient(BaseLLMClient):
    PROVIDER_SLUG = "gemini"
    ENV_API_KEY = "GEMINI_API_KEY"
```
---
## 🔌 Client Lifecycle and Resource Management (`close()`)

Some providers (such as **DeepSeek** and **Anthropic**) use `httpx.Client` internally, which maintains open network connections.

To prevent connection leaks in long-running processes, NexoIA defines a standard lifecycle API for all clients.

---

### `close()`

All clients expose a `close()` method.

- In `BaseLLMClient`, `close()` is a **no-op**
- Clients that manage network or system resources **must override it**

#### Example

```python
class DeepSeekClient(BaseLLMClient):
    def close(self) -> None:
        self._client.close()
```
### Context Manager Support

All clients support usage as a context manager:

```python
with DeepSeekClient(api_key="...") as client:
    text = client.generate_text("Hello", model="deepseek-chat")
```
When exiting the with block:

+ close() is automatically called

Network connections are released safely
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
