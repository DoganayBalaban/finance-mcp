from ..sheets.client import SheetsClient

async def set_savings_goal(year:int, month:int, target_amount:float)->dict:
    """Google Sheets'e belirtilen ay için yeni bir tasarruf/birikim hedefi yazar."""
    client = SheetsClient()
    success = client.set_savings_goal(year,month,target_amount)
    if success:
        return {"success": True, "message": f"{year}-{month:02d} dönemi için {target_amount} TL birikim hedefi E-tabloya başarıyla kaydedildi."}
    return {"success": False, "message": "Hedef kaydedilemedi. Tabloda 'Goals' adında bir sekme olduğundan emin olun."}