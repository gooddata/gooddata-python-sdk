# (C) 2026 GoodData Corporation
import io
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import orjson
import pytest
from gooddata_eval.cli import main as cli_main
from gooddata_eval.cli.main import _parse_model_arg
from gooddata_eval.core.config import JUDGE_MODEL_ENV_VAR, RunConfig, judge_model
from gooddata_eval.core.connection import (
    ConnectionError_,  # noqa: F401 - used in test_cli_operational_error_exits_nonzero
)
from gooddata_eval.core.models import DatasetItem
from gooddata_eval.core.runner import EvalReport, ItemReport
from gooddata_eval.core.timing import TIMERS_ENV_VAR, timers_enabled
from gooddata_eval.core.workspace import ActiveLlmProvider, ResolvedModel
from rich.console import Console


def test_build_run_config_rejects_both_sources():
    with pytest.raises(SystemExit):
        cli_main.parse_args(["run", "--host", "h", "--workspace", "w", "--dataset", "d", "--langfuse-dataset", "ds"])


def test_build_run_config_requires_a_source():
    with pytest.raises(SystemExit):
        cli_main.parse_args(["run", "--host", "h", "--workspace", "w"])


def test_parse_args_agent_id_flag():
    args = cli_main.parse_args(["run", "--host", "h", "--workspace", "w", "--dataset", "d", "--agent-id", "agent-1"])
    assert args.agent_id == "agent-1"


def test_parse_args_agent_id_defaults_to_none():
    args = cli_main.parse_args(["run", "--host", "h", "--workspace", "w", "--dataset", "d"])
    assert args.agent_id is None


def test_cli_run_end_to_end(monkeypatch, tmp_path, fixtures_dir):
    # Stub connection + model activation + chat backend so no network is needed.
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _FakeController:
        def __init__(self, *a, **k): ...
        def get_active(self):
            return ActiveLlmProvider(provider_id="prov", default_model_id="gpt-5.2")

        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(
                provider_id="prov", model_id=requested or "gpt-5.2", switched=False, provider_name="Test Provider"
            )

        def restore(self, original): ...
        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)

    def _fake_run(
        items,
        backend,
        *,
        runs,
        model,
        workspace_id,
        **kw,
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
    # run keys are provider-prefixed (provider_name/model) to stay collision-free across providers
    assert orjson.loads(out.read_bytes())["runs"]["Test Provider/gpt-5.2"]["summary"]["passed"] == 1


def _stub_run_for_agent_id_test(monkeypatch, seen_chat_client_kwargs):
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _FakeController:
        def __init__(self, *a, **k): ...
        def get_active(self):
            return ActiveLlmProvider(provider_id="prov", default_model_id="gpt-5.2")

        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(
                provider_id="prov", model_id=requested or "gpt-5.2", switched=False, provider_name="Test Provider"
            )

        def restore(self, original): ...
        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)

    def _fake_run(items, backend, *, runs, model, workspace_id, **kw):
        return EvalReport(model=model, workspace_id=workspace_id, items=[])

    monkeypatch.setattr(cli_main, "run_items", _fake_run)

    def _spy_chat_client(**kwargs):
        seen_chat_client_kwargs.update(kwargs)
        return object()

    monkeypatch.setattr(cli_main, "ChatClient", _spy_chat_client)


def test_cli_run_passes_agent_id_flag_to_chat_client(monkeypatch, tmp_path, fixtures_dir):
    seen = {}
    _stub_run_for_agent_id_test(monkeypatch, seen)
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
            "--agent-id",
            "agent-1",
            "--json",
            str(tmp_path / "res.json"),
        ]
    )
    assert exit_code == 0
    assert seen["agent_id"] == "agent-1"


def test_cli_run_falls_back_to_agent_id_env_var(monkeypatch, tmp_path, fixtures_dir):
    monkeypatch.setenv("GD_EVAL_AGENT_ID", "agent-from-env")
    seen = {}
    _stub_run_for_agent_id_test(monkeypatch, seen)
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
            str(tmp_path / "res.json"),
        ]
    )
    assert exit_code == 0
    assert seen["agent_id"] == "agent-from-env"


