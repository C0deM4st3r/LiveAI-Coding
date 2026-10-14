"""Read-only bounded queue projection; importing never creates/migrates a DB."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3
if __package__:
    from .managed_goals import GOAL_DB
else:
    from managed_goals import GOAL_DB

def snapshot(path=GOAL_DB):
    empty={'available':False,'requests':[],'counts':{}}
    if not Path(path).is_file():return empty
    try:
        with closing(sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True,timeout=.2)) as db:
            db.row_factory=sqlite3.Row;db.execute('PRAGMA query_only=ON');db.execute('BEGIN')
            tables={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not {'gq_schema','gq_requests'}<=tables:return empty
            version=db.execute('SELECT version FROM gq_schema WHERE id=1').fetchone()
            if not version or version[0]!=1:return empty
            rows=db.execute("""SELECT id,goal_id,text,state,plan,origin,reason,created,updated,
                CASE WHEN owner IS NOT NULL AND state IN ('translating','ready','running') THEN 1 ELSE 0 END AS owned FROM gq_requests
                WHERE state NOT IN ('completed','cancelled') ORDER BY seq LIMIT 20""").fetchall()
            requests=[]
            for row in rows:
                item=dict(row);item['plan']=json.loads(item['plan']) if item['plan'] else None
                requests.append(item)
            return {'available':True,'requests':requests,'counts':dict(db.execute('SELECT state,COUNT(*) FROM gq_requests GROUP BY state'))}
    except (sqlite3.Error,ValueError,OSError):return empty
