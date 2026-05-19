from datetime import date
from ..sheets.client import get_client
from ..models import Transaction

async def add_transaction(date_str:str, description:str, category: str, amount: float, txn_type: str, confirmed: bool = False)-> dict:
    """Sheets'e yeni gelir/gider satırı ekler.
    ÖNEMLİ GÜVENLİK KURALI: Bu aracı çalıştırmadan önce MUTLAKA kullanıcıya eklenecek verinin özetini sun ve 'Onaylıyor musun?' diye sor. Kullanıcı açıkça onay vermeden bu aracı ASLA çağırma.
    confirmed parametresi kullanıcının açık onayını temsil eder; False ise işlem gerçekleştirilmez.
    """
    if not confirmed:
        return {
            "success": False,
            "message": f"İşlem onaylanmadı. Lütfen şu işlemi onaylayın: {date_str} tarihinde '{description}' ({category}) — {amount} TL [{txn_type}]. Onaylıyor musunuz?"
        }
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

    client = get_client()

    row_data = [
        txn.date.isoformat(),  # YYYY-MM-DD formatında string
        txn.description,
        txn.category,
        txn.amount,
        txn.type.value
    ]

    success = client.append_transactions(row_data)
    if success:
        return {"success": True, "message": f"'{txn.description}' açıklamalı işlem başarıyla eklendi."}
    else:
        return {"success": False, "message": "İşlem Google Sheets'e kaydedilemedi."}