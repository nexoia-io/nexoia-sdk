import types


def test_gemini_generate_text_calls_generate_content(monkeypatch):
    from nexoia.clients.gemini_client import GeminiClient

    class FakeResponse:
        def __init__(self, text):
            self.text = text

    class FakeModels:
        def __init__(self):
            self.calls = []

        def generate_content(self, model, contents, **kwargs):
            self.calls.append({"model": model, "contents": contents, "kwargs": kwargs})
            return FakeResponse("OK_FROM_GEMINI")

    class FakeGenAIClient:
        def __init__(self, api_key=None):
            self.api_key = api_key
            self.models = FakeModels()

    import nexoia.clients.gemini_client as gemini_client_module

    monkeypatch.setattr(
        gemini_client_module,
        "genai",
        types.SimpleNamespace(Client=FakeGenAIClient),
        raising=True,
    )

    # ✅ FIX: provide a dummy key to satisfy BaseLLMClient
    c = GeminiClient(api_key="DUMMY_KEY")

    out = c.generate_text("hello", model="gemini-1.5-pro")

    assert out == "OK_FROM_GEMINI"
    assert c._client.api_key == "DUMMY_KEY"
    assert c._client.models.calls == [
        {"model": "gemini-1.5-pro", "contents": "hello", "kwargs": {}}
    ]
