from nexoia.types import LLMResponse


def test_llm_response_str_returns_text():
    resp = LLMResponse(
        text="hola",
        provider="openai",
        model="gpt-4o-mini",
    )
    assert str(resp) == "hola"