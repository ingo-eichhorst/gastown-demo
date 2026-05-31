# gastown-demo

A tiny, extensible task-manager CLI. It is the **demo app for the Gas Town talk**:
small enough to read in a minute, structured so that coding agents can pick up
features one at a time, with tests and quality gates already in place.

## Install

```bash
pip install -e ".[dev]"
```

## Use

```bash
gtdemo add "write the slides"
gtdemo add "rehearse the talk"
gtdemo list
gtdemo done 1
gtdemo list
```

Tasks are stored in `tasks.json` in the current directory. Override the location
with the `GTDEMO_STORE` environment variable.

## Develop

```bash
ruff check .     # lint
pytest -q        # tests
```

CI runs both on every push and pull request (see `.github/workflows/ci.yml`),
so every change has to pass the same quality gates an agent would.

## Structure

```
src/gastown_demo/
  core.py   # pure task logic + JSON store (well covered by tests)
  cli.py    # thin argparse layer that calls into core
tests/
  test_core.py
  test_cli.py
```

The split is deliberate: business logic lives in `core` as pure functions, the
CLI stays a thin shell. New behaviour is added by writing a function in `core`
(with a test) and wiring a subcommand in `cli.build_parser`.

## Ideas to extend (good first beads)

- `done`-state already exists; add a `reopen` command
- `remove <id>` to delete a task
- priorities (`--priority high`) and sort `list` by them
- due dates and an `overdue` view
- tags and `gtdemo list --tag <name>`
- `search <text>` across titles
- export to Markdown
- colourised output

## Contributing

### Report an issue

Open a GitHub issue with a short description of the bug or feature request.
Include the output of `gtdemo list` if relevant.

### Set up for development

```bash
git clone <repo-url>
cd gastown-demo
pip install -e ".[dev]"
```

### Run tests locally

```bash
ruff check .   # lint
pytest -q      # tests
```

Both gates must pass before submitting a pull request — CI enforces the same
checks on every push.

### Open a pull request

1. Fork the repo and create a branch (`git checkout -b my-feature`).
2. Make your changes with tests where appropriate.
3. Run `ruff check .` and `pytest -q` and confirm both pass.
4. Open a pull request against `main` with a clear description of what changed
   and why.

## License

MIT — see [LICENSE](LICENSE).
