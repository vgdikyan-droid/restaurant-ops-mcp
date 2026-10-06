"""Exercise the actual MCP protocol and installed server in a subprocess."""

import asyncio
from pathlib import Path
import sys

from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client


def test_stdio_tool_discovery_calls_and_errors(tmp_path):
    async def check():
        server = StdioServerParameters(
            command=str(Path(sys.executable).parent / "restaurant-ops-mcp"),
            cwd=str(tmp_path),
        )
        async with Client(stdio_client(server), read_timeout_seconds=10) as client:
            tools = await client.list_tools()
            assert {tool.name for tool in tools.tools} == {
                "calculate_menu_item_metrics", "analyze_menu_csv",
            }
            item = await client.call_tool("calculate_menu_item_metrics", {
                "selling_price": 20, "ingredient_cost": 6, "units_sold": 10,
            })
            assert not item.is_error
            assert item.structured_content["total_contribution_margin"] == 140
            menu = await client.call_tool("analyze_menu_csv", {
                "csv_text": "item,selling_price,ingredient_cost,units_sold\nSoup,10,2,3\n",
            })
            assert not menu.is_error
            assert menu.structured_content["summary"]["gross_sales"] == 30
            bad = await client.call_tool("analyze_menu_csv", {
                "csv_text": "item,selling_price,ingredient_cost,units_sold\nSoup,10,NaN,3\n",
            })
            assert bad.is_error
            assert "finite number" in bad.content[0].text
            # One invalid request must not stop the server.
            again = await client.call_tool("calculate_menu_item_metrics", {
                "selling_price": 10, "ingredient_cost": 0,
            })
            assert not again.is_error

    asyncio.run(asyncio.wait_for(check(), timeout=30))
