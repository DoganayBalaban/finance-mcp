import datetime
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

@mcp.tool()
def add_expense(kategori:str, aciklama:str, tutar:float)->str:
    """Yeni bir harcama kaydeder."""
    worksheet = sheet.worksheet("Harcamalar")
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row([tarih, kategori, aciklama, tutar])
    return f"Harcama başarıyla kaydedildi: {tarih} - {kategori} - {aciklama} - {tutar} TL."

@mcp.tool()
def can_i_afford_this(urun_adi:str, fiyat:float)->str:
    """Belirtilen ürünün fiyatını kontrol eder ve bütçe yeterli mi diye kontrol eder."""
    summary = get_balance_summary()
    kalan_limit = float(summary.split("Harcanabilir Kalan: ")[1].split(" TL.")[0])
    if fiyat <= kalan_limit:
        yeni_limit = kalan_limit - fiyat
        return f"Evet, '{urun_adi}' alabilirsiniz. Yeni kalan limit: {yeni_limit} TL."
    else:
        fark = fiyat - kalan_limit
        return f"Üzgünüz, '{urun_adi}' alamazsınız. Bütçenizde yeterli para yok. {fark} TL eksik."

if __name__ == "__main__":
    mcp.run()


