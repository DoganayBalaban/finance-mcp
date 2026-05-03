from ..sheets.client import SheetsClient
from ..models import Transaction, TransactionType


async def get_monthly_summary(year: int, month: int) -> dict:
    """Belirtilen ay için gelir/gider özeti döndürür."""
    client = SheetsClient()
    rows = client.get_transactions(year, month)

    txns = [Transaction(**r) for r in rows]

    income = sum(t.amount for t in txns if t.type == TransactionType.INCOME)
    expense = sum(abs(t.amount) for t in txns if t.type == TransactionType.EXPENSE)

    return {
        "total_income": income,
        "total_expense": expense,
        "net_balance": income - expense,
        "savings_rate": round((income - expense) / income * 100, 1) if income else 0.0,
    }