def test_cli_run_agent_id_omitted_when_unset(monkeypatch, tmp_path, fixtures_dir):
    monkeypatch.delenv("GD_EVAL_AGENT_ID", raising=False)
    seen = {}
    _stub_run_for_agent_id_test(monkeypatch, seen)
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
            str(tmp_path / "res.json"),
        ]
    )
    assert exit_code == 0
    assert seen["agent_id"] is None


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
        def get_active(self):
            return None

        def resolve_and_activate(self, requested, provider=None):
            raise httpx.HTTPError("401 unauthorized")

        def restore(self, original): ...
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
        def get_active(self):
            return ActiveLlmProvider(provider_id="prov", default_model_id="gpt-5.2")

        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="prov", model_id="gpt-5.2", switched=False, provider_name="Test Provider")

        def restore(self, original): ...
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
        **kw,
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
        def get_active(self):
            return ActiveLlmProvider(provider_id="p", default_model_id="gpt-5.2")

        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="p", model_id="gpt-5.2", switched=False, provider_name="P")

        def restore(self, original): ...
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
        def get_active(self):
            return ActiveLlmProvider(provider_id="p", default_model_id="gpt-5.2")

        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="p", model_id="gpt-5.2", switched=False, provider_name="P")

        def restore(self, original): ...
        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)
    monkeypatch.setattr(cli_main, "ChatClient", lambda **k: object())
    monkeypatch.setattr(cli_main, "_load_dataset", lambda config: [])

    langfuse_calls: list = []

    class _FakeSink:
        def __init__(self, dataset_name, run_name, model_id="", provider_type="", reasoning_effort=None): ...
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
        **kw,
    ):
        on_lf = kw.get("on_langfuse_item_done")
        r = EvalReport(model=model, workspace_id=workspace_id)
        item_report = ItemReport(
            id="acme-001", dataset_name="d", test_kind="visualization", question="q", pass_at_k=True, runs=1
        )
        r.items.append(item_report)
        if on_lf:
            on_lf(1, 1, item_report)
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


def test_cli_multimodel_runs_each_model(monkeypatch, fixtures_dir):
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))
    activated_models = []

    class _FakeController:
        def __init__(self, *a, **k): ...
        def get_active(self):
            return ActiveLlmProvider(provider_id="p", default_model_id="orig")

        def resolve_and_activate(self, requested, provider=None):
            activated_models.append(requested)
            return ResolvedModel(provider_id="p", model_id=requested or "orig", switched=False, provider_name="P")

        def restore(self, original):
            activated_models.append(f"restore:{original.default_model_id if original else 'none'}")

        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)
    monkeypatch.setattr(cli_main, "ChatClient", lambda **k: object())

    def _fake_run(items, backend, *, runs, model, workspace_id, **kw):
        return EvalReport(
            model=model,
            workspace_id=workspace_id,
            items=[
                ItemReport(id="i1", dataset_name="d", test_kind="visualization", question="q", pass_at_k=True, runs=1)
            ],
        )

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
            "--dataset",
            str(fixtures_dir / "sample_dataset"),
            "--model",
            "gpt-5.2",
            "--model",
            "gpt-4o",
            "--quiet",
        ]
    )
    assert exit_code == 0
    assert "gpt-5.2" in activated_models
    assert "gpt-4o" in activated_models
    assert any("restore:" in m for m in activated_models)


def test_cli_multimodel_writes_nested_json(monkeypatch, tmp_path, fixtures_dir):
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _FakeController:
        def __init__(self, *a, **k): ...
        def get_active(self):
            return ActiveLlmProvider(provider_id="p", default_model_id="orig")

        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="p", model_id=requested or "orig", switched=False, provider_name="P")

        def restore(self, original): ...
        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)
    monkeypatch.setattr(cli_main, "ChatClient", lambda **k: object())

    def _fake_run(items, backend, *, runs, model, workspace_id, **kw):
        return EvalReport(
            model=model,
            workspace_id=workspace_id,
            items=[
                ItemReport(id="i1", dataset_name="d", test_kind="visualization", question="q", pass_at_k=True, runs=1)
            ],
        )

    monkeypatch.setattr(cli_main, "run_items", _fake_run)
    out = tmp_path / "results.json"
    cli_main.main(
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
            "--model",
            "gpt-5.2",
            "--model",
            "gpt-4o",
            "--json",
            str(out),
            "--quiet",
        ]
    )
    data = orjson.loads(out.read_bytes())
    # keys are provider-prefixed (provider_name/model); provider_name is "P" here
    assert data["models"] == ["P/gpt-5.2", "P/gpt-4o"]
    assert "runs" in data and "comparison" in data
    assert data["comparison"]["P/gpt-5.2"]["passed"] == 1


