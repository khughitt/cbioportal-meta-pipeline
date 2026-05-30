# science:code
# status: library
# science:end
"""Smoke tests for the SELECT conda env file."""
from pathlib import Path

import yaml

ENV_PATH = Path(__file__).resolve().parents[3] / "code" / "envs" / "select.yml"


def test_env_file_exists():
    assert ENV_PATH.exists(), f"missing {ENV_PATH}"


def test_env_is_valid_yaml():
    with ENV_PATH.open() as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict)
    assert "name" in data
    assert "channels" in data
    assert "dependencies" in data


def test_env_pins_r44():
    with ENV_PATH.open() as f:
        data = yaml.safe_load(f)
    deps = data["dependencies"]
    r_base_pins = [d for d in deps if isinstance(d, str) and d.startswith("r-base")]
    assert r_base_pins, "must pin r-base"
    # Accept r-base=4.4 or r-base>=4.4
    assert any("4.4" in d for d in r_base_pins), f"must pin R 4.4, got {r_base_pins}"


def test_env_has_arrow():
    with ENV_PATH.open() as f:
        data = yaml.safe_load(f)
    assert any(
        d == "r-arrow" or (isinstance(d, str) and d.startswith("r-arrow"))
        for d in data["dependencies"]
    ), "must include r-arrow for feather I/O"


def test_env_excludes_devtools_and_remotes():
    """Design Section 4.8: tarball is the only install path; no devtools/remotes."""
    with ENV_PATH.open() as f:
        data = yaml.safe_load(f)
    deps = [d for d in data["dependencies"] if isinstance(d, str)]
    forbidden = {"r-devtools", "r-remotes"}
    found = forbidden & set(deps)
    assert not found, (
        f"must NOT include {found} — only install path is the vendored tarball "
        f"(design Section 4.8)"
    )
