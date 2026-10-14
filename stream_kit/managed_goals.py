"""Read-only projection of persisted Goal Manager data for viewer panels.

No migrations, admission, completion, controller access or write endpoints.
The optional gameplay package is not required to run the presentation kit.
"""
from contextlib import closing
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from collections import Counter

GOAL_DB = Path(__file__).resolve().parents[1] / 'local' / 'goals' / 'goals.sqlite3'
STATUSES = ('proposed', 'ready', 'active', 'blocked', 'paused', 'completed', 'failed', 'cancelled')


def progress_key(goal):
    target=goal.get('target',{});semantic=target.get('semantic_target',{})
    if goal['type'] in ('leave_bedroom','leave_house') and target.get('context_id') and goal.get('parent_id'):
        # Repeated motor chunks of the same parent intent, never unrelated trips.
        identity={k:v for k,v in target.items() if k not in ('execution_budget','reason','description')}
        return ('motor',goal['type'],goal['parent_id'],goal.get('source'),
                json.dumps(identity,sort_keys=True),json.dumps(goal.get('success_criteria',{}),sort_keys=True))
    if not isinstance(semantic,dict):return None
    if goal['type']!='world_investigation' or not semantic.get('helper_call') or not semantic.get('exploration_quota'):
        return None
    key=(target.get('context_id'),goal.get('parent_id'),goal.get('source'),semantic.get('helper_step'),
         semantic.get('label'),semantic.get('external_outcome'),semantic.get('frontier_direction'))
    return key if all(v is None or isinstance(v,str) for v in key) else None


def compact_progress(goals,totals=None):
    """Viewer grouping only; raw goals, proof records and statuses stay intact."""
    groups={};rows=[]
    parents={g['id']:g for g in goals}
    def superseded(g):
        if g.get('emergency'):return False
        parent=g.get('parent_id');seen={g['id']}
        while parent in parents and parent not in seen:
            seen.add(parent)
            if parents[parent]['status']=='cancelled':return True
            parent=parents[parent].get('parent_id')
        return False
    for g in goals:
        if g['status']=='cancelled' or superseded(g):continue  # Display only; durable history stays intact.
        key=progress_key(g)
        if key is None:rows.append(g);continue
        groups.setdefault(key,[]).append(g)
    for key,members in groups.items():
        ranks={'active':0,'ready':1,'blocked':2,'paused':3,'proposed':4,'failed':5,'completed':6}
        representative=sorted(members,key=lambda g:((0 if g['status']=='active' else 1) if key[0]=='motor' else ranks[g['status']],-datetime.fromisoformat(g['updated_at']).timestamp() if g.get('updated_at') else 0))[0]
        counts=totals.get(key) if totals else None
        counts=counts or Counter(g['status'] for g in members)
        counts={s:n for s,n in counts.items() if s!='cancelled'}
        n=sum(counts.values());semantic=representative['target'].get('semantic_target',{})
        summary=' · '.join(str(counts[s])+' '+s for s in STATUSES if counts.get(s))
        rows.append(representative|{'title':representative['title'] if key[0]=='motor' else 'Explore toward '+str(semantic.get('label','unknown area')),
            'group_count':n,'group_counts':dict(counts),'progress_summary':str(n)+' progress checkpoints · '+summary})
    return rows


def session_cards(goals,root_id,limit=5,ancestry=None):
    """Same bounded projection for stream and operator; no lifecycle changes."""
    ranks={'active':0,'ready':1,'blocked':2,'paused':3,'proposed':4,'failed':5,'completed':6}
    parents={g['id']:g.get('parent_id') for g in (ancestry or goals)}
    def belongs(g):
        current=g['id'];seen=set()
        while current and current not in seen:
            if current==root_id:return True
            seen.add(current);current=parents.get(current)
        return False
    rows=[g for g in goals if g['status']!='cancelled' and
          (not root_id or belongs(g) or g.get('emergency') and g['status'] in ('active','ready','blocked','paused'))]
    def rank(g):
        leading=0 if g.get('emergency') and g['status'] in ('active','ready','blocked','paused') else 1 if g['id']==root_id else 2
        return (leading,ranks[g['status']],-g.get('priority',0),
                -datetime.fromisoformat(g['updated_at']).timestamp() if g.get('updated_at') else 0)
    # Keep active nested work next to the major objective, followed by its
    # dependency-linked next steps. Unrelated historical roots stay in history.
    return [g|{'session_role':'major' if g['id']==root_id else 'emergency' if g.get('emergency') else 'subgoal'}
            for g in sorted(rows,key=rank)[:limit]]


