#!/usr/bin/env python3
"""
Skill Scout — scans Claude Code session transcripts from the past week to identify
repeatable processes that should become skills.

Designed to run every Monday via cron. Can also be invoked manually.

Output: ~/pm/brain/knowledge/scratch/skill-suggestions-{YYYY-WW}.md
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"
BRAIN_DIR = Path.home() / "pm" / "brain"
OUTPUT_DIR = BRAIN_DIR / "knowledge" / "scratch"
LOG_DIR = BRAIN_DIR / "logs"

# Tools that represent real work (not just reading)
WORK_TOOLS = {"Edit", "Write", "NotebookEdit", "Bash", "Agent"}

# Correction words — short follow-up from user indicating re-direction
CORRECTION_WORDS = ["no ", "wait", "actually", "instead", "not that", "wrong",
                    "don't", "stop", "undo", "revert", "different", "that's not"]

# Skills already in the system — don't suggest these again
EXISTING_SKILLS = {
    "brain-discovery", "brain-plan", "brain-prd", "brain-user-story",
    "brain-decision", "ops-feedback", "ops-bug", "brain-weekly-email",
    "brain-review", "brain-ship", "brain-investigate", "brain-sync",
    "wins", "wins-digest", "skill-scout",
    "eng-workflow", "pr-review", "ai-retro", "jira-status-update",
    "eng-scorecard", "generate-manual",
}


def log(msg: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "skill-scout.log"
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {msg}"
    print(line)
    with open(log_file, "a") as f:
        f.write(line + "\n")


def get_recent_transcripts(days: int = 7) -> list[Path]:
    """Find all .jsonl transcript files modified in the past N days."""
    cutoff = datetime.now() - timedelta(days=days)
    found = []

    if not PROJECTS_DIR.exists():
        return found

    for path in PROJECTS_DIR.rglob("*.jsonl"):
        # Skip directory-named jsonl (they're session dirs, not transcripts)
        if path.is_dir():
            continue
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            if mtime >= cutoff:
                found.append(path)
        except Exception:
            continue

    return sorted(found, key=lambda p: p.stat().st_mtime, reverse=True)


def parse_transcript(path: Path) -> dict | None:
    """Extract a structured summary from one session transcript."""
    messages = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    messages.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return None

    if not messages:
        return None

    user_messages = []
    tool_call_summaries = []
    skills_invoked = []
    correction_count = 0
    prev_role = None

    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", [])

        # --- User messages ---
        if role == "user":
            text = ""
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = block.get("text", "")
                        break

            if text and len(text) > 15:
                clean = text[:250].replace("\n", " ").strip()
                user_messages.append(clean)

                # Short follow-up after assistant = potential correction/re-direction
                if prev_role == "assistant" and len(text) < 120:
                    lower = text.lower()
                    if any(w in lower for w in CORRECTION_WORDS):
                        correction_count += 1

        # --- Assistant tool calls ---
        if role == "assistant" and isinstance(content, list):
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                tool_name = block.get("name", "")
                tool_input = block.get("input", {})

                if tool_name == "Skill":
                    skill = tool_input.get("skill", "")
                    if skill:
                        skills_invoked.append(skill)
                elif tool_name in WORK_TOOLS:
                    desc = tool_input.get("description", "")
                    cmd = tool_input.get("command", "")
                    label = desc or cmd or tool_name
                    tool_call_summaries.append(f"{tool_name}: {label[:70]}")

        prev_role = role

    if not user_messages:
        return None

    user_turns = len([m for m in messages if m.get("role") == "user"])
    if user_turns < 2:
        return None

    return {
        "path": str(path),
        "project": path.parent.name,
        "first_task": user_messages[0],
        "follow_ups": user_messages[1:6],
        "work_tool_count": len(tool_call_summaries),
        "tool_samples": tool_call_summaries[:8],
        "skills_invoked": list(set(skills_invoked)),
        "correction_count": correction_count,
        "user_turns": user_turns,
        "date": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d"),
    }


def build_prompt(sessions: list[dict], week_label: str) -> str:
    existing_list = ", ".join(f"/{s}" for s in sorted(EXISTING_SKILLS))

    lines = []
    for i, s in enumerate(sessions, 1):
        follow = "; ".join(s["follow_ups"]) if s["follow_ups"] else "—"
        tools = ", ".join(s["tool_samples"][:5]) if s["tool_samples"] else "—"
        skills = ", ".join(f"/{sk}" for sk in s["skills_invoked"]) if s["skills_invoked"] else "—"
        lines.append(f"""Session {i} [{s['date']}] (project: {s['project']})
  First request: {s['first_task']}
  Follow-ups: {follow}
  Work tool calls: {s['work_tool_count']} — {tools}
  Skills used: {skills}
  User corrections/re-directions: {s['correction_count']}
  Total user turns: {s['user_turns']}""")

    sessions_block = "\n\n".join(lines)

    return f"""You are analyzing Claude Code session transcripts from the past week (week {week_label}) to identify repeatable processes that would benefit from becoming skills.

