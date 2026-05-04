import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

class SheetsClient:
    def __init__(self):
        creds_path = os.getenv("SERVICE_ACCOUNT_JSON")
        if not creds_path:
            raise ValueError("SERVICE_ACCOUNT_JSON environment variable is not set")
        
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        self.gc = gspread.authorize(creds)
        self.sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        if not self.sheet_id:
            raise ValueError("GOOGLE_SHEETS_ID environment variable is not set")
    
    def get_transactions(self, year:int, month:int):
        ws = self.gc.open_by_key(self.sheet_id).worksheet("Transactions")
        rows = ws.get_all_records()

        filtered_rows = []
        for r in rows:
            try:
                # Beklenen format: YYYY-MM-DD
                row_date = str(r.get('date', ''))
                if row_date.startswith(f"{year}-{month:02d}"):
                    filtered_rows.append(r)
            except Exception as e:
                print(f"Satır işlenirken hata: {e}")

        return filtered_rows
    
    def get_budgets(self, year:int, month:int):
        ws = self.gc.open_by_key(self.sheet_id).worksheet("Budgets")
        rows = ws.get_all_records()
        return [r for r in rows if r.get('year') == year and r.get('month') == month]


if __name__ == "__main__":
    try:
        client = SheetsClient()
        print("Sheets bağlantısı başarılı")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
