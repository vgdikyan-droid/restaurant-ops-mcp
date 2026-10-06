"""Deterministic restaurant operating calculations."""

from __future__ import annotations

import csv
import io
from typing import Any


def _nonnegative_float(value: float | int | str, field: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a number") from exc

    if parsed < 0:
        raise ValueError(f"{field} cannot be negative")
    return parsed


def _nonnegative_int(value: float | int | str, field: str) -> int:
    parsed = _nonnegative_float(value, field)
    if not parsed.is_integer():
        raise ValueError(f"{field} must be a whole number")
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

    return {
        "selling_price": round(price, 2),
        "ingredient_cost": round(cost, 2),
        "units_sold": units,
        "food_cost_pct": round((cost / price) * 100, 2),
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

    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    required = {"item", "selling_price", "ingredient_cost", "units_sold"}
    fieldnames = set(reader.fieldnames or [])
    missing = sorted(required - fieldnames)

    if missing:
        raise ValueError(
            "CSV is missing required columns: " + ", ".join(missing)
        )

    items: list[dict[str, Any]] = []

    for row_number, row in enumerate(reader, start=2):
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

    return {
        "summary": summary,
        "items_by_total_contribution": ranked,
    }