EXISTING SKILLS — do not suggest these: {existing_list}

SESSIONS FROM THIS WEEK:
{sessions_block}

---

A process is worth making into a skill if:
- It appeared in 2+ sessions (frequency signal), OR
- It required 5+ work tool calls in one session (complexity signal), OR
- The user had to give 2+ corrections for the same kind of task (guidance overhead signal)
- AND it is general/reusable — not a one-off task

For each candidate skill, write:

## Candidate: [slug-style name]
**Trigger phrases:** what the user would say to invoke this (2–4 examples)
**Observed in:** Session numbers
**Pattern:** What the user was doing and why it's repetitive
**Why formalize:** What a skill adds that the user can't just ask for ad-hoc
**Proposed steps:**
1. ...
2. ...
**Complexity to build:** low / medium / high

Output 2–5 strong candidates only. If fewer than 2 clear patterns exist, say so and explain what you saw. Do not pad with weak suggestions."""


def run_scout(days: int = 7) -> str:
    week_label = datetime.now().strftime("%G-W%V")

    log(f"Scanning transcripts from past {days} days...")
    transcripts = get_recent_transcripts(days=days)
    log(f"Found {len(transcripts)} transcript files.")

    sessions = []
    for t in transcripts:
        parsed = parse_transcript(t)
        if parsed:
            sessions.append(parsed)

    log(f"Parsed {len(sessions)} substantive sessions.")

    if not sessions:
        return None, week_label

    prompt = build_prompt(sessions, week_label)

    # Write the prompt to a temp file for claude --print
    tmp = OUTPUT_DIR / "_skill_scout_prompt.txt"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    return tmp, week_label


def save_report(analysis: str, week_label: str, session_count: int) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    filename = OUTPUT_DIR / f"skill-suggestions-{week_label}.md"

    report = f"""---
title: Skill Suggestions — {week_label}
category: scratch
tags: [skill-scout, automation, weekly]
created: {today}
updated: {today}
---

# Skill Suggestions — {week_label}

*Generated by Skill Scout on {today} from {session_count} sessions.*
*Review these and run `/skill-scout` to draft any into a real skill.*

---

{analysis}
"""

    filename.write_text(report)
    return filename


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Skill Scout — surface repeatable processes from Claude Code sessions")
    parser.add_argument("--days", type=int, default=7, help="How many days back to scan (default: 7)")
    parser.add_argument("--print-prompt", action="store_true", help="Print the Claude prompt to stdout and exit (for debugging)")
    args = parser.parse_args()

    tmp_prompt, week_label = run_scout(days=args.days)

    if tmp_prompt is None:
        log("No substantive sessions found. Nothing to analyze.")
        sys.exit(0)

    if args.print_prompt:
        print(tmp_prompt.read_text())
        sys.exit(0)

    log(f"Prompt written to {tmp_prompt}")
    log("Run skill-scout-cron.sh to execute Claude analysis, or open the prompt manually.")
