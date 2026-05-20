import sys
from datetime import date
from ..sheets.client import get_client
from ..models import Transaction, TransactionType

async def get_saving_forecast(months_back:int=3, target_savings:float=None):
    """Son N ay verisiyle gelecek ay tasarruf tahmini üretir."""
    client = get_client()

    today = date.today()
    current_month = today.month
    current_year = today.year

    total_income = 0
    total_expense = 0
    valid_months = 0

    for i in range(months_back):
        total_months = current_year * 12 + current_month - i - 1
        y, m = divmod(total_months - 1, 12)
        m += 1

        try:
            rows = client.get_transactions(y, m)
            if not rows:
                continue

            txns = [Transaction(**r) for r in rows]
            total_income += sum(t.amount for t in txns if t.type == TransactionType.INCOME)
            total_expense += sum(abs(t.amount) for t in txns if t.type == TransactionType.EXPENSE)
            valid_months += 1
        except Exception as e:
            print(f"{y}-{m} dönemi çekilirken hata: {e}", file=sys.stderr)
            continue
    
    if valid_months == 0:
        return {"error": f"Son {months_back} ayda tahmin yapmak için geçmiş veri bulunamadı."}
    
    avg_income = total_income / valid_months
    avg_expense = total_expense / valid_months
    predicted_savings = avg_income - avg_expense

    trend = "positive" if predicted_savings > 0 else "negative"
    recommendation = "Ortalama geliriniz harcamalarınızın üzerinde, birikim yapmaya uygunsunuz." if trend == "positive" else "Dikkat: Ortalama harcamalarınız gelirinizi aşıyor."

    if target_savings:
        if predicted_savings >= target_savings:
            recommendation += f" {target_savings} TL hedefinize rahatça ulaşabilirsiniz."
        else:
            gap = target_savings - predicted_savings
            recommendation += f" {target_savings} TL hedefine ulaşmak için harcamalarınızı aylık ortalama {gap:.2f} TL kısmalısınız."
    
    return {
        "avg_income": round(avg_income, 2),
        "avg_expense": round(avg_expense, 2),
        "predicted_savings": round(predicted_savings, 2),
        "trend": trend,
        "recommendation": recommendation,
        "analyzed_months": valid_months
    }