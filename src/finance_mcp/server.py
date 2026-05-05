from mcp.server.fastmcp import FastMCP
from datetime import date

from finance_mcp.tools import goal, report
from .tools import compare
from .tools import add_transaction
from .tools import forecast
from .tools import budget
from .tools import spending
from .tools import balance

mcp = FastMCP(name="finance-mcp")

@mcp.resource("finance://summary/current")
async def current_month_summary()->str:
    """Bu ayın genel finansal özetini döndürür."""
    today = date.today()
    try:
        summary = await balance.get_monthly_summary(today.year, today.month)
        return (
            f"Güncel Ay ({today.year}-{today.month:02d}) Özeti:\n"
            f"Toplam Gelir: {summary['total_income']} TL\n"
            f"Toplam Gider: {summary['total_expense']} TL\n"
            f"Net Bakiye: {summary['net_balance']} TL\n"
            f"Tasarruf Oranı: %{summary['savings_rate']}"
        )
    except Exception as e:
        return f"Güncel ay verisi okunamadı: {e}"


mcp.tool()(balance.get_monthly_summary)
mcp.tool()(spending.get_spending_by_category)
mcp.tool()(budget.check_budget_status)
mcp.tool()(forecast.get_saving_forecast)
mcp.tool()(add_transaction.add_transaction)
mcp.tool()(compare.compare_months)
mcp.tool()(report.generate_monthly_report)
mcp.tool()(goal.set_savings_goal)

if __name__ == "__main__":
    mcp.run()