def snapshot(path=GOAL_DB):
    result = {'available': False, 'message': 'No managed goals yet', 'goals': [],
              'current': None, 'counts': {s: 0 for s in STATUSES}, 'total': 0,
              'events': [], 'timestamp': datetime.now(timezone.utc).isoformat()}
    path = Path(path)
    if not path.is_file():
        return result
    try:
        with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True, timeout=.2)) as db:
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA query_only=ON')
            db.execute('BEGIN')  # One consistent committed snapshot, including proofs.
            version = db.execute('SELECT version FROM gm_schema WHERE id=1').fetchone()
            if version is None or version[0] != 2:
                result['message'] = 'Goal database version needs a compatible reader'
                return result
            counts = dict(db.execute('SELECT status,COUNT(*) FROM gm_goals GROUP BY status').fetchall())
            result['counts'].update(counts)
            result['total'] = sum(counts.values())
            rows = db.execute("""SELECT g.*,
                (SELECT COUNT(*) FROM gm_evidence e WHERE e.goal_id=g.id) AS evidence_count
                FROM gm_goals g ORDER BY CASE status
                WHEN 'active' THEN 0 WHEN 'ready' THEN 1 WHEN 'blocked' THEN 2
                WHEN 'paused' THEN 3 WHEN 'proposed' THEN 4 ELSE 5 END,
                emergency DESC,priority DESC,(source='curiosity'),
                CASE WHEN status IN ('blocked','paused','completed','failed','cancelled') THEN -seq ELSE seq END
                LIMIT 200""").fetchall()

            def title(row):
                target = json.loads(row['target'])
                if not isinstance(target, dict):
                    raise ValueError('Invalid stored goal target')
                return str(target.get('title') or target.get('name') or row['type'])

            def project(row):
                dependencies = db.execute("""SELECT g.id,g.type,g.target,g.status FROM gm_dependencies d
                    JOIN gm_goals g ON g.id=d.dependency_id WHERE d.goal_id=? ORDER BY g.seq""", (row['id'],)).fetchall()
                dependency_rows = [{'id': d['id'], 'title': title(d), 'status': d['status']} for d in dependencies]
                blockers = json.loads(row['manual_blockers']) + [
                    'Needs ' + d['title'] + ' (' + d['status'] + ')'
                    for d in dependency_rows if d['status'] != 'completed']
                return {k: row[k] for k in ('id','type','source','priority','status','parent_id','retry_limit',
                                            'attempts','created_at','updated_at','evidence_count')} | {
                    'title': title(row), 'target': json.loads(row['target']), 'emergency': bool(row['emergency']),
                    'dependencies': dependency_rows, 'blockers': blockers,
                    'success_criteria': json.loads(row['success_criteria']),
                    'failure_reasons': json.loads(row['failure_reasons'])}

            result['goals'] = [project(row) for row in rows]
            result['current'] = result['goals'][0] if rows else None
            events = db.execute("""SELECT e.*,g.type,g.target FROM gm_events e
                JOIN gm_goals g ON g.id=e.goal_id ORDER BY e.id DESC LIMIT 12""").fetchall()
            result['events'] = [dict(id=e['id'], goal_id=e['goal_id'], title=title(e), event=e['event'],
                                     timestamp=e['timestamp'], data=json.loads(e['data'])) for e in events]
            tables={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if {'hy_meta','hy_events','hy_inference','hy_facts','hy_schema'}<=tables:
                hy_version=db.execute('SELECT version FROM hy_schema').fetchone()
                if hy_version and hy_version[0]==1:
                    meta={r['key']:json.loads(r['value']) for r in db.execute('SELECT * FROM hy_meta')}
                    # Historical high-priority goals must not crowd the current
                    # context out of the global bounded history projection.
                    current_rows=db.execute("""SELECT g.*,
                        (SELECT COUNT(*) FROM gm_evidence e WHERE e.goal_id=g.id) AS evidence_count
                        FROM gm_goals g WHERE json_extract(target,'$.context_id')=?
                        ORDER BY (id=?) DESC,(status='active') DESC,seq DESC LIMIT 200""",(meta.get('context'),meta.get('main_goal'))).fetchall()
                    current_goals=[project(row) for row in current_rows]
                    for g in current_goals:
                        g['source']=g['target'].get('origin',g['source'])
                    group_totals={}
                    for row in db.execute("SELECT type,target,parent_id,source,status,success_criteria FROM gm_goals WHERE json_extract(target,'$.context_id')=? AND type IN ('world_investigation','leave_bedroom','leave_house')",(meta.get('context'),)):
                        g=dict(row);g['target']=json.loads(g['target']);g['source']=g['target'].get('origin',g['source'])
                        g['success_criteria']=json.loads(g['success_criteria'])
                        key=progress_key(g)
                        if key is not None:group_totals.setdefault(key,Counter())[g['status']]+=1
                    main=next((g for g in current_goals if g['id']==meta.get('main_goal')),None)
                    active=next((g for g in current_goals if g['status']=='active' and g['id']!=meta.get('main_goal')),
                                next((g for g in current_goals if g['status']=='active'),None))
                    display_goals=compact_progress(current_goals,group_totals)
                    cards=session_cards(display_goals,meta.get('main_goal'),ancestry=current_goals)
                    card_total=len(session_cards(display_goals,meta.get('main_goal'),limit=len(display_goals),ancestry=current_goals))
                    visible_current=[g for g in current_goals if g['status']!='cancelled']
                    focus=main if main and main['status'] in ('completed','failed','cancelled') else active or (max(visible_current,key=lambda g:g['updated_at']) if visible_current else main)
                    if focus:focus=next((g for g in display_goals if g['id']==focus['id']),focus)
                    hy_events=[dict(id=e['id'],event=e['event'],data=json.loads(e['data']),timestamp=e['at'])
                               for e in db.execute('SELECT * FROM hy_events ORDER BY id DESC LIMIT 24')]
                    goal_ids={g['id'] for g in current_goals}
                    timeline=sorted(hy_events+[e for e in result['events'] if e['goal_id'] in goal_ids],
                                    key=lambda e:e['timestamp'],reverse=True)[:24]
                    facts={r['key']:dict(value=json.loads(r['value']),status=r['status'],source=r['source'],timestamp=r['at'])
                           for r in db.execute('SELECT * FROM hy_facts WHERE context=?',(meta.get('context'),))}
                    metrics=[json.loads(r['result']) for r in db.execute('SELECT * FROM hy_inference ORDER BY at DESC LIMIT 6')]
                    decision=next((e['data'] for e in hy_events if e['event']=='goal_replanned'),{})
                    result['hybrid']=dict(main_goal=main,active_goal=active,current_goal=focus,skill=meta.get('executing_skill'),
                        goals=current_goals,display_goals=display_goals,session_goals=cards,session_goal_total=card_total,world=facts,timeline=timeline,models=metrics,decision=decision,
                        learning=meta.get('learning_stats',{}),
                        model_events=[e for e in hy_events if e['event'].startswith('model_')][:6])
                    if focus:
                        result['current']=focus
            result.update(available=True, message='Persistent goals · read-only display', schema_version=version[0])
    except (sqlite3.Error, ValueError, KeyError, TypeError, OSError):
        # Never reset/migrate a damaged or locked database from presentation.
        result.update(available=False, message='Managed goals temporarily unavailable', goals=[], current=None, events=[])
    return result
