# Changelog

## 0.2.0a1 — first alpha release

- Add `restaurant-ops` for local CSV text reports and JSON output.
- Add `restaurant-ops-mcp` and module startup for stdio clients.
- Reject non-finite numbers, duplicate/empty CSV headers, and malformed rows;
  accept UTF-8 byte-order marks and surrounding header spaces.
- Add review warnings for ingredient costs above prices and no-sales periods.
- Add a weekly operator guide and clarify theoretical costs versus net profit.
- Test installed commands and a real MCP connection; expand Python CI coverage.
- Verify the built package in CI and include the operator guide and sample in the source distribution.
- Add issue and pull request templates for reproducible bugs and operator feedback.

This is an early testing release. It has no POS integration, measured business
outcomes, or verified external adoption. See the [release notes](docs/releases/0.2.0a1.md).

## 0.1.0 project baseline

- Initial menu-item calculations and CSV analysis, sample data, tests, and CI.
- This records the package baseline; it does not imply a published package or GitHub release.
