# Restaurant Ops MCP

Menu sales, food-cost analysis, and contribution rankings through a local CLI and the Model Context Protocol (MCP).

Turn a menu sales export and per-portion ingredient costs into a repeatable operating review. Run reports locally or connect the same calculations to an MCP-compatible assistant.

[![Tests](https://github.com/vgdikyan-droid/restaurant-ops-mcp/actions/workflows/tests.yml/badge.svg)](https://github.com/vgdikyan-droid/restaurant-ops-mcp/actions/workflows/tests.yml)

Created and maintained by the operator of **Balboa Poke**, Restaurant Ops MCP
brings restaurant operating knowledge to open-source tooling. The project uses
deterministic Python calculations, documented assumptions, and automated checks
to make menu economics inspectable and repeatable.

**Release:** [v0.2.0a1](https://github.com/vgdikyan-droid/restaurant-ops-mcp/releases/tag/v0.2.0a1) · Python 3.10–3.14 tested · MIT licensed.

## Engineering and verification

- **Shared calculation logic:** the CLI and MCP tools use the same menu metrics.
- **46 automated tests:** arithmetic, CSV validation, command-line behavior, and
  an actual MCP client/server connection, including recovery after invalid input.
- **Compatibility checks:** CI covers Python 3.10–3.14 and the minimum supported
  MCP SDK version.
- **Package verification:** CI builds distribution archives, checks metadata,
  and tests an installed wheel.
- **Reviewable changes:** feature branches, pull requests, and passing CI precede
  merges; release notes document supported behavior.

## Why this exists

Restaurant operators often have useful data trapped in POS exports and spreadsheets, but turning that data into clear decisions usually requires manual analysis.

Restaurant Ops MCP exposes auditable tools that an MCP-compatible AI assistant can call to answer questions such as:

- Which menu items contribute the most after ingredient costs?
- What is the food-cost percentage for each item?
- Which items sell well but have weak contribution margins?

Price-change scenarios and period comparisons are planned, not implemented yet.

Calculations run in Python, independently of the assistant, so operators and contributors can inspect and test how each result is produced.

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

It returns a menu-level summary, item rankings by total contribution margin,
and warnings for loss-making items or a period with no sales.

Synthetic example data is available in `examples/menu.csv`.

## Review your week without an AI assistant

After installing, run:

```bash
restaurant-ops examples/menu.csv
```

The sample has sales of **8,152.50** across **615 units**. The report shows
theoretical ingredient cost, weighted food-cost percentage, and items ranked by
contribution after ingredients. Amounts use the currency supplied in the CSV;
do not mix currencies.

For machine-readable output:

```bash
restaurant-ops examples/menu.csv --json
```

See the [weekly review guide](docs/weekly-review.md) for preparing your own data,
interpreting results, and recording useful feedback. No AI account is needed
for this local report.

## Quick start

For a versioned source download, see [GitHub releases](https://github.com/vgdikyan-droid/restaurant-ops-mcp/releases).
Extract the source archive, open its folder, and follow the virtual-environment
and pip installation steps below (skip `git clone` when using an archive).
This project is not published to PyPI; install from this repository or its releases.

### Requirements

- Python 3.10+
- `uv` recommended, or any normal Python environment
- Node.js/npm only if you want the optional browser-based MCP Inspector

### Using uv

```bash
git clone https://github.com/vgdikyan-droid/restaurant-ops-mcp.git
cd restaurant-ops-mcp
uv sync --extra dev
uv run restaurant-ops examples/menu.csv
```

For the optional MCP Inspector, run `uv run mcp dev src/restaurant_ops_mcp/server.py`.

### Using pip

```bash
git clone https://github.com/vgdikyan-droid/restaurant-ops-mcp.git
cd restaurant-ops-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
restaurant-ops examples/menu.csv
```

On Windows, activate with `.venv\Scripts\Activate.ps1` in PowerShell.

## Connect an MCP client

This project uses the official **MCP Python SDK v2** (`mcp>=2.0,<3.0`) and
`MCPServer`. It is not the separate FastMCP package. See the
[official SDK documentation](https://py.sdk.modelcontextprotocol.io/).

The installed `restaurant-ops-mcp` command runs the server over standard
input/output (stdio). The client launches it when needed; it does not open a
web port. Running it by itself waits quietly for protocol messages.

For clients that accept an `mcpServers` JSON configuration, use your installed
environment's **absolute** executable path:

```json
{
  "mcpServers": {
    "restaurant-ops": {
      "command": "/absolute/path/to/restaurant-ops-mcp/.venv/bin/restaurant-ops-mcp",
      "args": []
    }
  }
}
```

On Windows the executable is `.venv\\Scripts\\restaurant-ops-mcp.exe`.
Configuration location varies by client. A client can also launch the virtual
environment's Python with arguments `-m restaurant_ops_mcp.server`.

Try: “Use the restaurant tools to calculate a menu item with selling price 20,
ingredient cost 6, and 10 units sold.” Expected total contribution: **140**.
The CSV tool accepts CSV **text**, not a filename, and does not read arbitrary
files. If you use an AI client, CSV content and results may be sent to that
client's provider. The standalone CSV report runs locally.

## What these numbers mean

- Ingredient cost is the recipe cost **per portion**; units sold cover one period.
- Food-cost percentage = ingredient cost / selling price × 100.
- Weighted food-cost percentage = total ingredient cost / total sales × 100.
- Contribution = sales minus ingredients. It excludes labor, rent, payment and
  delivery fees, waste, and other costs, so it is **not net profit**.
- These are theoretical food costs, not actual inventory usage or purchase totals.
- Amounts are rounded to two decimal places for display; this is an operating
  estimate, not an accounting ledger.
- The JSON field `gross_sales` is price × units. Use realized prices after
  discounts and before tax/tips to approximate your POS sales consistently.
- With no units sold, the text report shows food cost as N/A. The JSON field
  `weighted_food_cost_pct` retains `0.0` for compatibility, alongside a warning.

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
- [x] Local CSV report for weekly reviews
- [x] MCP connection test and CSV validation
- [ ] Compare periods (week vs. week / month vs. month)
- [ ] Ingredient price-change scenarios
- [ ] Menu engineering quadrants
- [ ] Inventory variance analysis
- [ ] POS-specific import adapters
- [ ] Example Claude Desktop / Claude Code configuration

## Contributing

Contributions are welcome, especially from restaurant operators, hospitality technologists, and developers interested in practical MCP tooling.

See [CONTRIBUTING.md](CONTRIBUTING.md).

To try a real workflow, follow the [pilot checklist](docs/operator-pilot.md).
Report a reproducible bug or operator feedback using the GitHub issue templates.

## License

MIT
