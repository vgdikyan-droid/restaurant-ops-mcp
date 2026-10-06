import pytest

from restaurant_ops_mcp.analysis import (
    analyze_menu_csv_text,
    calculate_metrics,
)


def test_calculate_metrics():
    result = calculate_metrics(
        selling_price=20.0,
        ingredient_cost=6.0,
        units_sold=10,
    )

    assert result["food_cost_pct"] == 30.0
    assert result["contribution_margin_per_unit"] == 14.0
    assert result["gross_sales"] == 200.0
    assert result["total_contribution_margin"] == 140.0


def test_analyze_menu_csv_text_ranks_by_total_contribution():
    csv_text = """item,selling_price,ingredient_cost,units_sold
Salmon Bowl,18.50,6.40,10
Chicken Bowl,15.00,4.10,20
"""

    result = analyze_menu_csv_text(csv_text)

    assert result["summary"]["item_count"] == 2
    assert result["summary"]["total_units_sold"] == 30
    assert result["items_by_total_contribution"][0]["item"] == "Chicken Bowl"


def test_analyze_menu_csv_text_requires_expected_columns():
    csv_text = """item,selling_price
Salmon Bowl,18.50
"""

    with pytest.raises(ValueError, match="missing required columns"):
        analyze_menu_csv_text(csv_text)
