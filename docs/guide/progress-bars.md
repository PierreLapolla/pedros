---
icon: lucide/loader-circle
---

# Progress bars

`progbar` wraps an iterable with a progress bar, picking a backend
automatically so your code doesn't need to know which progress bar library is
installed.

## Basic usage

```python
import time
from pedros import progbar

for _ in progbar(range(10), desc="Processing"):
    time.sleep(0.1)
```

## Backend selection

The `backend` argument controls which library renders the bar:

- `"auto"` (default): use `rich` if installed, else `tqdm`, else no bar
- `"rich"`: force the [`rich.progress`](https://rich.readthedocs.io/en/stable/progress.html) backend
- `"tqdm"`: force the [`tqdm`](https://pypi.org/project/tqdm/) backend
- `"none"`: disable the bar and return the original iterable unmodified

```python
for _ in progbar(range(10), backend="tqdm", desc="Downloading"):
    ...

for _ in progbar(range(10), backend="none"):
    ...  # plain iteration, no progress bar
```

If an explicitly requested backend isn't installed, `progbar` logs a warning
and falls back to whichever backend is available (or none).

## Keyword arguments

Extra `*args`/`**kwargs` are forwarded to the underlying backend. `desc` and
`description` are interchangeable — `progbar` normalizes whichever one you
pass to the name the chosen backend expects:

```python
progbar(range(10), desc="Processing")       # works with tqdm
progbar(range(10), description="Processing")  # works with rich
```

## Installing a backend

```bash
pip install "pedros[rich]"   # rich backend
pip install "pedros[all]"    # all optional backends
```
