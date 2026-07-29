# Pedros

[![PyPI](https://img.shields.io/pypi/v/pedros)](https://pypi.org/project/pedros/)

A small package of reusable Python utilities for Python projects.

## Features

- **Dependency Management**: Smart detection of optional dependencies (rich, tqdm)
- **Logging**: Simplified logging setup with optional Rich support
- **Progress Bars**: Unified progress bar API with multiple backends
- **Decorators**: Robust decorators for timing (`@timed`), error handling (`@safe`), and call tracing (`@trace`), or all combined with `@monitor`
- **Type Safe**: Comprehensive type hints and PEP 561 compliance

## Installation

```bash
pip install pedros
```

OR

```bash
uv add pedros
```

`rich` and `tqdm` are optional and auto-detected at runtime. Install either
yourself to get the enhanced logging/progress-bar backend.

## Documentation

[pierrelapolla.github.io/pedros](https://pierrelapolla.github.io/pedros/) —
a Guide page per feature with runnable examples, plus a single API
Reference page listing every public signature.

## License

This project is licensed under the MIT [License](LICENSE).

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for dev
environment setup.

## Support

For questions or support, please open a GitHub issue.
