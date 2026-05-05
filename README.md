<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/DoganayBalaban/finance-mcp">
    <img src="https://img.shields.io/badge/💰-WealthGuard-green?style=for-the-badge" alt="WealthGuard Logo">
  </a>

<h3 align="center">WealthGuard MCP</h3>

  <p align="center">
    A Model Context Protocol server that connects Claude to your Google Sheets for personal finance tracking, analysis, and reporting — all through natural language.
    <br />
    <a href="https://github.com/DoganayBalaban/finance-mcp"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/DoganayBalaban/finance-mcp/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/DoganayBalaban/finance-mcp/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

WealthGuard is an MCP server that lets you manage your personal finances through conversation. Ask Claude to analyze your monthly expenses, check budget overruns, forecast savings, or log a new transaction — all backed by a real Google Spreadsheet you own.

**Available tools:**

| Tool | Description |
|------|-------------|
| `get_monthly_summary` | Total income, expenses, net balance, and savings rate for any month |
| `get_spending_by_category` | Category breakdown with percentage distribution (Top 5) |
| `check_budget_status` | Compares monthly limits against actual spending (Exceeded / Warning / On Track) |
| `get_savings_forecast` | 3-month moving average forecast for next month's savings |
| `add_transaction` | Appends a new income/expense row after explicit user confirmation |
| `compare_months` | Side-by-side income, expense, and balance comparison between two months |
| `set_savings_goal` | Writes a savings target to the Goals worksheet |
| `generate_monthly_report` | Produces a full Markdown report saved locally |

A live `finance://summary/current` MCP resource also lets the assistant read the current month at any time.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python][Python.org]][Python-url]
[![FastMCP][FastMCP-badge]][FastMCP-url]
[![Google Sheets][Sheets-badge]][Sheets-url]
[![Pydantic][Pydantic-badge]][Pydantic-url]
[![uv][uv-badge]][uv-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) package manager
- A Google Cloud **Service Account** with a JSON credentials file
- A Google Sheets file shared with the service account (Editor access)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/DoganayBalaban/finance-mcp.git
   cd finance-mcp
   ```

2. Create and activate a virtual environment
   ```sh
   uv venv
   source .venv/bin/activate
   ```

3. Install dependencies
   ```sh
   uv pip install -e .
   ```

4. Place your Service Account JSON at `credentials/service_account.json`

5. Copy `.env.example` to `.env` and fill in your values
   ```env
   GOOGLE_SHEETS_ID="your_spreadsheet_id_here"
   SERVICE_ACCOUNT_JSON="credentials/service_account.json"
   ```

6. Create a Google Sheets file with these three worksheets:

   | Worksheet | Columns |
   |-----------|---------|
   | `Transactions` | `date`, `description`, `category`, `amount`, `type` |
   | `Budgets` | `category`, `monthly_limit`, `year`, `month` |
   | `Goals` | `year`, `month`, `target_amount` |

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE -->
## Usage

### Claude Desktop Integration

Add the following to your Claude Desktop config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "finance-mcp": {
      "command": "/FULL/PATH/finance-mcp/.venv/bin/python",
      "args": ["-m", "src.finance_mcp.server"],
      "env": {
        "PYTHONPATH": "/FULL/PATH/finance-mcp",
        "GOOGLE_SHEETS_ID": "your_spreadsheet_id_here",
        "SERVICE_ACCOUNT_JSON": "/FULL/PATH/finance-mcp/credentials/service_account.json"
      }
    }
  }
}
```

Replace `/FULL/PATH/` with the absolute path to the project on your machine, then restart Claude Desktop.

**Example prompts:**
- *"How much did I spend last month?"*
- *"Show me my top spending categories for April."*
- *"I paid $80 at the grocery store today — log it."*
- *"Am I over budget anywhere this month?"*
- *"Forecast my savings for next month."*
- *"Generate a financial report for March."*

> **Security note:** `add_transaction` always asks for explicit confirmation before writing to your spreadsheet. The LLM will summarize the transaction and say "Do you confirm?" before calling the tool.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Multi-currency support
- [ ] Recurring transaction detection
- [ ] Chart/visualization exports (PNG)
- [ ] Support for multiple spreadsheet profiles
- [ ] Web dashboard (read-only view)

See the [open issues](https://github.com/DoganayBalaban/finance-mcp/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also open an issue with the tag `enhancement`.
Don't forget to give the project a star!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/DoganayBalaban/finance-mcp/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=DoganayBalaban/finance-mcp" alt="contrib.rocks image" />
</a>



<!-- CONTACT -->
## Contact

Doğanay Balaban — [GitHub](https://github.com/DoganayBalaban)

Project Link: [https://github.com/DoganayBalaban/finance-mcp](https://github.com/DoganayBalaban/finance-mcp)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [FastMCP](https://github.com/jlowin/fastmcp) — MCP server framework for Python
* [gspread](https://github.com/burnash/gspread) — Google Sheets API client
* [Model Context Protocol](https://modelcontextprotocol.io/) — Open protocol by Anthropic
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/DoganayBalaban/finance-mcp.svg?style=for-the-badge
[contributors-url]: https://github.com/DoganayBalaban/finance-mcp/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DoganayBalaban/finance-mcp.svg?style=for-the-badge
[forks-url]: https://github.com/DoganayBalaban/finance-mcp/network/members
[stars-shield]: https://img.shields.io/github/stars/DoganayBalaban/finance-mcp.svg?style=for-the-badge
[stars-url]: https://github.com/DoganayBalaban/finance-mcp/stargazers
[issues-shield]: https://img.shields.io/github/issues/DoganayBalaban/finance-mcp.svg?style=for-the-badge
[issues-url]: https://github.com/DoganayBalaban/finance-mcp/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/doganay-balaban
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org
[FastMCP-badge]: https://img.shields.io/badge/FastMCP-000000?style=for-the-badge&logo=anthropic&logoColor=white
[FastMCP-url]: https://github.com/jlowin/fastmcp
[Sheets-badge]: https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white
[Sheets-url]: https://sheets.google.com
[Pydantic-badge]: https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white
[Pydantic-url]: https://docs.pydantic.dev
[uv-badge]: https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=astral&logoColor=white
[uv-url]: https://github.com/astral-sh/uv
