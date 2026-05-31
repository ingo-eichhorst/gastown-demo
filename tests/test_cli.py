from gastown_demo.cli import main


def test_add_then_list(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("GTDEMO_STORE", str(tmp_path / "tasks.json"))
    assert main(["add", "first task"]) == 0
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "first task" in out


def test_done_marks_task(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("GTDEMO_STORE", str(tmp_path / "tasks.json"))
    main(["add", "ship it"])
    main(["done", "1"])
    main(["list"])
    out = capsys.readouterr().out
    assert "[x] #1 ship it" in out
