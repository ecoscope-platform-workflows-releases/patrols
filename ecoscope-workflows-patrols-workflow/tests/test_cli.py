# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "67e050a5f34893bb04f20a0b9d002543d121cd619de7305c3c889e5446d2b502"


from pathlib import Path

from ecoscope_workflows_core.testing import TestCase, run_cli_test_case


def test_cli(
    entrypoint: str,
    execution_mode: str,
    mock_io: bool,
    case: TestCase,
    tmp_path: Path,
):
    run_cli_test_case(entrypoint, execution_mode, mock_io, case, tmp_path)
