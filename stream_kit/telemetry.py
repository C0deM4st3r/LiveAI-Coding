"""Small event projection for the read-only stream display; no controller access."""

import json
import sys
import time
from pathlib import Path

KIT = Path(__file__).resolve().parent
STATUS = KIT / "runtime" / "status.json"


def initial_status():
    return {"timestamp": None, "goal": "Connect to mGBA and observe the game",
            "status": "Waiting for agent", "mode": "Setup", "episode": "—",
            "step": 0, "limit": None, "button": None, "history": [],
            "available_buttons": [], "story": [],
            "decision": "No gameplay events yet", "outcome": "Waiting for an observation",
            "reward": None, "return": 0.0, "active": False,
            "source": "Waiting for observation", "scene": "Unknown", "vision_summary": "",
            "uncertainties": [], "frame_version": None, "qwen_calls": 0, "cache_hits": 0,
            "qwen_reason": "No inference requested", "qwen_latency": None,
            "checks": {"passed": 0, "failed": 0}, "budget_label": "actions",
            "visual_kind": "unknown", "model_ui": "unknown", "feed_seq": 0,
            "checkpoint_name": None, "checkpoint_totals": {}, "checkpoint_history": [],
            "goals": [], "goals_explicit": False}


def start_attempt(state, name, record):
    # Only one checkpoint runs at a time. An unfinished previous attempt is
    # interrupted, never silently counted as a failed goal.
    for old_name, totals in state["checkpoint_totals"].items():
        if totals["active"]:
            finish_attempt(state, "INTERRUPTED", record, name=old_name,
                           detail="Previous attempt did not finish before another started")
    totals = state["checkpoint_totals"].pop(name, {
        "attempts": 0, "passed": 0, "failed": 0, "interrupted": 0, "active": False, "last_result": "Waiting"})
    state["checkpoint_totals"][name] = totals
    totals["attempts"] += 1
    totals.update(active=True, last_result="RUNNING", started_at=record["timestamp"], source=record.get("source", state["source"]))
    state["checkpoint_name"] = name
    # Names are bounded too; counters for recent checkpoints survive restarts.
    state["checkpoint_totals"] = dict(list(state["checkpoint_totals"].items())[-50:])


def finish_attempt(state, result, record, name=None, detail=None):
    name = name or state.get("checkpoint_name")
    totals = state["checkpoint_totals"].get(name)
    if totals and totals["active"]:
        totals[{"PASS": "passed", "FAIL": "failed", "INTERRUPTED": "interrupted"}[result]] += 1
        totals.update(active=False, last_result=result)
        state["checkpoint_history"] = (state["checkpoint_history"] + [{
            "name": name, "attempt": totals["attempts"], "result": result,
            "started_at": totals.get("started_at"), "finished_at": record["timestamp"],
            "source": totals.get("source", ""), "detail": detail or record.get("detail") or record.get("stop_reason") or record.get("reason") or "Attempt finished"}])[-30:]


def add_activity(state, record, kind, title, summary, hypothesis=False):
    state["feed_seq"] = state.get("feed_seq", 0) + 1
    state["story"] = (state["story"] + [{"kind": kind, "button": None,
        "sequence": state["feed_seq"], "step": state["step"], "timestamp": record["timestamp"],
        "source": record.get("source", state.get("source", "")), "decision": title,
        "outcome": " ".join(str(summary).split()), "hypothesis": hypothesis,
        "reward": None, "blocked": False,
        "call_id": record.get("call_id"), "qwen_phase": record.get("qwen_phase")}])[-60:]


def latest_action(state, record):
    actions = [row for row in reversed(state["story"])
               if row.get("kind", "action") == "action" and row.get("button") not in {None, "test"}]
    step = record.get("attempt", record.get("step"))
    if step is not None:
        return next((row for row in actions if row["step"] == step), None)
    return actions[0] if actions else None


