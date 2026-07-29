---
icon: lucide/timer
---

# `@timed`

Logs how long a function took to run.

```python
import time
from pedros import timed


@timed
def long_running_func(sleep_time: float):
    time.sleep(sleep_time)


long_running_func(0.001)
# Logs (DEBUG): "long_running_func took 1.23 ms to execute."
```

The duration is formatted with an appropriate unit: nanoseconds,
microseconds, milliseconds, seconds, or `hh:mm:ss` for anything over a
minute.

## Options

- `log_level`: level used to report the duration, or `"NONE"` to time
  silently without logging (default: `"DEBUG"`)

`@timed` logs at `DEBUG` by default, which stays silent unless you've
raised `pedros`'s verbosity, see the
[logging guide](../logging.md#pedross-own-logging):

```python
@timed(log_level="INFO")
def process_data():
    return "result"
```
