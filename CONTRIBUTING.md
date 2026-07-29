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

## Docs structure

The site follows [Diátaxis](https://diataxis.fr/): **Get Started**
(`docs/index.md`) is the only tutorial page, **Guide** (`docs/guide/`) is
how-to content — one page per feature, real code first, options as a bullet
list, no filler sections — and **API Reference** (`docs/reference.md`) is a
flat, hand-maintained list of every public signature. Keep new pages in
whichever bucket matches; don't blend tutorial prose into a guide page or
vice versa.

Writing a new decorator with the same sync/async-safe shape as `@timed`,
`@safe`, and `@trace`? Start from
`docs/guide/decorators/universal-decorator.md` — it's the annotated
skeleton, not part of the public API, so it's excluded from the site nav.
