# WealthGuard MCP Server 💰

WealthGuard is a Model Context Protocol (MCP) server that manages, analyzes, and reports on personal financial data through Google Sheets — fully integrated with LLMs such as Claude.

Simply ask your AI assistant questions in natural language to analyze monthly expenses, check budget overruns, get future forecasts, and write new transactions directly to your spreadsheet.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 📊 `get_monthly_summary` | Calculates total income, expenses, net balance, and savings rate for a given month |
| 🍕 `get_spending_by_category` | Breaks down spending by category and shows percentage distribution (Top 5) |
| 🚨 `check_budget_status` | Compares set monthly limits against actual spending and produces status alerts (Exceeded / Warning / On Track) |
| 🔮 `get_savings_forecast` | Uses a 3-month moving average of past data to forecast next month's savings |
| ✍️ `add_transaction` | Adds a new income/expense row to Google Sheets after receiving user confirmation via chat |
| ⚖️ `compare_months` | Compares income, expenses, and balance changes between two different months |
| 🎯 `set_savings_goal` | Writes savings/accumulation goals to the spreadsheet for upcoming months |
| 📄 `generate_monthly_report` | Generates a detailed Markdown (`.md`) report containing the month's full financial summary, budget status, and spending categories — saved locally |
| 🌐 Dynamic Resource | The `finance://summary/current` URI lets the assistant read current month data in real time |

---

## 🛠️ Setup

### Requirements

- Python 3.11 or higher
- `uv` package manager (or `pip`)
- Google Cloud Service Account (JSON credentials file)
- Google Sheets account

### Steps

**1. Clone the repository and set up the environment:**

```bash
git clone <repo-url>
cd wealthguard-mcp
uv venv
source .venv/bin/activate
```

**2. Install dependencies:**

```bash
uv pip install -e .
```

**3. Prepare your Google Spreadsheet:**

Create a new Google Sheets file and add the following 3 worksheets:

- `Transactions` — columns: `date`, `description`, `category`, `amount`, `type`
- `Budgets` — columns: `category`, `monthly_limit`, `year`, `month`
- `Goals` — columns: `year`, `month`, `target_amount`

> **Note:** Grant **Editor** access to your Service Account email (e.g. `bot@project.iam.gserviceaccount.com`) on this spreadsheet.

**4. Configure credentials and environment variables:**

Create a `credentials/` folder in the project root and place your Service Account JSON file there as `service_account.json`.

Copy `.env.example` to `.env` and fill in your values:

```env
GOOGLE_SHEETS_ID="your_spreadsheet_id_here"
SERVICE_ACCOUNT_JSON="credentials/service_account.json"
```

---

## 🚀 Usage — Claude Desktop Integration

To use WealthGuard with Claude Desktop, update your configuration file based on your OS:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "finance-mcp": {
      "command": "/FULL/PATH/wealthguard-mcp/.venv/bin/python",
      "args": [
        "-m",
        "src.finance_mcp.server"
      ],
      "env": {
        "PYTHONPATH": "/FULL/PATH/wealthguard-mcp",
        "GOOGLE_SHEETS_ID": "your_spreadsheet_id_here",
        "SERVICE_ACCOUNT_JSON": "/FULL/PATH/wealthguard-mcp/credentials/service_account.json"
      }
    }
  }
}
```

> Replace `/FULL/PATH/` with the absolute path to the project on your machine.

Restart Claude Desktop. You can now ask your assistant things like:

- *"How much did I spend last month?"*
- *"I paid $80 at the grocery store today — log it."*
- *"Generate a financial report for April."*

---

## 🔐 Security

- The `credentials/` directory and `.env` file are listed in `.gitignore`. **Never push these files to a public repository.**
- Write operations (`add_transaction`) require explicit user confirmation enforced through the LLM system prompt.

---

**Developer:** Doğanay Balaban · [GitHub](https://github.com/DoganayBalaban)