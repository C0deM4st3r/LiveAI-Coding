"""Read-only OBS projection of the shared map; never creates/migrates a DB."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3

if __package__:
    from .managed_goals import GOAL_DB
else:
    from managed_goals import GOAL_DB


def snapshot(path=GOAL_DB):
    result={'available':False,'message':'Waiting for visual mapping observations',
            'state':None,'area':None,'tiles':[],'entities':[],'edges':[],'areas':[],'path':[],
            'frontiers':[],'events':[],'encounters':[]}
    path=Path(path)
    if not path.is_file():
        return result
    try:
        with closing(sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True,timeout=.2)) as db:
            db.row_factory=sqlite3.Row
            db.execute('PRAGMA query_only=ON')
            db.execute('BEGIN')
            tables={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not {'wm_schema','wm_states','hy_meta'} <= tables:
                return result
            version=db.execute('SELECT version FROM wm_schema WHERE id=1').fetchone()
            if not version or version[0] not in (1,2):
                result['message']='Map reader requires a compatible schema'
                return result
            ctx=db.execute('SELECT value FROM hy_meta WHERE key=\'context\'').fetchone()
            if not ctx:
                return result
            context=json.loads(ctx[0])
            row=db.execute('SELECT * FROM wm_states WHERE context=?',(context,)).fetchone()
            result['available']=True
            if not row:
                return result
            state=dict(row)|{'player':json.loads(row['player'])}
            result['state']=state
            if 'wm_pose' in tables:
                pose=db.execute('SELECT * FROM wm_pose WHERE context=?',(context,)).fetchone()
                result['pose']=dict(pose)|{'pixels':json.loads(pose['pixels']),'trusted_tile':json.loads(pose['trusted_tile'])} if pose else None
            area=db.execute('SELECT * FROM wm_areas WHERE id=?',(state['area'],)).fetchone()
            if area:
                result['area']=dict(area)|{'grid':json.loads(area['grid'])}
                bounds=db.execute('SELECT COUNT(*),MIN(x),MAX(x),MIN(y),MAX(y) FROM wm_tiles WHERE area=?',(area['id'],)).fetchone()
                result['tile_count']=bounds[0]
                result['bounds']=dict(min_x=bounds[1],max_x=bounds[2],min_y=bounds[3],max_y=bounds[4])
                result['tiles_truncated']=bounds[0]>4096
                x,y=state['player'] or [0,0]
                tiles=db.execute('SELECT * FROM wm_tiles WHERE area=? ORDER BY ABS(x-?)+ABS(y-?),y,x LIMIT 4096',(area['id'],x,y)).fetchall()
                result['tiles']=[dict(r) for r in tiles]
                result['walked_count']=db.execute("SELECT COUNT(*) FROM wm_tiles WHERE area=? AND state='WALKABLE' AND visits>0",(area['id'],)).fetchone()[0]
                for tile in result['tiles']:tile['walked']=tile['state']=='WALKABLE' and tile['visits']>0
                if 'wm_appearance' in tables:
                    for tile in result['tiles']:
                        hint=db.execute('SELECT confidence FROM wm_appearance WHERE area=? AND x=? AND y=?',
                                        (area['id'],tile['x'],tile['y'])).fetchone()
                        tile['appearance_confidence']=hint[0] if hint else None
                entities=db.execute('SELECT * FROM wm_entities WHERE area=? ORDER BY CASE status WHEN \'VERIFIED\' THEN 0 WHEN \'OBSERVED\' THEN 1 ELSE 2 END,updated DESC LIMIT 20',(area['id'],)).fetchall()
                result['entities']=[dict(e)|{'position':json.loads(e['position']),
                    'current_seen':bool(db.execute('SELECT 1 FROM wm_evidence WHERE entity=? AND context=? AND status IN (\'OBSERVED\',\'VERIFIED\') LIMIT 1',(e['id'],context)).fetchone())} for e in entities]
                for entity in result['entities']:
                    if entity['status']=='VERIFIED' and not identity_has_captures(db,entity['id']):
                        entity['stored_status']='VERIFIED'
                        entity['status']='OBSERVED'
                cells={(t['x'],t['y']):t['state'] for t in tiles}
                result['frontiers']=[]
                for cell,kind in cells.items():
                    if kind!='WALKABLE': continue
                    for action,(dx,dy) in (('up',(0,-1)),('right',(1,0)),('down',(0,1)),('left',(-1,0))):
                        if cells.get((cell[0]+dx,cell[1]+dy),'UNKNOWN')!='UNKNOWN': continue
                        tries=db.execute("SELECT COUNT(*) FROM wm_navigation WHERE context=? AND area=? AND start=? AND action=? AND result IN ('unchanged','unlocalized')",
                                         (context,area['id'],json.dumps(cell,separators=(',',':')),action)).fetchone()[0]
                        if tries<3:
                            result['frontiers'].append(list(cell));break
            result['areas']=[dict(r) for r in db.execute('SELECT id,label,status FROM wm_areas ORDER BY updated DESC LIMIT 100')]
            result['edges']=[dict(r)|{'conditions':json.loads(r['conditions'])} for r in db.execute('SELECT * FROM wm_edges ORDER BY updated DESC LIMIT 100')]
            result['portals']=[];result['arrival']=None
            if 'wm_passages' in tables:
                for row in db.execute('SELECT * FROM wm_passages WHERE source=? OR destination=? ORDER BY at DESC LIMIT 40',(state['area'],state['area'])):
                    if not distinct_captures(db,json.loads(row['evidence']),3):continue
                    departing=row['source']==state['area']
                    destination=row['destination'] if departing else row['source']
                    label=db.execute('SELECT label FROM wm_areas WHERE id=?',(destination,)).fetchone()[0]
                    result['portals'].append({'id':row['id'],'role':'exit' if departing else 'entry',
                        'position':json.loads(row['source_position'] if departing else row['arrival_position']),
                        'action':row['action'] if departing else None,'destination':destination,'destination_label':label,'status':'VERIFIED'})
                    if not departing and row['context']==context and result['arrival'] is None:
                        result['arrival']={'source':row['source'],'source_label':label,'position':json.loads(row['arrival_position'])}
            for edge in result['edges']:
                if edge['status']=='VERIFIED' and not distinct_captures(db,json.loads(edge['evidence']).get('observations',[]),3):
                    edge['stored_status']='VERIFIED'
                    edge['status']='NEEDS_REVIEW'
            result['motion_counts']={r[0]:r[1] for r in db.execute('SELECT result,COUNT(*) FROM wm_navigation WHERE context=? GROUP BY result',(context,))}
            events=[dict(r)|{'data':json.loads(r['data'])} for r in db.execute('SELECT * FROM wm_events ORDER BY id DESC LIMIT 60')]
            result['events']=[e for e in events if e['data'].get('context')==context][:12]
            # Premapping/observations cannot push the active path out of a short
            # event window. Retrieve this context/area's actual latest proposal.
            decision=next((dict(e)|{'data':json.loads(e['data'])} for e in db.execute(
                "SELECT * FROM wm_events WHERE event IN ('navigation_route_selected','navigation_route_released') AND json_extract(data,'$.context')=? AND json_extract(data,'$.area')=? ORDER BY id DESC LIMIT 1",(context,state['area']))),None)
            route=decision or next((dict(e)|{'data':json.loads(e['data'])} for e in db.execute(
                "SELECT * FROM wm_events WHERE event='navigation_route_proposed' AND json_extract(data,'$.context')=? AND json_extract(data,'$.area')=? ORDER BY id DESC LIMIT 1",(context,state['area']))),None)
            if route:
                result['path_selected']=route['event']=='navigation_route_selected'
                result['path_status']='Selected route' if result['path_selected'] else 'Local guidance / route overridden' if decision else 'Proposal only'
                result['path_reason']=route['data'].get('reason','')
                proposed=route['data'].get('path',[])
                if state['player'] and proposed.count(state['player'])==1:
                    result['path']=proposed[proposed.index(state['player']):]
                    result['path_unknown']=route['data'].get('unknown',[])
                    result['path_reason']=route['data'].get('reason','')
                elif proposed:
                    result['path_status']='Player off route · replan needed'
            result['encounters']=[dict(r) for r in db.execute('SELECT e.name,c.area,c.status,COUNT(*) AS count,MAX(c.at) AS last_seen FROM wm_encounters c JOIN wm_entities e ON e.id=c.entity GROUP BY e.name,c.area,c.status ORDER BY last_seen DESC LIMIT 20')]
            result['external_knowledge']=[dict(r) for r in db.execute('SELECT id,name,kind,area,status FROM wm_entities WHERE status=\'EXTERNAL\' ORDER BY updated DESC LIMIT 5')]
            result['investigations']=[dict(r) for r in db.execute('SELECT id,kind,budget,used,status,outcome FROM wm_investigations WHERE context=? ORDER BY updated DESC LIMIT 6',(context,))]
            result['message']='Visual map · local coordinates are relative to measured anchors'
    except (sqlite3.Error,ValueError,TypeError,KeyError):
        result['available']=False
        result['message']='Map is temporarily unavailable'
    return result


def distinct_captures(db, observations, minimum):
    captures=set()
    for oid in observations:
        row=db.execute('SELECT data FROM wm_observations WHERE id=?',(oid,)).fetchone()
        capture=json.loads(row[0]).get('capture_id') if row else None
        if capture: captures.add(capture)
    return len(captures)>=minimum


def identity_has_captures(db, entity):
    for proof in db.execute("SELECT data FROM wm_evidence WHERE entity=? AND status='VERIFIED'",(entity,)):
        samples=[]
        for eid in json.loads(proof[0]).get('identity_evidence',[]):
            row=db.execute('SELECT reference FROM wm_evidence WHERE id=? AND entity=?',(eid,entity)).fetchone()
            if row: samples.append(row[0])
        if distinct_captures(db,samples,2): return True
    return False
