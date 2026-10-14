"""Smoke-check the retained presentation without any gameplay or emulator input."""

import json
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

if __package__:
    from .serve import handler_for
    from .telemetry import Publisher, initial_status
else:
    from serve import handler_for
    from telemetry import Publisher, initial_status


def main():
    with tempfile.TemporaryDirectory() as temporary:
        snapshot = Path(temporary) / "status.json"
        database = Path(temporary) / "goals.sqlite3"
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(snapshot, database))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with urlopen(base + "/status") as response:
                waiting = json.load(response)
            assert waiting == initial_status()
            assert not waiting["available_buttons"] and not waiting["story"]
            with urlopen(base + "/health") as response:
                health = json.load(response)
            assert health["mode"] == "view-only" and not health["controls_available"]
            for route in ("/actions", "/goal", "/dashboard", "/test-lab", "/vision",
                          "/architecture", "/actions?demo=1", "/goal?demo=1"):
                with urlopen(base + route) as response:
                    assert b"<!doctype html>" in response.read()
            with urlopen(base + "/qwen-history") as response:
                assert json.load(response) == []
            for route in ("/managed-goals", "/world-map"):
                with urlopen(base + route) as response:
                    assert not json.load(response)["available"]
            for route in ("/test-lab/options", "/test-lab/status"):
                with urlopen(base + route) as response:
                    assert not json.load(response)["controls_available"]
            for route in ("run", "stop", "preview", "enqueue", "cancel-queued", "keep-playing"):
                request = Request(base + "/test-lab/" + route, data=b"{}",
                                  headers={"Content-Type": "application/json", "Origin": base})
                try:
                    with urlopen(request):
                        raise AssertionError(f"Viewer accepted control route: {route}")
                except HTTPError as error:
                    assert error.code == 503
                    error.close()
            assert not snapshot.exists() and not database.exists()
            display = Publisher(snapshot)
            for name, fields in [
                ("run_started", {"goal": "Test display only", "available_buttons": ["up"], "step_limit": 2}),
                ("decision", {"step": 1, "button": "up", "reason": "Test event; no emulator input"}),
                ("action_started", {"button": "up", "attempt": 1}),
                ("action_feedback", {"mean_pixel_change": 0}),
            ]:
                display.publish({"event": name, "timestamp": "2026-10-08T00:00:00+00:00", **fields}, "test")
            with urlopen(base + "/status") as response:
                shown = json.load(response)
            assert shown["available_buttons"] == ["up"]
            assert len(shown["story"]) == 1 and shown["story"][0]["button"] == "up"
            assert shown["goal"] == "Test display only"
            for route in ("/../LIVE_RESTART_PROMPT.md", "/checkpoints/rehearsal_start.state", "/brain.json"):
                try:
                    with urlopen(base + route):
                        raise AssertionError(f"Unexpected exposed route: {route}")
                except HTTPError as error:
                    assert error.code == 404
                    error.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
    print("Stream kit ready: six panels, waiting state, read-only data, disabled controls and event projection pass.")
    print("No game input was sent; no real display snapshot was changed.")


if __name__ == "__main__":
    main()
