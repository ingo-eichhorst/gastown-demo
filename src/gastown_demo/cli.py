"""Command-line interface for gastown-demo.

The CLI stays thin: it parses arguments, calls the pure functions in `core`,
and prints the result. New subcommands slot in via `build_parser`.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from . import __version__
from .core import add_task, complete_task, load_tasks, reopen_task, save_tasks


def default_store() -> Path:
    """Where tasks are persisted. Override with the GTDEMO_STORE env var."""
    return Path(os.environ.get("GTDEMO_STORE", "tasks.json"))


def cmd_add(args: argparse.Namespace) -> int:
    store = default_store()
    tasks = load_tasks(store)
    task = add_task(tasks, args.title)
    save_tasks(store, tasks)
    print(f"added #{task.id}: {task.title}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    store = default_store()
    tasks = load_tasks(store)
    if not tasks:
        print('no tasks yet — add one with: gtdemo add "..."')
        return 0
    for task in tasks:
        mark = "x" if task.done else " "
        print(f"[{mark}] #{task.id} {task.title}")
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    store = default_store()
    tasks = load_tasks(store)
    task = complete_task(tasks, args.id)
    save_tasks(store, tasks)
    print(f"completed #{task.id}: {task.title}")
    return 0


def cmd_reopen(args: argparse.Namespace) -> int:
    store = default_store()
    tasks = load_tasks(store)
    task = reopen_task(tasks, args.id)
    save_tasks(store, tasks)
    print(f"reopened #{task.id}: {task.title}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gtdemo", description="A tiny task-manager CLI.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("title", help="the task title")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list all tasks")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="mark a task as done")
    p_done.add_argument("id", type=int, help="the task id")
    p_done.set_defaults(func=cmd_done)

    p_reopen = sub.add_parser("reopen", help="reopen a completed task")
    p_reopen.add_argument("id", type=int, help="the task id")
    p_reopen.set_defaults(func=cmd_reopen)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
