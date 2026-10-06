# Weekly menu sales and food-cost review

Use this workflow to check one week's menu economics. The included menu is
synthetic, and no real restaurant outcomes have been validated yet.

## 1. Prepare a small export

Start with five to ten items you know well. Use the same start/end dates for
every row. Copy or export these columns to a UTF-8 CSV:

| Column | Meaning | Example |
| --- | --- | --- |
| `item` | Menu item and portion size | Chicken Bowl |
| `selling_price` | Realized price per portion, excluding tax and tips | 15.00 |
| `ingredient_cost` | Current recipe ingredient cost per portion | 4.10 |
| `units_sold` | Whole portions sold in the period | 180 |

Use plain numbers without currency symbols, percent signs, or thousands
separators. All prices and costs must use the same currency. Price must be
greater than zero; costs and units must be nonnegative and finite. Extra named
columns are allowed and ignored; every row must match the header's width.
Column names are case-sensitive; surrounding header spaces and a UTF-8
byte-order mark are accepted.

Use one row per item/size. Repeated names are treated as separate rows and
counted separately; remove accidental duplicates before running a report.
Quote names containing commas, as normal spreadsheet CSV export does.

If prices vary, use sales after discounts divided by paid units for the average
realized price, or separate rows for different prices. Returns, negative units,
and zero-price comps are not supported in this first version; reconcile them
separately instead of silently omitting their impact. Track comp ingredient
costs separately. Sales tax, tips, delivery fees, and payments are not menu sales.

## 2. Run the review

```bash
restaurant-ops path/to/your-week.csv
```

If using uv, put `uv run` before the command. To save the report:

```bash
restaurant-ops path/to/your-week.csv > weekly-review.txt
```

Invalid files produce an error and a nonzero exit code instead of a partial
report. Row numbers identify the physical CSV line (the ending line for a
quoted multiline record). A price/cost error names the item and field.

## 3. Check the result against what you know

1. Check total units and sales against the same items and dates in your POS.
   Investigate discounts, modifiers, returns, comps, or missing items if they differ.
2. Check one recipe's per-portion cost manually against recent supplier prices.
   Include all ingredients and consistent yields. This tool does not yet cost recipes for you.
3. Review the contribution ranking. High sales volume can make an item important
   even if its food-cost percentage is higher than another item's.
4. Investigate items flagged as costing more in ingredients than their selling
   price. A warning is a reason to check data and context, not an automatic price change.
5. Choose one action to investigate, such as recosting a popular dish. Record what
   you learned before changing prices or portions.

Do not infer actual food usage or waste from this report. Actual usage requires
opening inventory, purchases, closing inventory, and adjustments. Labor, rent,
fees, and other costs must also be considered before interpreting profitability.

## 4. Record honest feedback

Keep a private note of the period, number of items reviewed, any data adjustments,
whether totals reconciled, and one useful finding or confusing result. If you
measure time saved, record how you measured it. Do not claim savings or adoption
without evidence.

To report a problem on GitHub, use a small anonymized or synthetic example and
show the expected result. Never attach customer details, employee information,
private supplier invoices, or confidential prices to a public issue. Personal
CSV data can live in the ignored `local-data/` folder.
