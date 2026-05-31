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

## License

MIT — see [LICENSE](LICENSE).
