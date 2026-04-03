#!/bin/zsh
# Daily Jira sync — runs every morning at 8:00am.
# Pulls the open sprint + recently updated tickets into knowledge/jira/.
# Called by cron. Uses a zsh login shell so ~/.zshrc env vars are available.

set -euo pipefail

CLAUDE="/Users/abhishek.shah/.local/bin/claude"
LOG="$HOME/pm/brain/logs/sync.log"

TODAY=$(date +%Y-%m-%d)

echo "[$(date '+%Y-%m-%d %H:%M')] Starting daily Jira sync..." >> "$LOG"

"$CLAUDE" \
  --allowedTools "Read,Write,Bash,Glob,Grep,mcp__atlassian__jira_search,mcp__atlassian__jira_get_issue,mcp__atlassian__jira_get_sprint_issues,mcp__atlassian__jira_get_sprints_from_board,mcp__atlassian__confluence_search,mcp__atlassian__confluence_get_page" \
  -p "Read ~/pm/brain/.claude/skills/brain-sync/SKILL.md for full instructions. Execute those instructions in full mode (sprint + recently updated tickets). Today is $TODAY. This is an automated background run — no interactive output needed, just sync the files and update brain.db." \
  >> "$LOG" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M')] Daily sync complete." >> "$LOG"
