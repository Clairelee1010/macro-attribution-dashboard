import csv, io, requests
from datetime import datetime, timezone
from .base_adapter import BaseAdapter,safe_number

class FredAdapter(BaseAdapter):
    def fetch(self,metric_id):
        if metric_id!="US10Y": raise KeyError(metric_id)
        def op():
            r=requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10",timeout=15); r.raise_for_status()
            rows=[]
            for x in csv.DictReader(io.StringIO(r.text)):
                v=safe_number(x.get("DGS10"))
                if v is not None: rows.append((x["DATE"],v))
            if not rows: raise ValueError("No FRED observations")
            date,current=rows[-1]; previous=rows[-2][1] if len(rows)>1 else None
            obs=datetime.strptime(date,"%Y-%m-%d").replace(tzinfo=timezone.utc)
            age=(datetime.now(timezone.utc)-obs).total_seconds()/86400
            ch=round((current-previous)/previous*100,2) if previous not in (None,0) else None
            return self.result("US10Y","US 10-Year Treasury Yield","MACRO","%","FRED / Federal Reserve Board H.15","PRIMARY","DGS10",current,previous,ch,obs.isoformat(),"FRESH" if age<=5 else "STALE")
        return self.retry(op)
