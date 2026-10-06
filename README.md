# Restaurant Ops MCP

Open-source MCP tools for analyzing restaurant menu economics with AI assistants.

> **Status:** early alpha. The first release focuses on menu contribution margin and food-cost analysis from simple CSV data.

## Why this exists

Restaurant operators often have useful data trapped in POS exports and spreadsheets, but turning that data into clear decisions usually requires manual analysis.

Restaurant Ops MCP exposes small, auditable tools that an MCP-compatible AI assistant can call to answer questions such as:

- Which menu items contribute the most gross profit?
- What is the food-cost percentage for each item?
- Which items sell well but have weak contribution margins?
- What happens to margin when ingredient costs change?

The project is intentionally starting small and transparent. Each calculation lives in ordinary Python so operators and contributors can inspect how the numbers are produced.

## Current tools

### `calculate_menu_item_metrics`

Calculates:

- food-cost percentage
- contribution margin per unit
- gross sales
- total ingredient cost
- total contribution margin

### `analyze_menu_csv`

Accepts CSV text with these columns:

```text
item,selling_price,ingredient_cost,units_sold
```

It returns a menu-level summary plus item rankings by total contribution margin.

Example data is available in `examples/menu.csv`.

## Quick start

### Requirements

- Python 3.10+
- `uv` recommended, or any normal Python environment

### Using uv

```bash
git clone https://github.com/vgdikyan-droid/restaurant-ops-mcp.git
cd restaurant-ops-mcp
uv sync --extra dev
uv run mcp dev src/restaurant_ops_mcp/server.py
```

The MCP Inspector should open and let you call the tools interactively.

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
mcp dev src/restaurant_ops_mcp/server.py
```

## Example CSV

```csv
item,selling_price,ingredient_cost,units_sold
Salmon Bowl,18.50,6.40,120
Chicken Bowl,15.00,4.10,180
Spicy Tuna Roll,13.50,4.70,95
```

## Project principles

1. **Useful before clever** — tools should answer real operating questions.
2. **Auditable math** — calculations should be easy to inspect and test.
3. **Portable data** — start with CSV and simple schemas instead of locking users into one POS vendor.
4. **AI as an interface, not the source of truth** — the model can reason over results, but the underlying calculations stay deterministic.

## Roadmap

- [x] Menu-item margin calculator
- [x] CSV menu analysis
- [x] Automated tests
- [ ] Compare periods (week vs. week / month vs. month)
- [ ] Ingredient price-change scenarios
- [ ] Menu engineering quadrants
- [ ] Inventory variance analysis
- [ ] POS-specific import adapters
- [ ] Example Claude Desktop / Claude Code configuration

## Contributing

Contributions are welcome, especially from restaurant operators, hospitality technologists, and developers interested in practical MCP tooling.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
