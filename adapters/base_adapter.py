import math, time
from abc import ABC, abstractmethod
from datetime import datetime, timezone

VALID_STATUSES={"FRESH","STALE","MISSING","ERROR"}
def now(): return datetime.now(timezone.utc).isoformat()
def safe_number(v):
    try:
        n=float(v)
        return None if math.isnan(n) or math.isinf(n) else round(n,4)
    except (TypeError,ValueError): return None

class BaseAdapter(ABC):
    def __init__(self,retries=2,retry_delay_seconds=1):
        self.retries=retries; self.retry_delay_seconds=retry_delay_seconds
    def retry(self,fn):
        err=None
        for i in range(self.retries+1):
            try: return fn()
            except Exception as e:
                err=e
                if i<self.retries: time.sleep(self.retry_delay_seconds*(i+1))
        raise err
    @staticmethod
    def result(metric_id,name,category,unit,source,source_type,ticker=None,value=None,previous_close=None,change_pct=None,observed_at=None,status="ERROR",error=None):
        if status not in VALID_STATUSES: raise ValueError(status)
        return {"metric_id":metric_id,"name":name,"category":category,"ticker":ticker,"value":value,"previous_close":previous_close,"change_pct":change_pct,"unit":unit,"source":source,"source_type":source_type,"observed_at":observed_at,"fetched_at":now(),"status":status,"error":error}
    @abstractmethod
    def fetch(self,metric_id): ...
