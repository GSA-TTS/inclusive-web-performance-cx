"""Tests for cli"""

import os
import csv
from pathlib import Path
import numbers

from click.testing import CliRunner
from api_client.main import main


OUTPUT_FILE = Path(__file__).parent.resolve() / "output.csv"


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
            Path(__file__).parent.resolve() / "urls.txt",
            "--output-file",
            OUTPUT_FILE,
        ],
    )
    assert result.exit_code == 0
    assert OUTPUT_FILE.exists()
    data = []
    with open(OUTPUT_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        for row in reader:
            data.append(float(row["first_contentful_paint_p75"]))
    assert all(isinstance(item, numbers.Number) for item in data) is True
    cleanup()
