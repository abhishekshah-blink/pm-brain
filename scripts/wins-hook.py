#!/usr/bin/env python3
"""
PostToolUse hook — captures work signals into wins/pending.jsonl.
Fires on Jira transitions, Jira ticket creation, and GitHub PR events.
Runs as a shell command; receives Claude Code hook payload on stdin.
"""

import json
import os
import sys
from datetime import date

PENDING = os.path.expanduser("~/brain/knowledge/wins/pending.jsonl")
INTERESTING_TRANSITIONS = {"done", "closed", "complete", "completed", "in review", "merged", "released"}


def append_entry(entry: dict):
    os.makedirs(os.path.dirname(PENDING), exist_ok=True)
    with open(PENDING, "a") as f:
        f.write(json.dumps(entry) + "\n")


def extract_response_key(tool_response) -> str:
    """Try to extract a Jira issue key from a tool response."""
    if not tool_response:
        return ""
    # Handle list of content blocks (MCP response format)
    if isinstance(tool_response, list):
        for block in tool_response:
            if isinstance(block, dict) and block.get("type") == "text":
                try:
                    data = json.loads(block.get("text", "{}"))
                    return data.get("key", "")
                except Exception:
                    pass
    # Handle direct dict
    if isinstance(tool_response, dict):
        return tool_response.get("key", "")
    # Handle raw string
    if isinstance(tool_response, str):
        try:
            data = json.loads(tool_response)
            return data.get("key", "")
        except Exception:
            pass
    return ""


def extract_response_pr_number(tool_response) -> str:
    """Try to extract a PR number from a create_pull_request response."""
    if not tool_response:
        return ""
    if isinstance(tool_response, list):
        for block in tool_response:
            if isinstance(block, dict) and block.get("type") == "text":
                try:
                    data = json.loads(block.get("text", "{}"))
                    return str(data.get("number", ""))
                except Exception:
                    pass
    if isinstance(tool_response, dict):
        return str(tool_response.get("number", ""))
    return ""


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool = payload.get("tool_name", "")
    inp = payload.get("tool_input", {})
    resp = payload.get("tool_response")
    today = date.today().isoformat()

    if tool == "mcp__atlassian__jira_transition_issue":
        issue_key = inp.get("issue_key", "").strip()
        transition = (inp.get("transition_name") or str(inp.get("transition_id", ""))).strip()
        if issue_key and any(t in transition.lower() for t in INTERESTING_TRANSITIONS):
            append_entry({
                "date": today,
                "source": "jira_transition",
                "issue_key": issue_key,
                "transition": transition,
            })

    elif tool == "mcp__atlassian__jira_create_issue":
        issue_key = extract_response_key(resp)
        fields = inp.get("fields", {})
        summary = fields.get("summary", "").strip()
        issue_type = ""
        issuetype = fields.get("issuetype", {})
        if isinstance(issuetype, dict):
            issue_type = issuetype.get("name", "")
        if summary:
            append_entry({
                "date": today,
                "source": "jira_created",
                "issue_key": issue_key,
                "summary": summary,
                "issue_type": issue_type,
            })

    elif tool == "mcp__github__create_pull_request":
        title = inp.get("title", "").strip()
        owner = inp.get("owner", "")
        repo_name = inp.get("repo", "")
        repo = f"{owner}/{repo_name}" if owner else repo_name
        pr_number = extract_response_pr_number(resp)
        if title:
            append_entry({
                "date": today,
                "source": "github_pr_created",
                "title": title,
                "repo": repo,
                "pr_number": pr_number,
            })

    elif tool == "mcp__github__merge_pull_request":
        owner = inp.get("owner", "")
        repo_name = inp.get("repo", "")
        repo = f"{owner}/{repo_name}" if owner else repo_name
        pr_number = str(inp.get("pull_number", ""))
        if repo and pr_number:
            append_entry({
                "date": today,
                "source": "github_pr_merged",
                "repo": repo,
                "pr_number": pr_number,
            })


if __name__ == "__main__":
    main()
