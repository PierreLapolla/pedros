# Contributing

Contributions are welcome! To set up a dev environment:

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/pierrelapolla/pedros.git
   cd pedros
   uv sync --group dev --group docs
   ```
3. Install the pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```
4. Run the test suite:
   ```bash
   uv run pytest
   ```
5. Preview the docs locally:
   ```bash
   uv run --group docs zensical serve
   ```

Before opening a pull request, run the hooks against the full tree:
```bash
uv run pre-commit run --all-files
```