def project(previous, record, preserve_feed=False):
    """Render recorded evidence, never invented reasoning or success."""
    state = {**previous, "history": list(previous["history"]),
             "story": [dict(item) for item in previous.get("story", [])],
             "checks": dict(previous.get("checks", {"passed": 0, "failed": 0})),
             "checkpoint_totals": {key: dict(value) for key, value in previous.get("checkpoint_totals", {}).items()},
             "checkpoint_history": list(previous.get("checkpoint_history", [])),
             "goals": [dict(item) for item in previous.get("goals", [])]}
    event = record["event"]
    if event in {"run_started", "episode_started"}:
        retained = {key: state[key] for key in ("story", "feed_seq", "checkpoint_totals", "checkpoint_history", "goals", "goals_explicit")}
        state = initial_status()
        state.update({key: value for key, value in retained.items() if key not in {"story", "feed_seq"}})
        if preserve_feed:
            state.update(story=retained["story"], feed_seq=retained["feed_seq"])
        state.update(status="Running", active=True,
                     source=record.get("source", "PLAYER · checkpoint run"),
                     mode={"train": "Learning", "evaluate": "Frozen evaluation",
                           "baseline": "Untrained baseline"}.get(record.get("mode"), "Rules / setup"),
                     episode=record.get("episode", "—"),
                     limit=record.get("max_steps", record.get("step_limit")),
                     continuous=record.get('continuous',False),
                     outcome="Restoring start / observing the room")
        if record.get("count_attempt", True):
            start_attempt(state, record.get("checkpoint_name") or record.get("goal") or "Controller rehearsal", record)
    if "available_buttons" in record:
        state["available_buttons"] = list(record["available_buttons"])
    state["timestamp"] = record["timestamp"]
    # Learning transitions use goal=bool; that is outcome evidence, not a title.
    if isinstance(record.get("goal"), str):
        state["goal"] = record["goal"]
        if not state.get("goals_explicit") and not record.get("source", "").startswith("CHECK"):
            state["goals"] = [{"id": "primary", "title": record["goal"], "status": "active"}]
    for key in ("source", "scene", "vision_summary", "uncertainties", "frame_version",
                "qwen_calls", "cache_hits", "qwen_reason", "qwen_latency", "budget_label", "visual_kind", "model_ui"):
        if key in record:
            if key == "source" and event == "decision":
                continue  # Policy-selection source is not the observation/source label.
            state[key] = record[key]
    if event == "goal_trial_status":
        state.update(status=record['status'], active=False, mode='Goal Manager · capability check',
                     outcome=record['outcome'], button=None, step=0, limit=None, budget_label='actions')
    elif event == "observer_status":
        state.update(status=record.get("status", "Observing"), active=record.get("active", False),
                     mode="Visible checks" if state["budget_label"] == "checks" else "Vision / memory", outcome=record.get("outcome", state["outcome"]))
    elif event == "walk_status":
        state.update(status=record.get("status", "Walking"), active=record.get("active", True),
                     mode="Navigator / frozen skill / action learning", budget_label="actions",
                     outcome=record.get("outcome", state["outcome"]))
    elif event == "attempt_started":
        start_attempt(state, record["checkpoint_name"], record)
        add_activity(state, record, "system", "Start checkpoint attempt", record["checkpoint_name"] + " · Attempt " + str(state["checkpoint_totals"][record["checkpoint_name"]]["attempts"]))
    elif event == "attempt_finished":
        if record["result"] not in {"PASS", "FAIL", "INTERRUPTED"}:
            raise ValueError("Invalid checkpoint attempt result")
        finish_attempt(state, record["result"], record)
        add_activity(state, record, "system", "Checkpoint · " + record["result"], record["detail"])
    elif event == "goals_updated":
        goals = record["goals"]
        if not isinstance(goals, list) or len(goals) > 20 or any(
            not isinstance(goal, dict) or not isinstance(goal.get("id"), str)
            or not isinstance(goal.get("title"), str) or goal.get("status") not in {"pending", "active", "complete"}
            for goal in goals) or len({goal["id"] for goal in goals}) != len(goals):
            raise ValueError("Invalid goal list")
        state.update(goals=[dict(goal) for goal in goals], goals_explicit=True)
    elif event == "activity":
        add_activity(state, record, record["kind"], record["title"], record["summary"], record.get("hypothesis", False))
        state["outcome"] = " ".join(str(record["summary"]).split())
    elif event == "checkpoint":
        result = record["result"]
        state.update(status="Checking" if result == "RUNNING" else "Check " + result.lower(),
                     active=result == "RUNNING", step=record.get("step", state["step"]),
                     mode="Visible checks", button=None, outcome=record["detail"], budget_label="checks")
        if result in {"PASS", "FAIL"}:
            state["checks"]["passed" if result == "PASS" else "failed"] += 1
            state["feed_seq"] += 1
            state["story"] = (state["story"] + [{"step": state["step"], "button": "test", "kind": "test",
                "sequence": state["feed_seq"], "timestamp": record["timestamp"], "source": state["source"],
                "decision": result + " · " + record["name"], "outcome": record["detail"],
                "reward": None, "blocked": False}])[-60:]
    if event == "decision":
        reasons = {"epsilon_exploration": "Explore: sample a random direction",
                   "learned_value": "Select a direction with the highest learned value",
                   "untrained_tie": "Untrained values tie: sample a direction"}
        state.update(button=record.get("button"), step=record.get("step", state["step"]),
                     decision=record.get("reason") or reasons.get(record.get("source"),
                                                                "Selected by the player"),
                     outcome="Action selected", status="Running", active=True)
    elif event == "action_started":
        if "source" not in record:
            state["source"] = "PLAYER · bounded controller inputs"
        if state["decision"] == "No gameplay events yet":
            state["decision"] = "Send a bounded controller input"
        state.update(button=record["button"], active=True, status="Running",
                     step=record.get("attempt", state["step"]), outcome="Executing action / waiting for frame")
        state["history"] = (state["history"] + [record["button"]])[-10:]
        state["feed_seq"] += 1
        state["story"] = (state["story"] + [{"step": state["step"], "button": record["button"], "kind": "action",
                                            "sequence": state["feed_seq"], "timestamp": record["timestamp"], "source": state["source"],
                                            "decision": state["decision"], "outcome": "Waiting for feedback",
                                            "reward": None, "blocked": False}])[-60:]
    elif event in {"action_feedback", "feedback"}:
        state["outcome"] = f"Pixel change: {record['mean_pixel_change']:.3f} (animation can change pixels)"
    elif event == "transition":
        state["reward"] = record["reward"]
        state["return"] += record["reward"]
        state["outcome"] = ("Downstairs landmarks confirmed" if record.get("goal") is True
                            else "View changed" if record["state"] != record["next_state"]
                            else "View unchanged — possibly blocked or turning")
    elif event == "likely_blocked":
        state["outcome"] = "Likely blocked — repeated unchanged observations"
        row = latest_action(state, record)
        if row:
            row["blocked"] = True
    elif event == "recovery_decision":
        state["button"] = record["new_direction"]
        state["decision"] = record["rule"] + " (recovery rule)"
    elif event == "memory_updated":
        state["outcome"] = "View changed; memory updated" if record["scene_changed"] else "View unchanged; memory updated"
    elif event == "observation":
        state["outcome"] = "Screenshot captured"
    elif event == "dialogue_detected":
        state.update(status="Handling textbox", active=True,
                     outcome="Textbox detected — continuing; goal not reached", reward=None)
    elif event == "dialogue_recovery":
        state.update(status="Handling textbox" if record["remaining"] else "Running", active=True,
                     outcome=record["reason"], reward=None)
    elif event in {"episode_stopped", "run_stopped", "action_aborted"}:
        finish_attempt(state, "PASS" if record.get("success") is True else "FAIL" if record.get("success") is False else "INTERRUPTED", record)
        if record.get("success") is True:
            for goal in state["goals"]:
                if goal["title"] == state["goal"] and goal["status"] == "active":
                    goal["status"] = "complete"
        success = record.get("success") is True
        state.update(status="Goal reached" if success else "Stopped", active=False,
                     outcome=record.get("stop_reason") or record.get("reason") or "Run finished")
        if state["outcome"] == "dialogue_detected_no_goal":
            state.update(status="Dialogue detected", outcome="Textbox detected — goal not reached")
        if "return" in record:
            state["return"] = record["return"]
        if "steps" in record:
            state["step"] = record["steps"]
    # Later feedback enriches the same action row, not a duplicate story entry.
    if state["story"] and event in {"action_feedback", "feedback", "transition", "memory_updated",
                                    "likely_blocked", "action_aborted", "dialogue_detected", "dialogue_recovery"}:
        row = latest_action(state, record)
        if row:
            row["outcome"] = state["outcome"]
            if event == "transition":
                row["reward"] = record["reward"]
    # Meaningful system work also belongs in the feed; observations/heartbeats
    # themselves stay out so a stationary room cannot flood the story.
    if event == "recovery_decision":
        add_activity(state, record, "recovery", "Choose a recovery direction", state["decision"])
    elif event == "memory_updated":
        add_activity(state, record, "memory", "Update movement memory", state["outcome"])
    elif event == "q_update":
        add_activity(state, record, "learning", "Update learned action value",
                     f"{record.get('action', 'action')} · {record.get('old', '—')} → {record.get('new', '—')}")
    elif event == "state_loaded":
        add_activity(state, record, "system", "Restore emulator checkpoint", record.get("state", "Checkpoint restored"))
    elif event in {"run_stopped", "episode_stopped", "action_aborted"}:
        add_activity(state, record, "system", state["status"], state["outcome"])
    elif event in {"dialogue_detected", "dialogue_recovery"}:
        add_activity(state, record, "recovery", "Handle textbox" if event == "dialogue_detected" else "Textbox recovery", state["outcome"])
    return state


