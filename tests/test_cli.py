import json
from pathlib import Path
import subprocess
import sys

from restaurant_ops_mcp.cli import main


def test_installed_cli_from_another_directory(tmp_path):
    sample = Path(__file__).resolve().parents[1] / "examples/menu.csv"
    command = Path(sys.executable).parent / "restaurant-ops"
    result = subprocess.run(
        [str(command), str(sample)], cwd=tmp_path,
        text=True, capture_output=True, timeout=15,
    )
    assert result.returncode == 0, result.stderr
    assert "Sales (price x units): 8,152.50" in result.stdout
    assert '1. "Chicken Bowl"' in result.stdout
    assert "Contribution is not net profit" in result.stdout


def test_json_output(tmp_path, capsys):
    sample = tmp_path / "menu.csv"
    sample.write_text("item,selling_price,ingredient_cost,units_sold\nSoup,10,2,3\n")
    assert main([str(sample), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["summary"]["gross_sales"] == 30


def test_invalid_csv_returns_error_without_partial_report(tmp_path, capsys):
    sample = tmp_path / "bad.csv"
    sample.write_text("item,selling_price,ingredient_cost,units_sold\nSoup,10,NaN,3\n")
    assert main([str(sample)]) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert "row 2 (Soup)" in output.err


def test_missing_file_is_readable_error(tmp_path, capsys):
    assert main([str(tmp_path / "missing.csv")]) == 2
    assert "Error:" in capsys.readouterr().err


def test_no_sales_report_shows_not_applicable(tmp_path, capsys):
    sample = tmp_path / "menu.csv"
    sample.write_text("item,selling_price,ingredient_cost,units_sold\nSoup,10,2,0\n")
    assert main([str(sample)]) == 0
    assert "Weighted food cost: N/A (no sales)" in capsys.readouterr().out
