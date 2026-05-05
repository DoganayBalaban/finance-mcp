import os
import sys
import gspread
from dotenv import load_dotenv

load_dotenv()

class SheetsClient:
    def __init__(self):
        creds_path = os.getenv("SERVICE_ACCOUNT_JSON")
        if not creds_path:
            raise ValueError("SERVICE_ACCOUNT_JSON environment variable is not set")

        self.gc = gspread.service_account(filename=creds_path)
        self.sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        if not self.sheet_id:
            raise ValueError("GOOGLE_SHEETS_ID environment variable is not set")

    def get_transactions(self, year:int, month:int):
        ws = self.gc.open_by_key(self.sheet_id).worksheet("Transactions")
        rows = ws.get_all_records()

        filtered_rows = []
        for r in rows:
            row_date = str(r.get('date', ''))
            if row_date.startswith(f"{year}-{month:02d}"):
                filtered_rows.append(r)

        return filtered_rows

    def get_budgets(self, year:int, month:int):
        ws = self.gc.open_by_key(self.sheet_id).worksheet("Budgets")
        rows = ws.get_all_records()
        return [r for r in rows if r.get('year') == year and r.get('month') == month]

    def append_transactions(self, row_data:list)->bool:
        """Transactions sayfasına yeni bir satır (işlem) ekler."""
        try:
            ws = self.gc.open_by_key(self.sheet_id).worksheet("Transactions")
            ws.append_row(row_data)
            return True
        except Exception as e:
            print(f"Google sheets'e yazılırken bir hata oluştu: {e}", file=sys.stderr)
            return False

    def set_savings_goal(self, year:int, month:int, amount:float)->bool:
        """Goals sayfasına tasarruf hedefi yazar. Aynı ay/yıl için mevcut satırı günceller."""
        try:
            ws = self.gc.open_by_key(self.sheet_id).worksheet("Goals")
            rows = ws.get_all_records()
            for i, r in enumerate(rows, start=2):
                if r.get('year') == year and r.get('month') == month:
                    ws.update(f"C{i}", [[amount]])
                    return True
            ws.append_row([year, month, amount])
            return True
        except Exception as e:
            print(f"Hedef Google Sheets'e yazılırken hata: {e}", file=sys.stderr)
            return False


if __name__ == "__main__":
    try:
        client = SheetsClient()
        print("Sheets bağlantısı başarılı", file=sys.stderr)
    except Exception as e:
        print(f"Bağlantı hatası: {e}", file=sys.stderr)