class Publisher:
    def __init__(self, path=STATUS, keep_feed=False):
        self.path = Path(path)
        self.state = initial_status()
        self.log = None
        self.warned = False
        self.keep_feed = keep_feed
        if keep_feed:
            try:
                saved = json.loads(self.path.read_text(encoding="utf-8"))
                if not isinstance(saved, dict):
                    saved = {}
                if isinstance(saved.get("story"), list):
                    self.state["story"] = saved["story"][-60:]
                    self.state["feed_seq"] = saved.get("feed_seq", len(self.state["story"]))
                if isinstance(saved.get("checkpoint_totals"), dict):
                    self.state["checkpoint_totals"] = saved["checkpoint_totals"]
                self.state["checkpoint_history"] = saved.get("checkpoint_history", [])[-30:]
                self.state["goals"] = saved.get("goals", [])[:20]
                self.state["goals_explicit"] = saved.get("goals_explicit", False)
            except (OSError, ValueError, TypeError):
                pass

    def publish(self, record, log):
        if self.log != str(log):
            retained = {key: self.state[key] for key in ("story", "feed_seq", "checkpoint_totals", "checkpoint_history", "goals", "goals_explicit")}
            self.state = initial_status()
            if self.keep_feed:
                self.state.update(retained)
            self.log = str(log)
        self.state = project(self.state, record, preserve_feed=self.keep_feed)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_suffix(".tmp")
            temporary.write_text(json.dumps(self.state), encoding="utf-8")
            for attempt in range(5):
                try:
                    temporary.replace(self.path)
                    break
                except PermissionError:
                    if attempt == 4:
                        raise
                    time.sleep(0.02)
        except OSError as exc:
            # A presentation failure must not fail a controller action or alter learning.
            if not self.warned:
                print(f"Overlay telemetry unavailable: {exc}", file=sys.stderr)
                self.warned = True


publisher = Publisher(keep_feed=True)
