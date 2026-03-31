#!/bin/bash
# Weekly wins digest — runs every Friday, generates a weekly summary.
# Called by cron. Sources the user environment so MCP credentials are available.

set -euo pipefail

CLAUDE="/Users/abhishek.shah/.local/bin/claude"
LOG="$HOME/brain/logs/wins-digest.log"

TODAY=$(date +%Y-%m-%d)
WEEK=$(date +%G-W%V)

echo "[$(date '+%Y-%m-%d %H:%M')] Starting weekly wins digest ($WEEK)..." >> "$LOG"

"$CLAUDE" \
  --allowedTools "Read,Write,Bash,Glob,Grep" \
  -p "Read ~/brain/.claude/skills/wins-digest/SKILL.md for full instructions. Execute those instructions with scope=weekly. Today is $TODAY. ISO week: $WEEK." \
  >> "$LOG" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M')] Digest complete." >> "$LOG"
