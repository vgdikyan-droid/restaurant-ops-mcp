# Contributing

Thanks for considering a contribution to Restaurant Ops MCP.

This project is early-stage, so small, focused contributions are especially useful.

## Good first contributions

- improve documentation or examples
- add tests for edge cases
- propose a restaurant operating metric
- add support for a common POS export format
- improve validation and error messages

## Development setup

```bash
git clone https://github.com/vgdikyan-droid/restaurant-ops-mcp.git
cd restaurant-ops-mcp
uv sync --extra dev
uv run pytest
```

## Pull requests

Please keep pull requests focused on one problem.

A useful PR should explain:

1. what problem it solves
2. why the change is useful
3. how it was tested

For changes to calculations, include tests showing the expected numbers.

## Product principle

The AI model should not invent restaurant financial calculations. Core metrics should be deterministic, inspectable Python whenever possible.
