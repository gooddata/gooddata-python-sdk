# (C) 2026 GoodData Corporation
from __future__ import annotations

import io
import json
import urllib.request
from pathlib import Path

import pytest
from next_dev_version import dev_base, main, next_dev_version, released_versions


def test_dev_base_bumps_patch() -> None:
    assert dev_base("1.79.0") == "1.79.1"
    assert dev_base("1.60.9") == "1.60.10"


@pytest.mark.parametrize("current", ["1.79", "1.79.1.dev2", "1.79.0a1", ""])
def test_dev_base_rejects_non_stable(current: str) -> None:
    with pytest.raises(ValueError):
        dev_base(current)


def test_first_dev_release() -> None:
    assert next_dev_version("1.79.1", ["1.78.0", "1.78.1.dev4", "1.79.0"]) == "1.79.1.dev1"


def test_compares_dev_numbers_numerically() -> None:
    assert next_dev_version("1.79.1", ["1.79.0", "1.79.1.dev9", "1.79.1.dev10"]) == "1.79.1.dev11"


def test_ignores_other_lines() -> None:
    # A newer minor or an older line's dev releases do not affect the base.
    released = ["1.60.1", "1.60.2.dev3", "1.79.0", "1.79.1.dev5", "1.80.0a1"]
    assert next_dev_version("1.60.2", released) == "1.60.2.dev4"


def test_union_of_components_after_partial_publish() -> None:
    # gooddata-sdk failed to publish dev3, gooddata-pandas got it: dev3 is taken.
    sdk = ["1.79.0", "1.79.1.dev1", "1.79.1.dev2"]
    pandas = ["1.79.0", "1.79.1.dev1", "1.79.1.dev2", "1.79.1.dev3"]
    assert next_dev_version("1.79.1", sdk + pandas) == "1.79.1.dev4"


def test_refuses_dev_of_released_version() -> None:
    # The branch is still at 1.79.0 while 1.79.1 is out: 1.79.1.devN would sort below 1.79.1.
    with pytest.raises(ValueError, match="already released"):
        next_dev_version("1.79.1", ["1.79.0", "1.79.1.dev4", "1.79.1"])


def _serve(monkeypatch: pytest.MonkeyPatch, payload: object) -> None:
    body = json.dumps(payload).encode()
    monkeypatch.setattr(urllib.request, "urlopen", lambda *_, **__: io.BytesIO(body))


def test_released_versions_reads_release_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    _serve(monkeypatch, {"releases": {"1.79.0": [], "1.79.1.dev1": []}})
    assert released_versions("gooddata-sdk") == ["1.79.0", "1.79.1.dev1"]


@pytest.mark.parametrize("payload", [{"releases": []}, {"info": {}}, []])
def test_released_versions_rejects_unexpected_shape(monkeypatch: pytest.MonkeyPatch, payload: object) -> None:
    _serve(monkeypatch, payload)
    with pytest.raises(ValueError, match="Unexpected PyPI response"):
        released_versions("gooddata-sdk")


def test_main_uses_given_pyproject(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # An old release line: its own version decides the base, not the script's checkout.
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[tool.tbump.version]\ncurrent = "1.60.1"\n')
    _serve(monkeypatch, {"releases": {"1.60.1": [], "1.60.2.dev1": [], "1.79.0": []}})
    main(["--pyproject", str(pyproject), "gooddata-sdk"])
    assert capsys.readouterr().out == "1.60.2.dev2\n"
