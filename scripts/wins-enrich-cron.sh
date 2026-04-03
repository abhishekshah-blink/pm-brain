#!/bin/zsh
# Wins enrichment — processes pending.jsonl into structured win files.
# Runs daily at 5:30pm. Called by cron. Uses a zsh login shell so ~/.zshrc env vars are available.

set -euo pipefail

CLAUDE="/Users/abhishek.shah/.local/bin/claude"
LOG="$HOME/pm/brain/logs/wins-enricher.log"
PENDING="$HOME/pm/brain/knowledge/wins/pending.jsonl"

# Nothing to do if no pending entries
if [[ ! -f "$PENDING" ]] || [[ ! -s "$PENDING" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M')] No pending wins entries. Skipping." >> "$LOG"
    exit 0
fi

TODAY=$(date +%Y-%m-%d)
WEEK=$(date +%G-W%V)

echo "[$(date '+%Y-%m-%d %H:%M')] Starting wins enrichment..." >> "$LOG"

"$CLAUDE" \
  --allowedTools "Read,Write,Bash,Glob,Grep,mcp__atlassian__jira_get_issue,mcp__atlassian__jira_search,mcp__github__get_file_contents" \
  -p "Read ~/pm/brain/.claude/skills/wins-enricher/SKILL.md for full instructions. Execute those instructions now. Today is $TODAY. ISO week: $WEEK." \
  >> "$LOG" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M')] Enrichment complete." >> "$LOG"
