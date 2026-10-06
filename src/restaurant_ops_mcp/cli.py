"""Local menu review without an AI account or MCP client."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from restaurant_ops_mcp.analysis import analyze_menu_csv_text


def format_report(result: dict[str, Any]) -> str:
    """Render amounts in the input's currency, without assuming a currency symbol."""
    summary = result["summary"]
    food_cost = (
        f"{summary['weighted_food_cost_pct']:.2f}%"
        if summary["total_units_sold"] else "N/A (no sales)"
    )
    lines = [
        "Menu sales and food-cost review",
        "Amounts use the currency in your CSV.",
        f"Menu rows: {summary['item_count']} | Units sold: {summary['total_units_sold']:,}",
        f"Sales (price x units): {summary['gross_sales']:,.2f}",
        f"Theoretical ingredient cost: {summary['total_ingredient_cost']:,.2f}",
        f"Contribution after ingredients: {summary['total_contribution_margin']:,.2f}",
        f"Weighted food cost: {food_cost}",
        "",
        "Items ranked by total contribution after ingredients:",
    ]
    for index, item in enumerate(result["items_by_total_contribution"], 1):
        # JSON quoting keeps names containing newlines/control characters on one line.
        name = json.dumps(item["item"], ensure_ascii=False)
        lines.append(
            f"{index}. {name} | {item['units_sold']:,} sold | "
            f"Food cost {item['food_cost_pct']:.2f}% | "
            f"Contribution/unit {item['contribution_margin_per_unit']:,.2f} | "
            f"Total contribution {item['total_contribution_margin']:,.2f}"
        )
    if result["warnings"]:
        lines.extend(["", "Review notes:"])
        lines.extend(f"- {json.dumps(note, ensure_ascii=False)}" for note in result["warnings"])
    lines.extend([
        "",
        "Contribution is not net profit: labor, rent, fees, waste, and other costs are excluded.",
        "Recipe costs estimate ingredients used; they do not measure actual inventory usage.",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Review menu sales and theoretical food costs from a CSV.")
    parser.add_argument("csv_file", type=Path, help="UTF-8 CSV containing one period's menu sales")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON instead of a text report")
    args = parser.parse_args(argv)
    try:
        result = analyze_menu_csv_text(args.csv_file.read_text(encoding="utf-8-sig"))
        output = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) if args.json else format_report(result)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
