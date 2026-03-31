# Blinkhealth Debug Patterns

Common root causes and investigation patterns for Blinkhealth services. Reference during /brain-investigate.

## Redis / Locking Issues

**Pattern: Lock acquired after read → race condition**
- Symptom: Duplicate assignments, double-processing, count mismatches
- Root cause: Code reads a value (e.g. task count = 0) and then acquires a lock — another request sees the same value between the read and the lock
- Fix: Acquire the lock BEFORE reading the value. Use `select_for_update()` within `transaction.atomic()` for DB-backed resources, or Redis lock before Redis reads
- Key format: `{service}:{resource_type}:{resource_id}` (e.g. `tas:task:12345`)

**Pattern: Lock with no TTL**
- Symptom: Service hangs indefinitely; workers stop processing
- Root cause: Redis lock acquired with TTL=None — if the process dies, lock is never released
- Fix: Always set a TTL (typically 30–120 seconds). Use `nx=True, ex=<ttl>` in redis-py

**Pattern: Too-broad lock key**
- Symptom: Throughput drops during high load even though operations are unrelated
- Root cause: Lock key is too coarse (e.g. `lock:all_tasks` instead of `lock:task:{id}`)
- Fix: Make the lock key as specific as possible — lock on the specific resource ID

## Django / Database Issues

**Pattern: bulk_create doesn't fire signals**
- Symptom: Post-create logic (notifications, downstream triggers) doesn't run for bulk-inserted records
- Root cause: Django's `bulk_create()` does not call `Model.save()` and therefore does not fire `post_save` signals
- Fix: Either loop with individual `.save()` (acceptable for small counts), or manually trigger the downstream logic after bulk_create, or use `update_or_create` with explicit logic

**Pattern: N+1 queries in DRF serializers**
- Symptom: Endpoint is slow; Django Debug Toolbar shows 50+ identical queries
- Root cause: Serializer accesses a related object in a loop without prefetching
- Fix: Add `select_related('field')` or `prefetch_related('related_set')` in the view's queryset. Check with `django.db.connection.queries` in tests

**Pattern: Migration not applied in staging/prod**
- Symptom: `OperationalError: table has no column named X`
- Root cause: Migration file exists but was not run; or circular migration dependency
- Fix: `poetry run python manage.py showmigrations` to see state; `migrate` to apply

**Pattern: select_for_update outside transaction**
- Symptom: `TransactionManagementError: SELECT FOR UPDATE cannot be used outside of a transaction`
- Root cause: `select_for_update()` called without wrapping `transaction.atomic()`
- Fix: Wrap the block in `with transaction.atomic():`

## Celery / Async Issues

**Pattern: Task retry storm**
- Symptom: Queue depth grows; CPU spikes on workers; same task processed many times
- Root cause: Task raises exception → Celery retries with no backoff → cascades
- Fix: Use `self.retry(exc=exc, countdown=2**self.request.retries, max_retries=5)` for exponential backoff

**Pattern: apply_async in request cycle**
- Symptom: API response is slow; tasks appear delayed
- Root cause: `task.apply_async()` called synchronously in the Django view, blocking on broker connection
- Fix: Use `task.delay()` which is non-blocking, or ensure the broker connection is healthy

**Pattern: Task not idempotent**
- Symptom: Duplicate records or side effects on retry
- Root cause: Task performs writes without checking if already processed
- Fix: Add idempotency check at the start of the task (e.g. check if record already exists before creating)

## Kinesis / Event Streaming

**Pattern: Consumer lag accumulating**
- Symptom: Events processed with increasing delay; CloudWatch `IteratorAgeMilliseconds` rising
- Root causes:
  1. Consumer is too slow — processing takes longer than the record arrival rate
  2. Shard is hot — too many records on one shard key
  3. Consumer is erroring and retrying indefinitely
- Fix: Check consumer logs for errors first. If no errors, check throughput per shard. Consider increasing shard count or parallelizing consumers

**Pattern: Duplicate event processing**
- Symptom: Same event processed multiple times
- Root cause: Kinesis delivers at-least-once; consumer doesn't checkpoint correctly, or process restarts before checkpoint
- Fix: Make consumer handlers idempotent. Use the sequence number as an idempotency key

## Frontend (React)

**Pattern: Stale closure in useEffect**
- Symptom: Effect uses an old value of a variable; state updates don't reflect in the effect
- Root cause: Variable captured in closure at render time; not in dependency array
- Fix: Add the variable to the dependency array, or use `useRef` for values you want to read without re-triggering the effect

**Pattern: MUI style overrides not applying**
- Symptom: Custom styles don't appear despite being set
- Root cause: Specificity issue — MUI's generated class names have higher specificity
- Fix: Use `sx` prop for one-off styles, or `styled()` with `shouldForwardProp`; avoid bare CSS class overrides
