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


@pytest.mark.parametrize("field", ["selling_price", "ingredient_cost", "units_sold"])
@pytest.mark.parametrize("value", ["NaN", "inf", "-inf", True, -1, "bad", None])
def test_rejects_invalid_numbers(field, value):
    arguments = dict(selling_price=20, ingredient_cost=6, units_sold=10)
    arguments[field] = value
    with pytest.raises(ValueError, match=field):
        calculate_metrics(**arguments)


def test_rejects_fractional_units_and_zero_price():
    with pytest.raises(ValueError, match="whole number"):
        calculate_metrics(20, 6, 1.5)
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_metrics(0, 6)


def test_unit_count_is_not_silently_rounded():
    with pytest.raises(ValueError, match="whole number"):
        calculate_metrics(10, 2, "2.0000000000000001")
    with pytest.raises(ValueError, match="units_sold is too large"):
        calculate_metrics(10, 2, "9007199254740993")


def test_rejects_overflowing_calculations():
    with pytest.raises(ValueError, match="too large"):
        calculate_metrics(1e308, 1, 10)


HEADER = "item,selling_price,ingredient_cost,units_sold\n"


def test_weighted_food_cost_uses_sales_not_average_of_percentages():
    result = analyze_menu_csv_text(HEADER + "A,10,2,10\nB,20,10,5\n")
    assert result["summary"] == {
        "item_count": 2, "total_units_sold": 15, "gross_sales": 200,
        "total_ingredient_cost": 70, "total_contribution_margin": 130,
        "weighted_food_cost_pct": 35,
    }
    assert result["warnings"] == []


@pytest.mark.parametrize("row, message", [
    ("A,10,2,1,extra", "number of values"),
    ("A,10,2", "number of values"),
    ("A,10,NaN,1", "ingredient_cost must be a finite number"),
    (",10,2,1", "item cannot be empty"),
    ('"A,10,2,1', "invalid CSV"),
])
def test_bad_csv_rows_have_useful_errors(row, message):
    with pytest.raises(ValueError, match=f"row 2.*{message}"):
        analyze_menu_csv_text(HEADER + row)


def test_duplicate_headers_are_rejected():
    with pytest.raises(ValueError, match="duplicate column"):
        analyze_menu_csv_text(HEADER.rstrip() + ",ingredient_cost\nA,10,2,1,99")


def test_spreadsheet_bom_header_spaces_and_quoted_names():
    result = analyze_menu_csv_text(
        '\ufeffitem, selling_price ,ingredient_cost,units_sold,category\n'
        '"Soup, large",10,2,3,lunch\n'
    )
    assert result["items_by_total_contribution"][0]["item"] == "Soup, large"
    assert result["summary"]["gross_sales"] == 30


@pytest.mark.parametrize("csv_text", ["", "   ", HEADER])
def test_empty_inputs_fail(csv_text):
    with pytest.raises(ValueError):
        analyze_menu_csv_text(csv_text)


def test_loss_making_items_and_zero_sales_are_reported():
    result = analyze_menu_csv_text(HEADER + "Soup,10,12,0\n")
    assert result["summary"]["gross_sales"] == 0
    # Retained for compatibility; warnings and the text report explain N/A.
    assert result["summary"]["weighted_food_cost_pct"] == 0
    assert len(result["warnings"]) == 2
    assert "exceeds selling price" in result["warnings"][1]


def test_zero_ingredient_cost_and_negative_margin_are_valid():
    assert calculate_metrics(10, 0, 2)["total_contribution_margin"] == 20
    assert calculate_metrics(10, 12, 2)["total_contribution_margin"] == -4
