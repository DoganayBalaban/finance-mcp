from ..sheets.client import get_client
from ..models import Transaction


async def edit_transaction(
    date_str: str,
    description: str,
    amount: float,
    new_date_str: str | None = None,
    new_description: str | None = None,
    new_category: str | None = None,
    new_amount: float | None = None,
    new_type: str | None = None,
    confirmed: bool = False,
) -> dict:
    """Mevcut bir işlemin alanlarını günceller. Sadece belirtilen new_* alanları değişir.
    İşlem; date_str, description ve amount üçlüsüyle benzersiz olarak tanımlanır.
    ÖNEMLİ GÜVENLİK KURALI: Bu aracı çalıştırmadan önce MUTLAKA kullanıcıya mevcut ve yeni değerleri
    yan yana göster, 'Onaylıyor musun?' diye sor. Kullanıcı açıkça onay vermeden bu aracı ASLA çağırma.
    confirmed parametresi kullanıcının açık onayını temsil eder; False ise işlem gerçekleştirilmez.
    """
    if not confirmed:
        changes = []
        if new_date_str:
            changes.append(f"tarih → {new_date_str}")
        if new_description:
            changes.append(f"açıklama → {new_description}")
        if new_category:
            changes.append(f"kategori → {new_category}")
        if new_amount is not None:
            changes.append(f"tutar → {new_amount} TL")
        if new_type:
            changes.append(f"tür → {new_type}")
        return {
            "success": False,
            "message": (
                f"İşlem onaylanmadı. '{description}' ({date_str}, {amount} TL) kaydında şu değişiklikler yapılacak: "
                f"{', '.join(changes) if changes else 'değişiklik yok'}. Onaylıyor musunuz?"
            ),
        }

    client = get_client()
    row = client.find_transaction_row(date_str, description, amount)
    if row is None:
        return {"success": False, "message": "Eşleşen işlem bulunamadı. Tarih (YYYY-MM-DD), açıklama ve tutar bilgilerini kontrol edin."}

    ws = client.gc.open_by_key(client.sheet_id).worksheet("Transactions")
    existing = ws.row_values(row)
    if len(existing) < 5:
        return {"success": False, "message": "Mevcut satır okunamadı, beklenmedik format."}

    final_date = new_date_str or existing[0]
    final_description = new_description or existing[1]
    final_category = new_category or existing[2]
    final_amount = new_amount if new_amount is not None else float(existing[3])
    final_type = new_type or existing[4]

    try:
        txn = Transaction(
            date=final_date,
            description=final_description,
            category=final_category,
            amount=final_amount,
            type=final_type,
        )
    except Exception as e:
        return {"success": False, "message": f"Doğrulama hatası: {e}"}

    row_data = [txn.date.isoformat(), txn.description, txn.category, txn.amount, txn.type.value]
    success = client.update_transaction_row(row, row_data)
    if success:
        return {"success": True, "message": f"'{txn.description}' açıklamalı işlem başarıyla güncellendi."}
    return {"success": False, "message": "İşlem Google Sheets'te güncellenemedi."}
