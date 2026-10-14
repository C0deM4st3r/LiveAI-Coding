"""Serve stream panels; optional trusted local operator adapter enables controls."""

import argparse
import json
import os
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4

if __package__:
    from .telemetry import STATUS, initial_status
    from .qwen_gallery import QwenGallery
    from .managed_goals import GOAL_DB, snapshot
    from .world_map import snapshot as map_snapshot
    from .queued_goals import snapshot as queue_snapshot
else:
    from telemetry import STATUS, initial_status
    from qwen_gallery import QwenGallery
    from managed_goals import GOAL_DB, snapshot
    from world_map import snapshot as map_snapshot
    from queued_goals import snapshot as queue_snapshot

PAGE = Path(__file__).with_name("actions.html")
GOAL_PAGE = Path(__file__).with_name("goal.html")
VISION_PAGE = Path(__file__).with_name("vision.html")
DASHBOARD_PAGE = Path(__file__).with_name("dashboard.html")
ARCHITECTURE_PAGE = Path(__file__).with_name("architecture.html")
LAB_PAGE = Path(__file__).with_name('test_lab.html')


def handler_for(status_path=STATUS, goal_db=GOAL_DB, lab=None):
    instance_id = uuid4().hex

    class Handler(BaseHTTPRequestHandler):
        def discard_small_body(self):
            # Closing with unread client bytes can reset a Windows connection
            # before its rejection response arrives. Never drain unbounded data.
            previous=self.connection.gettimeout()
            try:
                length=int(self.headers.get('Content-Length','0'))
                if 0<length<=8192:
                    self.connection.settimeout(2)
                    self.rfile.read(length)
            except (ValueError,OSError):pass
            finally:self.connection.settimeout(previous)

        def lab_host(self):
            return self.headers.get('Host') in {f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}

        def send_json(self,payload,code=200):
            data=json.dumps(payload).encode('utf-8')
            self.send_response(code)
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Cache-Control','no-store')
            self.send_header('Content-Length',str(len(data)))
            self.end_headers();self.wfile.write(data)

        def do_POST(self):
            route=urlsplit(self.path).path
            if route not in ('/test-lab/run','/test-lab/stop','/test-lab/preview','/test-lab/keep-playing','/test-lab/enqueue','/test-lab/cancel-queued'):
                self.discard_small_body();self.send_error(501);return
            if lab is None:
                self.discard_small_body();self.send_json({'error':'Test console controls are unavailable'},503);return
            origin=self.headers.get('Origin')
            if (not self.lab_host() or origin!='http://'+self.headers.get('Host','')
                    or not secrets.compare_digest(self.headers.get('X-Test-Lab-Token',''),lab.token)):
                self.discard_small_body();self.send_json({'error':'Same-origin test-console token required'},403);return
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=8192 or self.headers.get('Content-Type','').split(';')[0]!='application/json':
                    raise ValueError('Use a small JSON settings object')
                body=json.loads(self.rfile.read(length))
                if type(body) is not dict:raise ValueError('Settings object required')
                if route=='/test-lab/enqueue':
                    if set(body)!={'text','request_id','allow_external'}:raise ValueError('Literal objective, request ID and planning consent required')
                    result=lab.enqueue(body['text'],body['request_id'],body['allow_external'])
                elif route=='/test-lab/cancel-queued':
                    if set(body)!={'request_id'}:raise ValueError('Queued request ID required')
                    result=lab.cancel_queued(body['request_id'])
                elif route=='/test-lab/stop':
                    if body:raise ValueError('Stop takes no process ID or command')
                    result=lab.stop()
                elif route=='/test-lab/keep-playing':
                    if set(body)!={'job_id','enabled'}:raise ValueError('Owned job ID and boolean switch required')
                    result=lab.keep_playing(body['job_id'],body['enabled'])
                else:
                    if set(body)!={'kind','parameters'}:raise ValueError('Workflow and parameters required')
                    if route.endswith('/preview'):
                        if __package__:from .test_lab import compile_command
                        else:from test_lab import compile_command
                        import subprocess
                        result={'command':subprocess.list2cmdline(compile_command(body['kind'],body['parameters']))}
                    else:result=lab.start(body['kind'],body['parameters'])
                self.send_json(result)
            except (ValueError,TypeError) as exc:self.send_json({'error':str(exc)},400)
            except RuntimeError as exc:self.send_json({'error':str(exc)},409)
            except OSError:self.send_json({'error':'Unable to launch owned job; no success awarded'},500)

        def do_GET(self):
            route = urlsplit(self.path).path
            if route == '/health':
                self.send_json({'service': 'pokemon-stream-kit', 'instance_id': instance_id,
                                'pid': os.getpid(), 'mode': 'operator' if lab is not None else 'view-only',
                                'controls_available': lab is not None,
                                'status_available': Path(status_path).is_file(),
                                'goals_available': Path(goal_db).is_file()})
                return
            if route in ('/test-lab/options','/test-lab/status'):
                if not self.lab_host():self.send_error(403);return
                if lab is None:
                    self.send_json({'controls_available': False, 'mode': 'view-only',
                                    'message': 'Viewer mode: no gameplay controller is loaded.'})
                elif route.endswith('/options'):
                    if __package__:from .test_lab import catalog
                    else:from test_lab import catalog
                    self.send_json(catalog() | {'controls_available': True})
                else:self.send_json(lab.state())
                return
            if route=='/test-lab':
                payload=LAB_PAGE.read_bytes();mime='text/html; charset=utf-8'
            elif route in {"/", "/index.html", "/actions"}:
                payload = PAGE.read_bytes()
                mime = "text/html; charset=utf-8"
            elif route in {"/goal", "/goal.html"}:
                payload = GOAL_PAGE.read_bytes()
                mime = "text/html; charset=utf-8"
            elif route == "/status":
                try:
                    state = json.loads(Path(status_path).read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    state = initial_status()
                if not isinstance(state, dict):
                    state = initial_status()
                payload = json.dumps(state).encode("utf-8")
                mime = "application/json; charset=utf-8"
            elif route == "/managed-goals":
                payload = json.dumps(snapshot(goal_db)|{'queue':queue_snapshot(goal_db)}).encode('utf-8')
                mime = "application/json; charset=utf-8"
            elif route == "/world-map":
                payload = json.dumps(map_snapshot(goal_db)).encode('utf-8')
                mime = "application/json; charset=utf-8"
            elif route == "/vision":
                payload = VISION_PAGE.read_bytes()
                mime = "text/html; charset=utf-8"
            elif route == "/dashboard":
                payload = DASHBOARD_PAGE.read_bytes()
                mime = "text/html; charset=utf-8"
            elif route == "/architecture":
                payload = ARCHITECTURE_PAGE.read_bytes()
                mime = "text/html; charset=utf-8"
            elif route == "/qwen-history":
                payload = json.dumps(QwenGallery(Path(status_path).parent / "qwen").read()).encode("utf-8")
                mime = "application/json; charset=utf-8"
            elif route.startswith("/qwen-image/") and route.endswith(".png"):
                path = QwenGallery(Path(status_path).parent / "qwen").image_path(route.removeprefix("/qwen-image/").removesuffix(".png"))
                if path is None:
                    self.send_error(404)
                    return
                try:
                    payload = path.read_bytes()
                except OSError:
                    self.send_error(404)
                    return
                mime = "image/png"
            elif route == "/frame":
                try:
                    payload = Path(status_path).with_name("frame.png").read_bytes()
                except OSError:
                    self.send_error(404)
                    return
                mime = "image/png"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *_):
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument('--view-only', action='store_true',
                        help='Serve panels without gameplay dependencies or operator controls')
    parser.add_argument('--status-path', type=Path, default=STATUS,
                        help='Read-only status JSON source (custom paths require --view-only)')
    parser.add_argument('--goal-db', type=Path, default=GOAL_DB,
                        help='Read-only shared goal/map SQLite source (custom paths require --view-only)')
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Use a port between 1 and 65535")
    if not args.view_only and (args.status_path != STATUS or args.goal_db != GOAL_DB):
        parser.error('Custom data paths require --view-only; operator controls use the project profile')
    # The public starter intentionally ships no gameplay/controller module.
    # Select viewer mode only for that known absence; an installed but broken
    # operator dependency remains an explicit error rather than hiding a fault.
    view_only = args.view_only or not Path(__file__).with_name('test_lab.py').is_file()
    try:
        lab = None
        if not view_only:
            if __package__:from .test_lab import LabRunner
            else:from test_lab import LabRunner
            lab = LabRunner()
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(args.status_path, args.goal_db, lab))
    except ImportError as exc:
        print(f'Operator dependencies unavailable ({exc.name}); use --view-only for the standalone panels.')
        return 1
    except OSError as exc:
        print(f"Cannot start overlay: {exc}")
        return 1
    print(f"OBS actions: http://127.0.0.1:{args.port}/ (480 x 720, or taller)", flush=True)
    print(f"OBS goal: http://127.0.0.1:{args.port}/goal (match game width x 160)", flush=True)
    print(f"Visible vision checks: http://127.0.0.1:{args.port}/vision (1280 x 720)", flush=True)
    print(f"Running scene: http://127.0.0.1:{args.port}/dashboard (2560 x 1440; game=40–60 percent)", flush=True)
    mode = 'viewer mode; controls disabled' if view_only else 'local operator controls + stream panels'
    print(f'Test console: http://127.0.0.1:{args.port}/test-lab ({mode})',flush=True)
    print(f'Architecture: http://127.0.0.1:{args.port}/architecture | Health: /health', flush=True)
    print("Add ?demo=1 for a labeled visual demo with no game input. Ctrl+C stops this server.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
