from collections import defaultdict
from ..sheets.client import SheetsClient
from ..models import Transaction, Budget

async def check_budget_status(year:int, month:int) -> list[dict]:
    """Bütçe limitlerini gerçek harcamalarla karşılaştırır."""
    client = SheetsClient()

    try:
        budget_rows = client.get_budgets(year,month)
        budgets = [Budget(**r) for r in budget_rows]
    except Exception as e:
        print(f"Bütçe verisi çekilirken hata: {e}")
        return []
    
    if not budgets:
        return []

    txn_rows = client.get_transactions(year,month)
    expenses = [Transaction(**r) for r in txn_rows if r.get('type') == "expense"]

    spending_by_category = defaultdict(float)
    for exp in expenses:
        spending_by_category[exp.category] += abs(exp.amount)
    
    results = []
    for b in budgets:
        spent = spending_by_category.get(b.category, 0.0)
        remaining = b.monthly_limit - spent
        
        # Durum belirleme: Negatifse aşıldı, %20'den az kaldıysa uyarı
        if remaining < 0:
            status = "exceeded"
        elif remaining < (b.monthly_limit * 0.2):
            status = "warning"
        else:
            status = "ok"
            
        results.append({
            "category": b.category,
            "limit": b.monthly_limit,
            "spent": spent,
            "remaining": remaining,
            "status": status
        })
    
    return results