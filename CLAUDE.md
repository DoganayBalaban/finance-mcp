# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WealthGuard is a **Model Context Protocol (MCP) server** that connects LLMs (e.g. Claude Desktop) to a personal finance Google Spreadsheet. It exposes tools and a resource via FastMCP so that users can query and write financial data through natural language.

## Development Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e .
```

Required environment variables (copy `.env.example` → `.env`):
- `GOOGLE_SHEETS_ID` — the Google Sheets file ID
- `SERVICE_ACCOUNT_JSON` — path to the service account JSON (e.g. `credentials/service_account.json`)

Run the server directly:
```bash
python -m src.finance_mcp.server
```

Interactive inspection via MCP Inspector (spins up a local UI):
```bash
mcp dev src/finance_mcp/server.py
```

Verify Google Sheets connectivity in isolation:
```bash
python src/finance_mcp/sheets/client.py
```

There are no automated tests. Manually test by connecting Claude Desktop (see README for config).

## Architecture

```
src/finance_mcp/
├── server.py          # FastMCP entrypoint — registers all tools and the resource
├── models.py          # Pydantic models: Transaction, Budget, TransactionType
├── sheets/
│   ├── client.py      # SheetsClient — all Google Sheets I/O (gspread + service account auth)
│   └── parser.py      # Row parsing helpers
└── tools/
    ├── balance.py     # get_monthly_summary
    ├── spending.py    # get_spending_by_category
    ├── budget.py      # check_budget_status
    ├── forecast.py    # get_saving_forecast (3-month moving average)
    ├── add_transaction.py  # add_transaction (write tool — requires user confirmation)
    ├── compare.py     # compare_months
    ├── goal.py        # set_savings_goal
    └── report.py      # generate_monthly_report (writes local .md file)
```

**MCP resource:** `finance://summary/current` — returns a plain-text current-month summary (income/expense/balance/savings rate). Registered in `server.py` with `@mcp.resource()`.

**Data flow:** `server.py` registers each tool function with `mcp.tool()`. Tool functions are async and instantiate `SheetsClient` on each call — there is no shared connection state. `SheetsClient` reads credentials from env vars at construction time.

**Google Sheets schema** (three worksheets):
- `Transactions` — columns: `date` (YYYY-MM-DD), `description`, `category`, `amount`, `type` (income/expense)
- `Budgets` — columns: `category`, `monthly_limit`, `year`, `month`
- `Goals` — columns: `year`, `month`, `target_amount`

## Adding a New Tool

1. Create `src/finance_mcp/tools/<name>.py` with an `async def` function.
2. Import and register it in `server.py` with `mcp.tool()(<module>.<function>)`.
3. If the tool writes data, use the two-layer safety pattern from `add_transaction.py`:
   - Add a `confirmed: bool = False` parameter; return an early rejection dict when `False`.
   - Embed a Turkish-language instruction in the docstring telling the LLM to ask for confirmation before calling the tool.

## Language Constraint

All docstrings and user-facing messages must be written in **Turkish**. The LLM reads tool docstrings as runtime instructions, so language consistency matters.

## Key Constraints

- **Write operations require explicit user confirmation.** The `add_transaction` tool docstring instructs the LLM to ask for confirmation before calling the tool. Do not remove or weaken this constraint.
- Credentials (`credentials/`, `.env`) are gitignored and must never be committed.
- The MCP server is run by Claude Desktop as a subprocess; **stdout must stay clean**. All debug/error output must go to `sys.stderr` (e.g. `print(..., file=sys.stderr)`), never plain `print()`.
