from mcp.server.fastmcp import FastMCP

from .tools import balance

mcp = FastMCP(name="finance-mcp")

mcp.tool()(balance.get_monthly_summary)

if __name__ == "__main__":
    mcp.run()
