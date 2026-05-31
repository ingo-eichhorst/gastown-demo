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

- `done`-state already exists; add a `reopen` command — already implemented: see `reopen_task()` in `core.py` and `cmd_reopen()` in `cli.py`; study these as the pattern for adding new commands
- `remove <id>` to delete a task — add `remove_task()` in `core.py` (modelled on `complete_task()`), then wire `cmd_remove()` and a `remove` subparser in `cli.build_parser()`
- priorities (`--priority high`) and sort `list` by them — add a `priority` field to the `Task` dataclass in `core.py`, update `add_task()` to accept it, and sort by priority in `cmd_list()` in `cli.py`
- due dates and an `overdue` view — add a `due` field to the `Task` dataclass in `core.py`; add an `overdue_tasks()` filter there, then wire an `overdue` subparser in `cli.build_parser()`
- tags and `gtdemo list --tag <name>` — add a `tags: list[str]` field to `Task` in `core.py`; filter by tag in `cmd_list()` and add a `--tag` argument to the `list` subparser in `cli.build_parser()`
- `search <text>` across titles — add `search_tasks()` in `core.py` (substring match on `task.title`), then wire `cmd_search()` and a `search` subparser in `cli.build_parser()`
- export to Markdown — add `export_markdown()` in `core.py`, then wire `cmd_export()` and an `export` subparser in `cli.build_parser()`
- colourised output — modify `cmd_list()` in `cli.py` to wrap output in ANSI codes or add `colorama` as a dependency; no changes to `core.py` needed

## License

MIT — see [LICENSE](LICENSE).
