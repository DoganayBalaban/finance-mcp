# src/finance_mcp/tools/report.py
import os
from .balance import get_monthly_summary
from .spending import get_spending_by_category
from .budget import check_budget_status

async def generate_monthly_report(year: int, month: int) -> dict:
    """Ayın tüm finansal verilerini toplayıp yerel bir Markdown (.md) dosyası olarak kaydeder."""
    summary = await get_monthly_summary(year, month)
    spending = await get_spending_by_category(year, month)
    budget = await check_budget_status(year, month)

    # Rapor içeriğini Markdown formatında oluştur
    report_content = f"# {year}-{month:02d} Kişisel Finans Raporu 💰\n\n"
    
    report_content += f"## 📊 Genel Özet\n"
    report_content += f"- **Toplam Gelir:** {summary['total_income']} TL\n"
    report_content += f"- **Toplam Gider:** {summary['total_expense']} TL\n"
    report_content += f"- **Net Bakiye:** {summary['net_balance']} TL\n"
    report_content += f"- **Tasarruf Oranı:** %{summary['savings_rate']}\n\n"

    report_content += f"## 🍕 En Çok Harcama Yapılan Kategoriler (Top 5)\n"
    for item in spending:
        report_content += f"- **{item['category']}:** {item['total']} TL (%{item['percentage']})\n"

    report_content += f"\n## 🚨 Bütçe ve Limit Durumu\n"
    for b in budget:
        status_emoji = "✅" if b['status'] == "ok" else ("⚠️" if b['status'] == "warning" else "❌")
        report_content += f"- {status_emoji} **{b['category']}**: Limit {b['limit']} TL | Harcanan: {b['spent']} TL | Kalan: {b['remaining']} TL\n"

    # reports klasörünü ana dizinde oluştur ve dosyayı kaydet
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    file_path = os.path.join(reports_dir, f"finance_report_{year}_{month:02d}.md")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return {
        "success": True,
        "message": f"Rapor başarıyla oluşturuldu ve kaydedildi.",
        "file_path": file_path
    }