from pathlib import Path

import pytest

from gastown_demo.core import Task, add_task, complete_task, load_tasks, reopen_task, save_tasks


def test_add_task_assigns_incrementing_ids():
    tasks: list[Task] = []
    first = add_task(tasks, "write slides")
    second = add_task(tasks, "rehearse talk")
    assert (first.id, second.id) == (1, 2)
    assert len(tasks) == 2


def test_add_task_rejects_empty_title():
    with pytest.raises(ValueError):
        add_task([], "   ")


def test_complete_task_sets_done():
    tasks = [Task(id=1, title="demo")]
    complete_task(tasks, 1)
    assert tasks[0].done is True


def test_complete_unknown_task_raises():
    with pytest.raises(KeyError):
        complete_task([], 99)


def test_reopen_task_clears_done():
    tasks = [Task(id=1, title="demo", done=True)]
    reopen_task(tasks, 1)
    assert tasks[0].done is False


def test_reopen_unknown_task_raises():
    with pytest.raises(KeyError):
        reopen_task([], 99)


def test_save_and_load_roundtrip(tmp_path: Path):
    store = tmp_path / "tasks.json"
    tasks = [Task(id=1, title="a"), Task(id=2, title="b", done=True)]
    save_tasks(store, tasks)
    assert load_tasks(store) == tasks


def test_load_missing_file_returns_empty(tmp_path: Path):
    assert load_tasks(tmp_path / "nope.json") == []
