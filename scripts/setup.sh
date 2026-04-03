#!/usr/bin/env bash
# ~/pm/brain/scripts/setup.sh
# Idempotent setup: creates directories, initializes SQLite schema, symlinks skills into ~/.claude/skills/
set -euo pipefail

BRAIN_DIR="${BRAIN_DIR:-$HOME/pm/brain}"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
# Must match folders under $BRAIN_DIR/.claude/skills/ (names Cursor / Claude Code discover via ~/.claude/skills symlinks)
SKILLS=(
  "brain-discovery"
  "brain-plan"
  "brain-prd"
  "brain-user-story"
  "brain-review"
  "brain-ship"
  "brain-investigate"
  "brain-sync"
  "ops-feedback"
  "ops-bug"
  "brain-weekly-email"
  "wins"
  "wins-enricher"
  "wins-digest"
  "brain-decision"
  "skill-scout"
)

echo "==> Setting up ~/pm/brain/ system"
echo ""

# ── Step 1: Directory structure ────────────────────────────────────────────
echo "[1/4] Creating directory structure..."
mkdir -p \
  "$BRAIN_DIR"/{inbox,data,scripts} \
  "$BRAIN_DIR"/knowledge/{prd,decisions,stakeholders,jira,confluence,features,domain,oncall,scratch} \
  "$BRAIN_DIR"/knowledge/wins/digests \
  "$BRAIN_DIR"/logs \
  "$BRAIN_DIR"/.claude/{agents,skills} \
  "$BRAIN_DIR"/.claude/skills/brain-plan \
  "$BRAIN_DIR"/.claude/skills/brain-ship \
  "$BRAIN_DIR"/.claude/skills/brain-sync \
  "$BRAIN_DIR"/.claude/skills/brain-review/references \
  "$BRAIN_DIR"/.claude/skills/brain-investigate/references \
  "$BRAIN_DIR"/.claude/skills/skill-scout \
  "$CLAUDE_SKILLS_DIR"
echo "    Done."

# ── Step 2: SQLite schema ──────────────────────────────────────────────────
echo "[2/4] Initializing SQLite database..."
DB="$BRAIN_DIR/data/brain.db"
if [ -f "$DB" ]; then
  echo "    brain.db already exists — skipping schema creation."
else
  sqlite3 "$DB" <<'SQL'
CREATE TABLE knowledge_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path   TEXT NOT NULL UNIQUE,
    category    TEXT NOT NULL,
    title       TEXT NOT NULL,
    summary     TEXT,
    tags        TEXT,
    created_at  TEXT,
    updated_at  TEXT,
    indexed_at  TEXT NOT NULL
);
CREATE TABLE stakeholders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    role        TEXT,
    team        TEXT,
    file_path   TEXT,
    jira_user   TEXT,
    notes       TEXT
);
CREATE TABLE features (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    jira_epic_key   TEXT,
    confluence_page_id TEXT,
    status          TEXT,
    prd_path        TEXT,
    github_repo     TEXT,
    github_pr_url   TEXT,
    created_at      TEXT,
    updated_at      TEXT
);
CREATE TABLE jira_tickets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_key      TEXT NOT NULL UNIQUE,
    summary         TEXT,
    status          TEXT,
    assignee        TEXT,
    priority        TEXT,
    epic_key        TEXT,
    sprint          TEXT,
    file_path       TEXT,
    last_synced     TEXT NOT NULL
);
CREATE TABLE confluence_pages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id         TEXT NOT NULL UNIQUE,
    title           TEXT NOT NULL,
    space_key       TEXT,
    parent_title    TEXT,
    url             TEXT,
    file_path       TEXT,
    last_synced     TEXT NOT NULL
);
CREATE TABLE relationships (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    from_type       TEXT NOT NULL,
    from_id         INTEGER NOT NULL,
    to_type         TEXT NOT NULL,
    to_id           INTEGER NOT NULL,
    relationship    TEXT NOT NULL,
    created_at      TEXT NOT NULL
);
CREATE INDEX idx_knowledge_category ON knowledge_items(category);
CREATE INDEX idx_knowledge_updated  ON knowledge_items(updated_at);
CREATE INDEX idx_jira_status        ON jira_tickets(status);
CREATE INDEX idx_jira_epic          ON jira_tickets(epic_key);
CREATE INDEX idx_features_status    ON features(status);
SQL
  echo "    brain.db initialized with schema."
fi

# ── Step 3: Symlink skills into ~/.claude/skills/ ──────────────────────────
echo "[3/4] Symlinking skills into $CLAUDE_SKILLS_DIR ..."
printf "    %-22s %-8s %s\n" "SKILL" "STATUS" "PATH"
printf "    %-22s %-8s %s\n" "-----" "------" "----"

for skill in "${SKILLS[@]}"; do
  src="$BRAIN_DIR/.claude/skills/$skill"
  tgt="$CLAUDE_SKILLS_DIR/$skill"

  if [ -L "$tgt" ] && [ "$(readlink "$tgt")" = "$src" ]; then
    printf "    %-22s %-8s %s\n" "$skill" "OK" "$tgt → $src"
  elif [ -e "$tgt" ] && [ ! -L "$tgt" ]; then
    printf "    %-22s %-8s %s\n" "$skill" "WARN" "$tgt exists as a real path — not overwriting. Resolve manually."
  else
    ln -sf "$src" "$tgt"
    printf "    %-22s %-8s %s\n" "$skill" "LINKED" "$tgt → $src"
  fi
done

# ── Step 4: Verify SKILL.md files are readable ────────────────────────────
echo ""
echo "[4/4] Verifying SKILL.md files..."
printf "    %-22s %s\n" "SKILL" "STATUS"
printf "    %-22s %s\n" "-----" "------"
all_ok=true
for skill in "${SKILLS[@]}"; do
  skill_dir="$BRAIN_DIR/.claude/skills/$skill"
  skill_md="$skill_dir/SKILL.md"
  skill_md_alt="$skill_dir/skill.md"
  if [ -r "$skill_md" ] || [ -r "$skill_md_alt" ]; then
    printf "    %-22s %s\n" "$skill" "readable"
  else
    printf "    %-22s %s\n" "$skill" "MISSING — populate $skill_dir/SKILL.md"
    all_ok=false
  fi
done

echo ""
if $all_ok; then
  echo "==> Setup complete. All skills are linked and readable."
else
  echo "==> Setup complete. Some SKILL.md files are missing — see above."
fi
echo ""
echo "Next steps:"
echo "  1. Open this repo in Cursor (~/brain) or use Claude Code here"
echo "  2. Run /brain-sync sprint  to pull your current Jira sprint"
echo "  3. Run /brain-plan <feature> to plan with brain + live Jira/Confluence context"
echo "  4. From Blinkhealth code repos, use the same skills if linked in ~/.claude/skills/"
