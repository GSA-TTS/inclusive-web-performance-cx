"""Tests for cli"""

import os
from pathlib import Path

from click.testing import CliRunner
from format_urls.main import main

OUTPUT_FILE = Path(__file__).parent.resolve() / "output.txt"


def cleanup():
    """cleanup from previous tests"""
    try:
        os.remove(OUTPUT_FILE)
    except OSError:
        pass


def test_main():
    """Test correct output is generated"""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--input-urls",
            Path(__file__).parent.resolve() / "input.csv",
            "--output-file",
            OUTPUT_FILE,
        ],
    )
    assert result.exit_code == 0
    assert OUTPUT_FILE.exists()
    with open(OUTPUT_FILE, encoding="utf8") as f:
        result = f.read()
    assert result == (
        "url\n"
        "https://www.time.gov/\n"
        "https://tools.usps.com/go/trackconfirmaction\n"
    )
    cleanup()


def test_missing_params():
    """Test exception is raised if missing params"""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--input-urls",
        ],
    )
    assert result.exception
