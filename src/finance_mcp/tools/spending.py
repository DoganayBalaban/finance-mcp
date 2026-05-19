from collections import defaultdict
from ..sheets.client import get_client
from ..models import Transaction

async def get_spending_by_category(year:int, month:int,top_n:int=5)->list[dict]:
    """Belirtilen ay için kategori bazlı harcama dağılımını döndürür."""
    client = get_client()
    rows = client.get_transactions(year,month)

    expenses = [Transaction(**r) for r in rows if r.get('type') == "expense"]

    total_expense = sum(abs(t.amount) for t in expenses)
    if total_expense == 0:
        return []
    
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)

    for exp in expenses:
        category_totals[exp.category] += abs(exp.amount)
        category_counts[exp.category] += 1
    
    results = []
    for category, total in category_totals.items():
        results.append({
            "category":category,
            "total":round(total, 2),
            "percentage": round((total / total_expense) * 100, 1),
            "transaction_count": category_counts[category]
        })
    
    results.sort(key=lambda x: x["total"], reverse=True)
    return results[:top_n]