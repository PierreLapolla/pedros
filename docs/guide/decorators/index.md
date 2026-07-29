---
icon: lucide/at-sign
---

# Decorators

pedros ships four ready-to-use decorators, all built on
[`wrapt`](https://pypi.org/project/wrapt/) so they preserve signatures and
work transparently on sync and async functions, used bare (`@timed`) or
configured (`@timed(...)`):

- [`@timed`](timed.md): logs how long a function took to run
- [`@safe`](safe.md): wraps a function in a try/except, with logging,
  callbacks, and optional re-raising
- [`@trace`](trace.md): logs a function's arguments, return value, or raised
  exception, without ever suppressing the exception
- [`@monitor`](monitor.md): combines all three above with their defaults,
  no configuration of its own

Writing your own decorator with the same sync/async-safe shape? See
[the universal decorator template](universal-decorator.md) — it's the
annotated skeleton `@timed`, `@safe`, and `@trace` are all built from. It's
not part of the public API, so it's linked here rather than in the main
nav.
