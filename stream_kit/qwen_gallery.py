"""Bounded evidence gallery: only images actually submitted to Qwen."""
import json
from pathlib import Path
import re
import time

IDENTIFIER = re.compile(r"[0-9a-f]{32}")
LIMIT = 10


class QwenGallery:
    def __init__(self, root):
        self.root = Path(root)
        self.manifest = self.root / "history.json"

    def read(self):
        try:
            rows = json.loads(self.manifest.read_text(encoding="utf-8"))
            return [row for row in rows if isinstance(row, dict)
                    and IDENTIFIER.fullmatch(str(row.get("id", "")))][-LIMIT:]
        except (OSError, ValueError, TypeError):
            return []

    def write(self, rows):
        self.root.mkdir(parents=True, exist_ok=True)
        temporary = self.manifest.with_suffix(".tmp")
        temporary.write_text(json.dumps(rows[-LIMIT:]), encoding="utf-8")
        for attempt in range(6):
            try:
                temporary.replace(self.manifest)
                break
            except PermissionError:
                if attempt==5:
                    raise
                time.sleep(.04)
        # This directory owns only UUID-named Qwen captures. Never remove other
        # artifacts, protected game states, or anything outside this exact root.
        retained = {row["id"] + ".png" for row in rows[-LIMIT:]}
        root = self.root.resolve()
        for path in self.root.glob("*.png"):
            if IDENTIFIER.fullmatch(path.stem) and path.name not in retained:
                if path.resolve().parent == root:
                    path.unlink(missing_ok=True)

    def capture(self, identifier, image, *, timestamp, trigger, goal, source):
        if not IDENTIFIER.fullmatch(identifier):
            raise ValueError("Invalid Qwen capture ID")
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / (identifier + ".png")
        temporary = path.with_suffix(".tmp")
        image.save(temporary, format="PNG")
        temporary.replace(path)
        rows = [row for row in self.read() if row["id"] != identifier]
        rows.append({"id": identifier, "image": "/qwen-image/" + identifier + ".png",
                     "timestamp": timestamp, "trigger": " ".join(trigger.split()),
                     "goal": goal, "source": source, "status": "Waiting for Qwen",
                     "response": "Waiting for response", "latency": None, "stale": False})
        self.write(rows)

    def finish(self, identifier, response, *, status, latency=None, stale=False):
        rows = self.read()
        row = next((item for item in rows if item["id"] == identifier), None)
        if row is None:
            return False  # An evicted late reply must not resurrect its image.
        row.update(response=" ".join(response.split()), status=status, latency=latency, stale=stale)
        self.write(rows)
        return True

    def image_path(self, identifier):
        if IDENTIFIER.fullmatch(identifier) and any(row["id"] == identifier for row in self.read()):
            path = self.root / (identifier + ".png")
            if path.resolve().parent == self.root.resolve():
                return path
        return None
