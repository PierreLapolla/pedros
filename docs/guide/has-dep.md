---
icon: lucide/package-search
---

# Dependency checks

`has_dep` checks whether an optional dependency is importable, with an
optional version constraint. It's what `progbar` and `setup_logging` use
internally to pick a backend, and it's available for your own code too.

```python
from pedros import has_dep

if has_dep("rich"):
    ...

if has_dep("rich", ">=13.0"):
    ...

if has_dep("tqdm", ">=4.60,<5"):
    ...
```

Supported operators: `==`, `!=`, `>=`, `>`, `<=`, `<`. Multiple
comma-separated clauses are combined with AND, e.g. `">=4.60,<5"`.

Returns `False` if the module can't be imported or, when a version
constraint is given, if the installed version doesn't satisfy it.
