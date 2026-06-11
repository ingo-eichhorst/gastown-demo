# gastown-demo

[![CI](https://github.com/ingo-eichhorst/gastown-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/ingo-eichhorst/gastown-demo/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/gastown-demo.svg)](https://pypi.org/project/gastown-demo/)
[![PyPI downloads](https://img.shields.io/pypi/dm/gastown-demo.svg)](https://pypi.org/project/gastown-demo/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A task manager you can start using in 30 seconds, right from your terminal.

`gtdemo` keeps a todo list in a plain JSON file — no account, no cloud, no friction. Type a task, check it off, move on.

It's also the demo codebase for the [Gas Town](https://github.com/universalagents/gastown) talk: small enough to read in 10 minutes, structured so AI coding agents can add features one at a time, with tests and quality gates already wired up.

---

## Willkommen, betterCode()-Teilnehmer!

Schön, dass ihr hier seid! Dieses Repository ist das Demo-Projekt zum Gas-Town-Vortrag auf der betterCode() Konferenz — ihr habt live verfolgt, wie KI-Agenten es Stück für Stück weiterentwickeln.

**Was euch erwartet:** `gastown-demo` ist bewusst klein gehalten: ein schlichter Aufgaben-Manager für die Kommandozeile, den ihr in zehn Minuten vollständig lesen könnt. Genau das macht ihn zum idealen Spielplatz für autonome Coding-Agenten. Das **Gas Town**-System zerlegt Features in Issues (sogenannte Beads), weist sie koordinierten Polecat-Agenten zu und führt ihre Änderungen über eine Merge Queue zusammen — alles ohne manuellen Eingriff.

**So könnt ihr selbst experimentieren:**

1. **Repository klonen** und die Commit-Historie erkunden — jeder Commit stammt von einem Agenten.
2. **`gtdemo` installieren** (s. Quickstart unten) und die Befehle direkt ausprobieren.
3. **Ein eigenes Feature einbauen** nach dem Drei-Schritt-Muster im Abschnitt *Architecture* — `reopen_task()` dient als Referenz-Implementierung.
4. **Gas Town selbst erkunden:** [github.com/universalagents/gastown](https://github.com/universalagents/gastown)

Viel Spaß beim Stöbern und Ausprobieren!

---

## Quickstart

**Install** (Python 3.10+ required):

```bash
pip install -e ".[dev]"
```

This creates the `gtdemo` command in your current environment.

**Try it:**

```
$ gtdemo add "write the slides"
added #1: write the slides

$ gtdemo add "rehearse the talk"
added #2: rehearse the talk

$ gtdemo list
[ ] #1 write the slides
[ ] #2 rehearse the talk

$ gtdemo done 1
completed #1: write the slides

$ gtdemo list
[x] #1 write the slides
[ ] #2 rehearse the talk

$ gtdemo reopen 1
reopened #1: write the slides
```

---

## Commands

| Command | What it does |
|---------|-------------|
| `gtdemo add "your task"` | Add a new task |
| `gtdemo list` | Show all tasks (open and done) |
| `gtdemo done <id>` | Mark a task as completed |
| `gtdemo reopen <id>` | Reopen a completed task |
| `gtdemo --version` | Show the installed version |

---

## Where tasks are stored

Tasks are saved to `tasks.json` in the current directory. To use a different file, set the `GTDEMO_STORE` environment variable:

```bash
GTDEMO_STORE=~/work/tasks.json gtdemo list
```

This works per-project: `cd` into a folder and run `gtdemo` — each folder gets its own task list.

---

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

---

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

---

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

---

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

---

## License

MIT — see [LICENSE](LICENSE).
