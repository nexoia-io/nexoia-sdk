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

    c = GeminiClient()
    text = c.generate_text(prompt="Hola", model="gemini-2.5-flash", temperature=0.2)

    assert text == "OK_FROM_GEMINI"
