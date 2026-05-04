from mcp.server.fastmcp import FastMCP

from .tools import spending
from .tools import balance

mcp = FastMCP(name="finance-mcp")

mcp.tool()(balance.get_monthly_summary)
mcp.tool()(spending.get_spending_by_category)

if __name__ == "__main__":
    mcp.run()
