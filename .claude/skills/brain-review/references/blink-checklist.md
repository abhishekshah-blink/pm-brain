# Blinkhealth Code Review Checklist

Apply every item below during /brain-review. Mark pass [x] or fail [ ] with file:line.

## Testing
- [ ] New code has corresponding tests (unit or integration)
- [ ] Test names are descriptive — describe what behavior is being tested, not how
- [ ] Tests cover the happy path AND key failure/edge cases
- [ ] No tests were deleted without explanation

## Formatting & Style
- [ ] Python: `poetry run black --check .` passes (no reformatting needed)
- [ ] Python: imports are organized (stdlib → third-party → local)
- [ ] TypeScript/JS: ESLint passes (`npm run lint`)
- [ ] No commented-out code blocks left in (remove or document why)

## Django / Python Specific
- [ ] No bare `select_for_update()` without an enclosing `transaction.atomic()` block
- [ ] Bulk operations use `bulk_create()` or `bulk_update()` — not individual `.save()` in a loop
- [ ] `bulk_create()` is not expected to trigger `post_save` signals — code accounts for this
- [ ] No `Model.objects.all()` in a loop (N+1 query risk) — use `select_related` / `prefetch_related`
- [ ] New database queries use queryset methods, not raw SQL with string formatting
- [ ] Celery tasks are idempotent (safe to retry)
- [ ] Celery `apply_async` delay/countdown is appropriate — not blocking the request cycle
- [ ] New migrations are reversible (`RunPython` ops have a reverse function or `atomic=False` with explanation)
- [ ] No new hardcoded settings that should be in `settings.py` or environment variables

## Redis / Locking
- [ ] Redis lock scope is not too broad (not locking on a broad key like `lock:all_tasks`)
- [ ] Redis lock has a reasonable TTL set (not `None` / infinite)
- [ ] Lock acquisition failure is handled explicitly (not silently ignored)

## API / DRF (Django REST Framework)
- [ ] Serializer validation is not bypassed (no `.save(validated_data=...)` with unvalidated data)
- [ ] New endpoints have permission classes set explicitly — no accidental public endpoints
- [ ] Pagination is applied to list endpoints that could return large querysets

## Security
- [ ] No secrets, API keys, or tokens hardcoded in source code
- [ ] User input is not passed to `eval()`, `exec()`, `os.system()`, or shell commands
- [ ] No SQL string interpolation (`f"SELECT * FROM table WHERE id = {id}"`)
- [ ] File paths constructed from user input are validated/sanitized

## Frontend (React / TypeScript)
- [ ] No `useEffect` with missing dependencies (ESLint exhaustive-deps rule)
- [ ] No direct DOM manipulation (`document.getElementById` etc.) — use React refs
- [ ] API error states are handled in the UI (not just loading + success)
- [ ] No hardcoded URLs — use constants or environment variables

## General
- [ ] No `TODO`, `FIXME`, or `HACK` comments added without a Jira ticket reference
- [ ] No `print()` / `console.log()` debug statements left in production code paths
- [ ] Function/method names are descriptive and consistent with existing conventions in the file
