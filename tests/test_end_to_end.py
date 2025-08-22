from main import build_app, load_settings

def test_e2e_runs():
    cfg = load_settings()
    app = build_app(cfg)
    res = app.run(service="web-api")
    assert "history" in res
    assert any("monitor" in h for h in res["history"])
    assert any("analysis" in h for h in res["history"])
    assert any("recovery" in h for h in res["history"])
    assert any("validation" in h for h in res["history"])
