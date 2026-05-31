"""Core task logic.

Pure functions plus a small JSON store. Kept deliberately simple so the demo
can be grown one feature at a time (priorities, due dates, tags, search ...).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Task:
    """A single task."""

    id: int
    title: str
    done: bool = False


def add_task(tasks: list[Task], title: str) -> Task:
    """Append a new task with the next free id. Returns the created task."""
    title = title.strip()
    if not title:
        raise ValueError("task title must not be empty")
    next_id = max((t.id for t in tasks), default=0) + 1
    task = Task(id=next_id, title=title)
    tasks.append(task)
    return task


def complete_task(tasks: list[Task], task_id: int) -> Task:
    """Mark the task with the given id as done. Raises KeyError if not found."""
    for task in tasks:
        if task.id == task_id:
            task.done = True
            return task
    raise KeyError(f"no task with id {task_id}")


def load_tasks(path: Path) -> list[Task]:
    """Load tasks from a JSON file. Returns an empty list if the file is absent."""
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Task(**item) for item in data]


def save_tasks(path: Path, tasks: list[Task]) -> None:
    """Persist tasks to a JSON file."""
    path.write_text(
        json.dumps([asdict(t) for t in tasks], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
