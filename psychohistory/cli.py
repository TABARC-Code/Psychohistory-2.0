import argparse,json
from datetime import datetime,timezone
from .core.store import Store
from .pipeline import evaluate

def dt(s):
    x=datetime.fromisoformat(s.replace('Z','+00:00')); return x if x.tzinfo else x.replace(tzinfo=timezone.utc)
def main():
    p=argparse.ArgumentParser(prog='psychohistory'); p.add_argument('--db',default='registry/psychohistory.db'); sub=p.add_subparsers(dest='cmd',required=True)
    e=sub.add_parser('evaluate'); e.add_argument('--as-of',required=True)
    a=p.parse_args(); store=Store(a.db)
    if a.cmd=='evaluate': print(json.dumps(evaluate(store,dt(a.as_of)),indent=2))
if __name__=='__main__':main()
