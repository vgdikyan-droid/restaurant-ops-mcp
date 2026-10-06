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

Tests include launching the installed MCP server and CSV command, so install
the package before running them (`uv sync --extra dev` or `pip install -e ".[dev]"`).
The MCP test checks tool discovery, structured results, invalid inputs, and
recovery after errors over a real stdio connection.

Use an issue to describe the operator problem, a feature branch for the change,
and a pull request to review it. Wait for CI before merging. Keep examples
synthetic or anonymized, and describe AI assistance honestly when relevant.

## Release checklist

Before tagging a release, run the full suite in a fresh environment, try the
sample CLI and MCP client workflow, and check the supported Python CI jobs.
Move the relevant changelog entries out of Unreleased, update the version in
both `pyproject.toml` and `src/restaurant_ops_mcp/__init__.py`, and describe known
limitations. Tag the reviewed main-branch commit and publish matching GitHub
release notes. PyPI publication is a separate step and is not configured yet.

## Product principle

The AI model should not invent restaurant financial calculations. Core metrics should be deterministic, inspectable Python whenever possible.
