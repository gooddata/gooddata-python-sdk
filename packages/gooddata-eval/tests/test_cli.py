# (C) 2026 GoodData Corporation
import httpx
import orjson
import pytest
from gooddata_eval.cli import main as cli_main
from gooddata_eval.core.connection import (
    ConnectionError_,  # noqa: F401 - used in test_cli_operational_error_exits_nonzero
)
from gooddata_eval.core.models import DatasetItem
from gooddata_eval.core.runner import EvalReport, ItemReport
from gooddata_eval.core.workspace import ResolvedModel
from rich.console import Console


def test_build_run_config_rejects_both_sources():
    with pytest.raises(SystemExit):
        cli_main.parse_args(["run", "--host", "h", "--workspace", "w", "--dataset", "d", "--langfuse-dataset", "ds"])


def test_build_run_config_requires_a_source():
    with pytest.raises(SystemExit):
        cli_main.parse_args(["run", "--host", "h", "--workspace", "w"])


def test_cli_run_end_to_end(monkeypatch, tmp_path, fixtures_dir):
    # Stub connection + model activation + chat backend so no network is needed.
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _FakeController:
        def __init__(self, *a, **k): ...
        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(
                provider_id="prov", model_id=requested or "gpt-5.2", switched=False, provider_name="Test Provider"
            )

        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)

    def _fake_run(
        items,
        backend,
        *,
        runs,
        model,
        workspace_id,
        on_item_start=None,
        on_run_done=None,
        on_item_done=None,
        on_langfuse_item_done=None,
    ):
        return EvalReport(
            model=model,
            workspace_id=workspace_id,
            items=[
                ItemReport(
                    id="acme-001",
                    dataset_name="acme_q1_pilot",
                    test_kind="visualization",
                    question="q",
                    pass_at_k=True,
                    runs=runs,
                )
            ],
        )

    monkeypatch.setattr(cli_main, "run_items", _fake_run)
    monkeypatch.setattr(cli_main, "ChatClient", lambda **k: object())

    out = tmp_path / "res.json"
    exit_code = cli_main.main(
        [
            "run",
            "--host",
            "https://h",
            "--token",
            "tok",
            "--workspace",
            "ws1",
            "--dataset",
            str(fixtures_dir / "sample_dataset"),
            "--json",
            str(out),
        ]
    )
    assert exit_code == 0
    assert orjson.loads(out.read_bytes())["summary"]["passed"] == 1


def test_cli_operational_error_exits_nonzero(monkeypatch, fixtures_dir):
    def _boom(host, token, profile):
        raise ConnectionError_("Missing token.")

    monkeypatch.setattr(cli_main, "resolve_connection", _boom)
    exit_code = cli_main.main(
        ["run", "--host", "https://h", "--workspace", "ws1", "--dataset", str(fixtures_dir / "sample_dataset")]
    )
    assert exit_code == 2


def test_cli_http_error_exits_nonzero(monkeypatch, fixtures_dir):
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _BoomController:
        def __init__(self, *a, **k): ...
        def resolve_and_activate(self, requested, provider=None):
            raise httpx.HTTPError("401 unauthorized")

        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _BoomController)
    exit_code = cli_main.main(
        [
            "run",
            "--host",
            "https://h",
            "--token",
            "tok",
            "--workspace",
            "ws1",
            "--dataset",
            str(fixtures_dir / "sample_dataset"),
        ]
    )
    assert exit_code == 2


def test_cli_warns_on_skipped_kinds(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _FakeController:
        def __init__(self, *a, **k): ...
        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="prov", model_id="gpt-5.2", switched=False, provider_name="Test Provider")

        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)
    monkeypatch.setattr(cli_main, "ChatClient", lambda **k: object())
    monkeypatch.setattr(cli_main, "load_local_dataset", lambda folder: [])

    def _fake_run(
        items,
        backend,
        *,
        runs,
        model,
        workspace_id,
        on_item_start=None,
        on_run_done=None,
        on_item_done=None,
        on_langfuse_item_done=None,
    ):
        return EvalReport(
            model=model,
            workspace_id=workspace_id,
            items=[ItemReport(id="s1", dataset_name="d", test_kind="metric_skill", question="q", skipped=True)],
        )

    monkeypatch.setattr(cli_main, "run_items", _fake_run)
    exit_code = cli_main.main(
        ["run", "--host", "https://h", "--token", "tok", "--workspace", "ws1", "--dataset", str(tmp_path)]
    )
    assert exit_code == 0
    err = capsys.readouterr().err
    assert "metric_skill" in err and "skipped" in err


def test_make_progress_callbacks_emit_status_and_run_lines():
    console = Console(record=True, width=100)
    on_start, on_run, on_done = cli_main._make_progress_callbacks(console)
    item = DatasetItem(
        id="i1", dataset_name="d", test_kind="visualization", question="Show revenue", expected_output={}
    )
    on_start(1, 2, item)
    on_run(1, 2, 1, 2, True, 1.23)
    on_done(
        1,
        2,
        ItemReport(
            id="i1",
            dataset_name="d",
            test_kind="visualization",
            question="Show revenue",
            pass_at_k=True,
            runs=2,
            latency_s=2.5,
        ),
    )
    text = console.export_text()
    assert "1/2" in text
    assert "i1" in text
    assert "PASS" in text
    assert "run 1/2" in text
    assert "1.23s" in text  # per-run latency
    assert "1.25s" in text  # item avg latency (2.5s / 2 runs)


def test_cli_langfuse_without_langfuse_dataset_exits_with_error(monkeypatch, fixtures_dir):
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _FakeController:
        def __init__(self, *a, **k): ...
        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="p", model_id="gpt-5.2", switched=False, provider_name="P")

        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)
    exit_code = cli_main.main(
        [
            "run",
            "--host",
            "https://h",
            "--token",
            "tok",
            "--workspace",
            "ws1",
            "--dataset",
            str(fixtures_dir / "sample_dataset"),
            "--langfuse",
        ]
    )
    assert exit_code == 2


def test_cli_langfuse_sink_called_per_item(monkeypatch, fixtures_dir):
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _FakeController:
        def __init__(self, *a, **k): ...
        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="p", model_id="gpt-5.2", switched=False, provider_name="P")

        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)
    monkeypatch.setattr(cli_main, "ChatClient", lambda **k: object())
    monkeypatch.setattr(cli_main, "_load_dataset", lambda config: [])

    langfuse_calls: list = []

    class _FakeSink:
        def __init__(self, dataset_name, run_name): ...
        def log_item(self, report, *, dataset_item_id):
            langfuse_calls.append(dataset_item_id)

    monkeypatch.setattr(cli_main, "LangfuseSink", _FakeSink)

    def _fake_run(
        items,
        backend,
        *,
        runs,
        model,
        workspace_id,
        on_item_start=None,
        on_run_done=None,
        on_item_done=None,
        on_langfuse_item_done=None,
    ):
        r = EvalReport(model=model, workspace_id=workspace_id)
        item_report = ItemReport(
            id="acme-001", dataset_name="d", test_kind="visualization", question="q", pass_at_k=True, runs=1
        )
        r.items.append(item_report)
        if on_langfuse_item_done:
            on_langfuse_item_done(1, 1, item_report)
        return r

    monkeypatch.setattr(cli_main, "run_items", _fake_run)

    exit_code = cli_main.main(
        [
            "run",
            "--host",
            "https://h",
            "--token",
            "tok",
            "--workspace",
            "ws1",
            "--langfuse-dataset",
            "my_dataset",
            "--langfuse",
        ]
    )
    assert exit_code == 0
    assert langfuse_calls == ["acme-001"]
