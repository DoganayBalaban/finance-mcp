import gspread
from oauth2client.service_account import ServiceAccountCredentials
from mcp.server.fastmcp import FastMCP

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

SHEET_NAME = "WealthGuard_Data"
sheet = client.open(SHEET_NAME)

mcp = FastMCP("WealthGuard")

@mcp.tool()
def get_balance_summary()->str:
    """Bütçe özetini ve kalan parayı getirir"""
    worksheet = sheet.worksheet("Butce")
    data = worksheet.get_all_records()[0]

    gelir = data["Gelir"]
    gider = data["Sabit_Giderler"]
    hedef = data["Tasarruf_Hedefi"]
    kalan = gelir - gider - hedef

    return f"Gelir: {gelir} TL, Sabit Giderler: {gider} TL, Hedeflenen Tasarruf: {hedef} TL. Harcanabilir Kalan: {kalan} TL."

if __name__ == "__main__":
    mcp.run()


