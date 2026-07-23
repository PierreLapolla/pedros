---
icon: lucide/timer
---

# Decorators

pedros ships two ready-to-use decorators, both built on
[`wrapt`](https://pypi.org/project/wrapt/) so they preserve signatures and
work transparently on sync and async functions, used bare (`@timed`) or
configured (`@timed(...)`):

- [`@timed`](timed.md) — logs how long a function took to run
- [`@safe`](safe.md) — wraps a function in a try/except, with logging,
  callbacks, and optional re-raising

If you need a decorator with the same sync/async-safe shape but different
behavior, start from [the universal decorator](universal-decorator.md) — it's
the annotated skeleton both `@timed` and `@safe` are built from.
