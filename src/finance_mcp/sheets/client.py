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
        try:
            ws = self.gc.open_by_key(self.sheet_id).worksheet("Transactions")
            rows = ws.get_all_records()
        except Exception:
            invalidate_client()
            raise

        filtered_rows = []
        for r in rows:
            row_date = str(r.get('date', ''))
            if row_date.startswith(f"{year}-{month:02d}"):
                filtered_rows.append(r)

        return filtered_rows

    def get_budgets(self, year:int, month:int):
        try:
            ws = self.gc.open_by_key(self.sheet_id).worksheet("Budgets")
            rows = ws.get_all_records()
        except Exception:
            invalidate_client()
            raise
        return [r for r in rows if r.get('year') == year and r.get('month') == month]

    def append_transactions(self, row_data:list)->bool:
        """Transactions sayfasına yeni bir satır (işlem) ekler."""
        try:
            ws = self.gc.open_by_key(self.sheet_id).worksheet("Transactions")
            ws.append_row(row_data)
            return True
        except Exception as e:
            print(f"Google sheets'e yazılırken bir hata oluştu: {e}", file=sys.stderr)
            invalidate_client()
            return False

    def find_transaction_row(self, date_str: str, description: str, amount: float) -> int | None:
        """Eşleşen ilk işlemin satır numarasını döndürür (1-tabanlı, başlık dahil)."""
        try:
            ws = self.gc.open_by_key(self.sheet_id).worksheet("Transactions")
            rows = ws.get_all_values()
        except Exception:
            invalidate_client()
            raise
        for i, row in enumerate(rows[1:], start=2):
            try:
                if (len(row) >= 5 and
                        row[0] == date_str and
                        row[1] == description and
                        abs(float(row[3]) - amount) < 0.001):
                    return i
            except (ValueError, IndexError):
                continue
        return None

    def delete_transaction_row(self, row_number: int) -> bool:
        try:
            ws = self.gc.open_by_key(self.sheet_id).worksheet("Transactions")
            ws.delete_rows(row_number)
            return True
        except Exception as e:
            print(f"Satır silinirken hata: {e}", file=sys.stderr)
            invalidate_client()
            return False

    def update_transaction_row(self, row_number: int, row_data: list) -> bool:
        try:
            ws = self.gc.open_by_key(self.sheet_id).worksheet("Transactions")
            ws.update(f"A{row_number}:E{row_number}", [row_data])
            return True
        except Exception as e:
            print(f"Satır güncellenirken hata: {e}", file=sys.stderr)
            invalidate_client()
            return False

    def upsert_budget(self, category: str, year: int, month: int, monthly_limit: float) -> bool:
        try:
            ws = self.gc.open_by_key(self.sheet_id).worksheet("Budgets")
            rows = ws.get_all_records()
            for i, r in enumerate(rows, start=2):
                if (r.get('category') == category and
                        r.get('year') == year and
                        r.get('month') == month):
                    ws.update(f"B{i}", [[monthly_limit]])
                    return True
            ws.append_row([category, monthly_limit, year, month])
            return True
        except Exception as e:
            print(f"Bütçe kaydedilirken hata: {e}", file=sys.stderr)
            invalidate_client()
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
            invalidate_client()
            return False


_client: "SheetsClient | None" = None


def get_client() -> "SheetsClient":
    global _client
    if _client is None:
        try:
            _client = SheetsClient()
        except Exception:
            _client = None
            raise
    return _client


def invalidate_client() -> None:
    """Singleton'ı sıfırlar. gspread API hatalarında çağrılır, bir sonraki get_client() yeniden bağlanır."""
    global _client
    _client = None


if __name__ == "__main__":
    try:
        client = SheetsClient()
        print("Sheets bağlantısı başarılı", file=sys.stderr)
    except Exception as e:
        print(f"Bağlantı hatası: {e}", file=sys.stderr)
