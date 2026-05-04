from datetime import date
from ..sheets.client import SheetsClient
from ..models import Transaction

async def add_transaction(date_str:str, description:str, category: str, amount: float, txn_type: str)-> dict:
    """Sheets'e yeni gelir/gider satırı ekler. 
    ÖNEMLİ GÜVENLİK KURALI: Bu aracı çalıştırmadan önce MUTLAKA kullanıcıya eklenecek verinin özetini sun ve 'Onaylıyor musun?' diye sor. Kullanıcı açıkça onay vermeden bu aracı ASLA çağırma.
    """
    try:
        txn = Transaction(
            date=date_str,
            description=description,
            category=category,
            amount=amount,
            type=txn_type
        )
    except Exception as e:
        return {"success": False, "message": f"Doğrulama hatası (Tarih formatı YYYY-MM-DD olmalı vb.): {e}"}

    client = SheetsClient()

    row_data = [
        txn.date.isoformat(),  # YYYY-MM-DD formatında string
        txn.description,
        txn.category,
        txn.amount,
        txn.type.value
    ]

    success = client.append_transactions(row_data)
    if success:
        return {"success": True, "message": f"'{description}' açıklamalı işlem başarıyla eklendi."}
    else:
        return {"success": False, "message": "İşlem Google Sheets'e kaydedilemedi."}