def test_cli_restore_fires_even_when_model_loop_raises(monkeypatch, fixtures_dir):
    """workspace.restore() must be called even if all model activations raise."""
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    restored = []

    class _FakeController:
        def __init__(self, *a, **k): ...

        def get_active(self):
            return ActiveLlmProvider(provider_id="p", default_model_id="orig")

        def resolve_and_activate(self, requested, provider=None):
            raise RuntimeError("activation failed")

        def restore(self, original):
            restored.append(original.default_model_id if original else None)

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
            "--model",
            "gpt-5.2",
            "--quiet",
        ]
    )
    assert exit_code == 2  # no models succeeded → error
    assert restored == ["orig"]  # restore was still called


def test_parse_model_arg_plain_model():
    assert _parse_model_arg("gpt-5.2") == (None, "gpt-5.2")


def test_parse_model_arg_provider_slash_model():
    assert _parse_model_arg("Foundry4o/gpt-5.2") == ("Foundry4o", "gpt-5.2")


def test_parse_model_arg_provider_id_slash_model():
    p, m = _parse_model_arg("foundry_6563e0a3-9354/gpt-4o")
    assert p == "foundry_6563e0a3-9354" and m == "gpt-4o"


def test_parse_model_arg_strips_whitespace():
    assert _parse_model_arg(" Provider / gpt-5.2 ") == ("Provider", "gpt-5.2")


def test_cli_models_command_exits_ok(monkeypatch):
    """gd-eval models dispatches to _list_models and exits 0."""
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))
    monkeypatch.setattr(cli_main, "_list_models", lambda host, token, workspace_id: cli_main._EXIT_OK)
    exit_code = cli_main.main(
        [
            "models",
            "--host",
            "https://h",
            "--token",
            "tok",
            "--workspace",
            "ws1",
        ]
    )
    assert exit_code == 0


def test_parse_model_arg_plain_model_no_strip():
    # The no-slash path does not strip whitespace; argparse never passes
    # whitespace through, so this documents the current behaviour.
    assert _parse_model_arg(" gpt-5.2 ") == (None, " gpt-5.2 ")


def test_cli_rejects_zero_concurrency(monkeypatch, fixtures_dir):
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))
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
            "--concurrency",
            "0",
        ]
    )
    assert exit_code == 2


def test_cli_preserve_failed_flag_parsed(monkeypatch, fixtures_dir):
    """--preserve-failed sets preserve_failed=True in RunConfig and is passed to ChatClient."""
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))
    captured_kwargs: dict = {}

    class _FakeController:
        def __init__(self, *a, **k): ...
        def get_active(self):
            return ActiveLlmProvider(provider_id="p", default_model_id="gpt-5.2")

        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="p", model_id="gpt-5.2", switched=False, provider_name="P")

        def restore(self, original): ...
        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)

    def _capture_chat_client(**kwargs):
        captured_kwargs.update(kwargs)
        return object()

    monkeypatch.setattr(cli_main, "ChatClient", _capture_chat_client)

    def _fake_run(items, backend, *, runs, model, workspace_id, **kw):
        return EvalReport(
            model=model,
            workspace_id=workspace_id,
            items=[
                ItemReport(id="i1", dataset_name="d", test_kind="visualization", question="q", pass_at_k=True, runs=1)
            ],
        )

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
            "--dataset",
            str(fixtures_dir / "sample_dataset"),
            "--preserve-failed",
            "--quiet",
        ]
    )
    assert exit_code == 0
    assert captured_kwargs.get("preserve_failed") is True


def test_cli_rejects_negative_concurrency(monkeypatch, fixtures_dir):
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))
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
            "--concurrency",
            "-1",
        ]
    )
    assert exit_code == 2


def test_progress_callbacks_thread_safe():
    """Verify progress callbacks can be called from multiple threads without error."""
    console = Console(file=io.StringIO(), force_terminal=False)
    on_item_start, on_run_done, on_item_done = cli_main._make_progress_callbacks(console)

    errors: list[Exception] = []

    def _worker(index: int) -> None:
        try:
            item = DatasetItem(
                id=f"test-{index}",
                dataset_name="test",
                test_kind="general_question",
                question=f"Question {index}",
                expected_output="answer",
            )
            on_item_start(index, 100, item)
            on_run_done(index, 100, 1, 1, index % 2 == 0, 1.5)
            report = ItemReport(
                id=f"test-{index}", dataset_name="test", test_kind="general_question", question=f"Question {index}"
            )
            report.runs = 1
            report.latency_s = 1.5
            report.pass_at_k = index % 2 == 0
            on_item_done(index, 100, report)
        except Exception as e:
            errors.append(e)

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(_worker, i) for i in range(50)]
        for f in as_completed(futures):
            f.result()  # re-raise if any thread failed

    assert not errors, f"Thread-safety violation: {errors}"
    output = console.file.getvalue()
    assert "test-1" in output
    assert "test-49" in output


