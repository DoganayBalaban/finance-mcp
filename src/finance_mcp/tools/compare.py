from .balance import get_monthly_summary

async def compare_months(year1:int, month1:int, year2:int, month2:int)->dict:
    """İki farklı ayın finansal durumunu karşılaştırır (Örn: Mart vs Nisan)."""
    try:
        m1_data = await get_monthly_summary(year1, month1)
        m2_data = await get_monthly_summary(year2, month2)
    except Exception as e:
        return {"error": f"Ay verileri alınırken hata oluştu: {e}"}

    income_diff = m2_data["total_income"] - m1_data["total_income"]
    expense_diff = m2_data["total_expense"] - m1_data["total_expense"]
    net_diff = m2_data["net_balance"] - m1_data["net_balance"]

    return {
        "period_1": f"{year1}-{month1:02d}",
        "period_2": f"{year2}-{month2:02d}",
        "changes": {
            "income_change": round(income_diff, 2),
            "expense_change": round(expense_diff, 2),
            "net_balance_change": round(net_diff, 2)
        },
        "analysis": "Harcamalar arttı" if expense_diff > 0 else "Harcamalar azaldı",
        "raw_data": {
            "period_1": m1_data,
            "period_2": m2_data
        }
    }