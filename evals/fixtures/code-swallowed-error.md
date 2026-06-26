# Fixture: Code Swallowed Error

## Artifact type

code

## Input

```python
def sync_record(client, record):
    try:
        client.send(record)
    except Exception:
        pass
    return True
```

## Expected decision

reject

## Expected confidence

high

## Required findings

- Blocker: swallowed failure.
- Blocker: caller receives success even when sync fails.
- Required fix: preserve the error cause and return or raise an accurate failure signal.