def test_cli_reasoning_effort_flag_parsed(monkeypatch, fixtures_dir):
    """--reasoning-effort reaches RunConfig and is passed on to ChatClient."""
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))
    captured_kwargs: dict = {}

    class _FakeController:
        def __init__(self, *a, **k): ...
        def get_active(self):
            return ActiveLlmProvider(provider_id="p", default_model_id="gpt-5.2")

        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="p", model_id="gpt-5.2", switched=False, provider_name="P")

        def restore(self, original): ...
        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)

    def _capture_chat_client(**kwargs):
        captured_kwargs.update(kwargs)
        return object()

    monkeypatch.setattr(cli_main, "ChatClient", _capture_chat_client)

    def _fake_run(items, backend, *, runs, model, workspace_id, **kw):
        return EvalReport(
            model=model,
            workspace_id=workspace_id,
            items=[
                ItemReport(id="i1", dataset_name="d", test_kind="visualization", question="q", pass_at_k=True, runs=1)
            ],
        )

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
            "--dataset",
            str(fixtures_dir / "sample_dataset"),
            "--reasoning-effort",
            "LOW",
            "--quiet",
        ]
    )
    assert exit_code == 0
    assert captured_kwargs.get("reasoning_effort") == "LOW"


def test_cli_rejects_unknown_reasoning_effort(fixtures_dir):
    """argparse choices guard the value before it can reach the server as a 422."""
    with pytest.raises(SystemExit) as exc_info:
        cli_main.main(
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
                "--reasoning-effort",
                "low",
            ]
        )
    assert exc_info.value.code == 2


def test_cli_passes_concurrency_to_the_agentic_runner(monkeypatch, tmp_path):
    # The gap this closes: --concurrency reached run_items only, so a dataset of agentic
    # items accepted the flag and then ran strictly sequentially anyway -- a real run with
    # --concurrency 4 came out no faster than without it.
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _FakeController:
        def __init__(self, *a, **k): ...
        def get_active(self):
            return ActiveLlmProvider(provider_id="prov", default_model_id="gpt-5.2")

        def resolve_and_activate(self, requested, provider=None):
            return ResolvedModel(provider_id="prov", model_id="gpt-5.2", switched=False, provider_name="P")

        def restore(self, original): ...
        def close(self): ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)
    monkeypatch.setattr(cli_main, "ChatClient", lambda **k: object())
    monkeypatch.setattr(
        cli_main,
        "load_local_dataset",
        lambda folder: [
            DatasetItem(
                id="q1",
                dataset_name="d",
                test_kind="agentic_general_question",
                question="q",
                expected_output="a",
            )
        ],
    )
    monkeypatch.setattr(cli_main, "run_items", lambda items, backend, **kw: EvalReport(model="gpt-5.2"))

    captured = {}

    def _fake_run_agentic(items, **kwargs):
        captured.update(kwargs)
        return EvalReport(model="gpt-5.2")

    monkeypatch.setattr(cli_main, "run_agentic_items", _fake_run_agentic)

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
            str(tmp_path),
            "--concurrency",
            "3",
        ]
    )

    assert exit_code == 0
    assert captured["concurrency"] == 3


def test_cli_timers_flag_enables_timer_output(monkeypatch):
    # --timers is the discoverable front door for GD_EVAL_TIMERS. The env var is the
    # mechanism because the [timer] call sites sit four layers below the CLI, inside the
    # per-run helpers -- the same reason TAVERN_E2E_SKIP_TRACE_LINK is read at call time.
    monkeypatch.delenv(TIMERS_ENV_VAR, raising=False)
    assert timers_enabled() is False
    cli_main.parse_args(["run", "--workspace", "ws1", "--dataset", "/tmp", "--timers"])
    cli_main._apply_timer_flag(True)
    assert timers_enabled() is True


def test_cli_leaves_timers_off_without_the_flag(monkeypatch):
    monkeypatch.delenv(TIMERS_ENV_VAR, raising=False)
    cli_main._apply_timer_flag(False)
    assert timers_enabled() is False


def test_cli_timers_flag_defaults_to_false():
    args = cli_main.parse_args(["run", "--workspace", "ws1", "--dataset", "/tmp"])
    assert args.timers is False


def test_cli_judge_model_defaults_to_gpt_4o(monkeypatch):
    args = cli_main.parse_args(["run", "--workspace", "ws1", "--dataset", "/tmp"])
    assert args.judge_model is None
    monkeypatch.delenv(JUDGE_MODEL_ENV_VAR, raising=False)
    cli_main._apply_judge_model(args.judge_model)
    assert judge_model() == "gpt-4o"


