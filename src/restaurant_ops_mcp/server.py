"""MCP server exposing restaurant operating tools."""

from __future__ import annotations

from typing import Any

from mcp.server import MCPServer

from restaurant_ops_mcp.analysis import (
    analyze_menu_csv_text,
    calculate_metrics,
)

mcp = MCPServer("Restaurant Ops MCP")


@mcp.tool()
def calculate_menu_item_metrics(
    selling_price: float,
    ingredient_cost: float,
    units_sold: int = 1,
) -> dict[str, float | int]:
    """Calculate food cost and contribution margin for one menu item.

    Args:
        selling_price: Customer-facing selling price for one unit.
        ingredient_cost: Direct ingredient cost for one unit.
        units_sold: Number of units sold in the period being analyzed.
    """
    return calculate_metrics(
        selling_price=selling_price,
        ingredient_cost=ingredient_cost,
        units_sold=units_sold,
    )


@mcp.tool()
def analyze_menu_csv(csv_text: str) -> dict[str, Any]:
    """Analyze menu economics from CSV text.

    The CSV must include these columns:
    item,selling_price,ingredient_cost,units_sold

    Returns menu-level totals and items ranked by total contribution margin.
    """
    return analyze_menu_csv_text(csv_text)
