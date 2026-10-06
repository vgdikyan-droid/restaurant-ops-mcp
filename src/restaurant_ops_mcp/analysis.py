"""Deterministic restaurant operating calculations."""

from __future__ import annotations

import csv
from decimal import Decimal, InvalidOperation
import io
import math
from typing import Any


def _nonnegative_float(value: float | int | str, field: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a number, not true/false")
    try:
        parsed = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{field} must be a number") from exc

    if not math.isfinite(parsed):
        raise ValueError(f"{field} must be a finite number")
    if parsed < 0:
        raise ValueError(f"{field} cannot be negative")
    return parsed


def _nonnegative_int(value: float | int | str, field: str) -> int:
    # Parse counts without first rounding them through a binary float.
    try:
        parsed = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{field} must be a number") from exc
    if not parsed.is_finite():
        raise ValueError(f"{field} must be a finite number")
    if parsed < 0:
        raise ValueError(f"{field} cannot be negative")
    if parsed != parsed.to_integral_value():
        raise ValueError(f"{field} must be a whole number")
    if parsed > 2**53 - 1:
        raise ValueError(f"{field} is too large to calculate safely")
    return int(parsed)


def calculate_metrics(
    selling_price: float,
    ingredient_cost: float,
    units_sold: int = 1,
) -> dict[str, float | int]:
    """Calculate core economics for one menu item."""
    price = _nonnegative_float(selling_price, "selling_price")
    cost = _nonnegative_float(ingredient_cost, "ingredient_cost")
    units = _nonnegative_int(units_sold, "units_sold")

    if price == 0:
        raise ValueError("selling_price must be greater than zero")

    contribution_margin = price - cost
    gross_sales = price * units
    total_ingredient_cost = cost * units
    total_contribution_margin = contribution_margin * units
    food_cost_pct = (cost / price) * 100
    if not all(math.isfinite(value) for value in (
        gross_sales, total_ingredient_cost, total_contribution_margin, food_cost_pct
    )):
        raise ValueError("values are too large to calculate safely")

    return {
        "selling_price": round(price, 2),
        "ingredient_cost": round(cost, 2),
        "units_sold": units,
        "food_cost_pct": round(food_cost_pct, 2),
        "contribution_margin_per_unit": round(contribution_margin, 2),
        "gross_sales": round(gross_sales, 2),
        "total_ingredient_cost": round(total_ingredient_cost, 2),
        "total_contribution_margin": round(total_contribution_margin, 2),
    }


def analyze_menu_csv_text(csv_text: str) -> dict[str, Any]:
    """Analyze menu economics from CSV text.

    Required columns:
    item,selling_price,ingredient_cost,units_sold
    """
    if not csv_text or not csv_text.strip():
        raise ValueError("csv_text cannot be empty")

    # UTF-8 spreadsheet exports may start with a byte-order mark.
    reader = csv.DictReader(io.StringIO(csv_text.lstrip("\ufeff")), strict=True)
    required = {"item", "selling_price", "ingredient_cost", "units_sold"}
    try:
        headers = [name.strip() for name in (reader.fieldnames or [])]
    except csv.Error as exc:
        raise ValueError(f"CSV header: {exc}") from exc
    if len(headers) != len(set(headers)):
        raise ValueError("CSV contains duplicate column names")
    if any(not name for name in headers):
        raise ValueError("CSV contains an empty column name")
    reader.fieldnames = headers
    fieldnames = set(headers)
    missing = sorted(required - fieldnames)

    if missing:
        raise ValueError(
            "CSV is missing required columns: " + ", ".join(missing)
        )

    items: list[dict[str, Any]] = []

    for row_number, row in _csv_rows(reader):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"row {row_number}: number of values does not match the header")
        item = (row.get("item") or "").strip()
        if not item:
            raise ValueError(f"row {row_number}: item cannot be empty")

        try:
            metrics = calculate_metrics(
                selling_price=row["selling_price"],
                ingredient_cost=row["ingredient_cost"],
                units_sold=row["units_sold"],
            )
        except ValueError as exc:
            raise ValueError(f"row {row_number} ({item}): {exc}") from exc

        items.append({"item": item, **metrics})

    if not items:
        raise ValueError("CSV contains no menu items")

    total_sales = sum(float(item["gross_sales"]) for item in items)
    total_ingredient_cost = sum(
        float(item["total_ingredient_cost"]) for item in items
    )
    total_contribution = sum(
        float(item["total_contribution_margin"]) for item in items
    )
    total_units = sum(int(item["units_sold"]) for item in items)
    if not all(math.isfinite(value) for value in (
        total_sales, total_ingredient_cost, total_contribution
    )):
        raise ValueError("menu totals are too large to calculate safely")

    ranked = sorted(
        items,
        key=lambda item: float(item["total_contribution_margin"]),
        reverse=True,
    )

    summary = {
        "item_count": len(items),
        "total_units_sold": total_units,
        "gross_sales": round(total_sales, 2),
        "total_ingredient_cost": round(total_ingredient_cost, 2),
        "total_contribution_margin": round(total_contribution, 2),
        "weighted_food_cost_pct": round(
            (total_ingredient_cost / total_sales) * 100, 2
        )
        if total_sales
        else 0.0,
    }

    warnings = []
    if total_units == 0:
        warnings.append("No units were sold; weighted food-cost percentage is not applicable.")
    for item in items:
        if item["ingredient_cost"] > item["selling_price"]:
            warnings.append(f"{item['item']}: ingredient cost exceeds selling price.")

    return {
        "summary": summary,
        "items_by_total_contribution": ranked,
        "warnings": warnings,
    }


def _csv_rows(reader: csv.DictReader):
    """Turn parser failures into actionable errors with physical CSV line numbers."""
    while True:
        try:
            row = next(reader)
        except StopIteration:
            return
        except csv.Error as exc:
            raise ValueError(f"row {reader.reader.line_num}: invalid CSV: {exc}") from exc
        yield reader.line_num, row
