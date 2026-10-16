from adapters.fred_adapter import FredAdapter

def test_fred_accepts_current_and_legacy_date_headers(monkeypatch):
    import adapters.fred_adapter as mod
    class Response:
        def __init__(self, text): self.text=text
        def raise_for_status(self): pass
    for header in ['DATE','observation_date','date']:
        monkeypatch.setattr(mod.requests,'get',lambda *a, **k: Response(f'{header},DGS10\n2026-10-13,4.00\n2026-10-14,4.10\n'))
        result=FredAdapter().fetch('US10Y')
        assert result['value']==4.10
        assert result['observed_at'].startswith('2026-10-14')
