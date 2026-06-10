# gastown-demo

[![PyPI version](https://img.shields.io/pypi/v/gastown-demo.svg)](https://pypi.org/project/gastown-demo/)
[![PyPI downloads](https://img.shields.io/pypi/dm/gastown-demo.svg)](https://pypi.org/project/gastown-demo/)
[![Python versions](https://img.shields.io/pypi/pyversions/gastown-demo.svg)](https://pypi.org/project/gastown-demo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/ingo-eichhorst/gastown-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/ingo-eichhorst/gastown-demo/actions/workflows/ci.yml)

A tiny, extensible task-manager CLI — demo app for the Gas Town talk. Small
enough to read in 10 minutes, structured so coding agents can add features
one at a time, with tests and quality gates already in place.

## Install

```bash
pip install -e ".[dev]"
```

Requires Python 3.10+. Creates the `gtdemo` entry point in your environment.

## Use

```bash
gtdemo add "write the slides"
gtdemo add "rehearse the talk"
gtdemo list
gtdemo done 1
gtdemo reopen 1
gtdemo list
```

Tasks are stored in `tasks.json` in the current directory. Override the
location with the `GTDEMO_STORE` environment variable:

```bash
GTDEMO_STORE=/tmp/my-tasks.json gtdemo list
```

## Architecture

The codebase has two layers kept deliberately separate:

```
src/gastown_demo/
  core.py   # pure task logic + JSON store — no I/O except the store file
  cli.py    # argparse layer; calls core, prints output, returns exit codes
tests/
  test_core.py   # unit tests for pure functions
  test_cli.py    # integration tests driven through main()
```

**Data model.** `core.Task` is the only domain object:

```python
@dataclass
class Task:
    id: int
    title: str
    done: bool = False
```

All business logic in `core.py` operates on `list[Task]` using pure functions.
The CLI in `cli.py` loads from disk, delegates to a core function, saves, and
prints — nothing more.

**Extension pattern.** Every new command follows three steps:

1. Add a function to `core.py` that takes `list[Task]` and returns or raises
2. Cover it with tests in `test_core.py`
3. Add a `cmd_*` handler and a `sub.add_parser(...)` block in `cli.py`

`reopen_task()` / `cmd_reopen()` is the reference implementation — study it
before adding your first command.

**Data flow:**

```
GTDEMO_STORE env var
       │
       ▼
load_tasks(path)          # JSON → list[Task]
       │
       ▼
core function             # pure: list[Task] → list[Task] or Task
       │
       ▼
save_tasks(path, tasks)   # list[Task] → JSON
       │
       ▼
print(...)                # CLI output
```

## Develop

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Lint
ruff check .

# Format (auto-fix)
ruff format .

# Tests
pytest -q

# Fail fast, short tracebacks
pytest -q --tb=short -x
```

CI (`.github/workflows/ci.yml`) runs `ruff check` then `pytest -q` on every
push and pull request. Both must pass before merging.

## Ideas to extend

Good first contributions — each follows the three-step extension pattern above:

| Feature | `core.py` change | `cli.py` change |
|---------|-----------------|-----------------|
| `remove <id>` | `remove_task()` modelled on `complete_task()` | `cmd_remove()` + `remove` subparser |
| `--priority high` | add `priority` field to `Task`; update `add_task()` | `--priority` arg on `add`; sort in `cmd_list()` |
| Due dates + `overdue` | add `due` field to `Task`; add `overdue_tasks()` filter | `overdue` subparser |
| Tags + `list --tag` | add `tags: list[str]` to `Task` | `--tag` arg on `list` subparser |
| `search <text>` | `search_tasks()` substring match on `task.title` | `search` subparser |
| Markdown export | `export_markdown()` returns a string | `export` subparser; print to stdout |
| Coloured output | no change | wrap output in ANSI codes in `cmd_list()` |

Already implemented: `reopen` — see `reopen_task()` in `core.py` and
`cmd_reopen()` in `cli.py`.

## Contributing

### Set up

```bash
git clone <repo-url>
cd gastown-demo
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Workflow

1. Create a branch: `git checkout -b my-feature`
2. Implement — follow the three-step extension pattern above
3. Add tests in `tests/` (required for new `core.py` functions)
4. Run `ruff check . && pytest -q` — both must pass
5. Open a pull request against `main` with a description of what changed and why

### Code conventions

- `ruff` enforces style; run `ruff format .` to auto-format
- Line length: 100 characters (set in `pyproject.toml`)
- Core functions take a `list[Task]` as the first argument; no `print` in `core.py`
- New functions get a single-line docstring matching the existing style
- CLI handlers return `int` exit codes (0 = success)

### Filing bugs

Open a GitHub issue with the output of `gtdemo list` if relevant.

## License

MIT — see [LICENSE](LICENSE).
