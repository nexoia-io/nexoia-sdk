def test_config_loader(tmp_path, monkeypatch):
    #Crea un YAML temporal con la API-key
    cfg = tmp_path / "nexoia.yaml"
    cfg.write_text("api_keys:\n  openai: sk-test\n")

    #Indica a la librería que use ese archivo
    monkeypatch.setenv("NEXOIA_CONFIG", str(cfg))

    #Importa y comprueba que la clave se lea bien
    from nexoia.config import get_api_key
    assert get_api_key("openai") == "sk-test"