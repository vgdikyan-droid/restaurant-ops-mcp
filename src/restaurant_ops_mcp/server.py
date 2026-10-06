"""MCP server exposing restaurant operating tools."""

from __future__ import annotations

from typing import Any

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

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
        selling_price: Realized selling price per unit, excluding tax and tips.
        ingredient_cost: Direct ingredient cost for one unit.
        units_sold: Number of units sold in the period being analyzed.
    """
    try:
        return calculate_metrics(
            selling_price=selling_price,
            ingredient_cost=ingredient_cost,
            units_sold=units_sold,
        )
    except ValueError as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool()
def analyze_menu_csv(csv_text: str) -> dict[str, Any]:
    """Analyze menu economics from CSV text.

    The CSV must include these columns:
    item,selling_price,ingredient_cost,units_sold

    Returns menu-level totals and items ranked by total contribution margin.
    Costs are theoretical recipe costs, not measured purchases or inventory usage.
    Contribution excludes labor, rent, fees, waste, and other operating costs.
    """
    try:
        return analyze_menu_csv_text(csv_text)
    except ValueError as exc:
        raise ToolError(str(exc)) from exc


def main() -> None:
    """Run the local MCP server over standard input/output."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