def test_cli_judge_model_flag_overrides_the_default(monkeypatch):
    # Recorded first so teardown removes what _apply_judge_model writes into os.environ
    # directly; monkeypatch only restores keys it has seen.
    monkeypatch.delenv(JUDGE_MODEL_ENV_VAR, raising=False)
    args = cli_main.parse_args(["run", "--workspace", "ws1", "--dataset", "/tmp", "--judge-model", "gpt-4o-mini"])
    cli_main._apply_judge_model(args.judge_model)
    assert judge_model() == "gpt-4o-mini"


def test_cli_judge_model_flag_beats_the_env_var(monkeypatch):
    # An explicit flag is a deliberate choice for this run; an exported var is ambient.
    monkeypatch.setenv(JUDGE_MODEL_ENV_VAR, "gpt-4o")
    cli_main._apply_judge_model("gpt-5.6-luna")
    assert judge_model() == "gpt-5.6-luna"


# --- a local dataset plus live Langfuse credentials cannot link (say so up front) ---


_LF_CREDS = {"LANGFUSE_PUBLIC_KEY": "pk", "LANGFUSE_SECRET_KEY": "sk"}


def _export_langfuse_creds(monkeypatch) -> None:
    for name, value in _LF_CREDS.items():
        monkeypatch.setenv(name, value)


def _local_dataset_config(tmp_path):
    return RunConfig(host="http://h", token="t", workspace_id="ws1", dataset_folder=tmp_path)


def _agentic_item():
    return DatasetItem(
        id="gdai-2179-001",
        dataset_name="GDAI-2179",
        test_kind="agentic_general_question",
        question="q",
        expected_output="e",
    )


def test_warns_up_front_when_a_local_dataset_cannot_be_linked(monkeypatch, tmp_path, capsys):
    """--langfuse is refused with a local dataset, but the evaluators' own
    try_make_langfuse_client() fallback links anyway when LANGFUSE_* are exported -- so
    every conversation 404s from dataset-run-items, in a block at the very END of the run.
    By then the flag that would have avoided it is long past being changeable.
    """
    _export_langfuse_creds(monkeypatch)
    monkeypatch.delenv(TIMERS_ENV_VAR, raising=False)
    monkeypatch.delenv("TAVERN_E2E_SKIP_TRACE_LINK", raising=False)
    cli_main._warn_if_local_dataset_cannot_link(_local_dataset_config(tmp_path), [_agentic_item()])

    err = capsys.readouterr().err
    assert "--dataset is a local folder" in err
    assert "--langfuse-dataset" in err and "TAVERN_E2E_SKIP_TRACE_LINK=1" in err


def test_no_warning_when_the_skip_switch_is_already_set(monkeypatch, tmp_path, capsys):
    _export_langfuse_creds(monkeypatch)
    monkeypatch.setenv("TAVERN_E2E_SKIP_TRACE_LINK", "1")
    cli_main._warn_if_local_dataset_cannot_link(_local_dataset_config(tmp_path), [_agentic_item()])

    assert capsys.readouterr().err == ""


def test_no_warning_without_langfuse_credentials(monkeypatch, tmp_path, capsys):
    for k in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "TAVERN_E2E_SKIP_TRACE_LINK"):
        monkeypatch.delenv(k, raising=False)
    cli_main._warn_if_local_dataset_cannot_link(_local_dataset_config(tmp_path), [_agentic_item()])

    assert capsys.readouterr().err == ""


def test_no_warning_for_a_langfuse_backed_dataset(monkeypatch, capsys):
    # --langfuse-dataset items carry real Langfuse ids, so linking works and there is
    # nothing to warn about.
    config = RunConfig(host="http://h", token="t", workspace_id="ws1", langfuse_dataset="GDAI-2179")
    _export_langfuse_creds(monkeypatch)
    monkeypatch.delenv("TAVERN_E2E_SKIP_TRACE_LINK", raising=False)
    cli_main._warn_if_local_dataset_cannot_link(config, [_agentic_item()])

    assert capsys.readouterr().err == ""


def test_no_warning_when_there_are_no_agentic_items(monkeypatch, tmp_path, capsys):
    # The single-turn path links through LangfuseSink and only with --langfuse, so it never
    # hits the fallback this warning is about.
    _export_langfuse_creds(monkeypatch)
    monkeypatch.delenv("TAVERN_E2E_SKIP_TRACE_LINK", raising=False)
    cli_main._warn_if_local_dataset_cannot_link(_local_dataset_config(tmp_path), [])

    assert capsys.readouterr().err == ""
