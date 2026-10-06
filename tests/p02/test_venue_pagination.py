import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(name):
 p=ROOT/"p02"/"adapters"/f"{name}_adapter.py"; s=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
class Resp:
 def __init__(self,p): self.p=p
 def raise_for_status(self): pass
 def json(self): return self.p
def test_polymarket_pagination(monkeypatch):
 m=load("polymarket"); calls=[]
 def get(url,params,headers,timeout):
  calls.append(dict(params)); return Resp({"markets":[{"id":str(len(calls))}],"next_cursor":"abc" if len(calls)==1 else None})
 monkeypatch.setattr(m.requests,"get",get); rows=m.fetch_active_markets(150)
 assert len(rows)==2 and calls[1]["next_cursor"]=="abc"
def test_kalshi_pagination(monkeypatch):
 m=load("kalshi"); calls=[]
 def get(url,params,headers,timeout):
  calls.append(dict(params)); return Resp({"markets":[{"ticker":str(len(calls))}],"cursor":"next" if len(calls)==1 else ""})
 monkeypatch.setattr(m.requests,"get",get); rows=m.fetch_open_markets(1500)
 assert len(rows)==2 and calls[1]["cursor"]=="next"
