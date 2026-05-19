from ..sheets.client import get_client


async def delete_transaction(date_str: str, description: str, amount: float, confirmed: bool = False) -> dict:
    """Belirtilen işlemi Sheets'ten kalıcı olarak siler.
    ÖNEMLİ GÜVENLİK KURALI: Bu aracı çalıştırmadan önce MUTLAKA kullanıcıya silinecek işlemin özetini sun
    (tarih, açıklama, tutar) ve 'Onaylıyor musun?' diye sor. Kullanıcı açıkça onay vermeden bu aracı ASLA çağırma.
    confirmed parametresi kullanıcının açık onayını temsil eder; False ise işlem gerçekleştirilmez.
    """
    import re
    safe_description = re.sub(r'[\x00-\x1f\x7f]', ' ', description).strip()

    if not confirmed:
        return {
            "success": False,
            "message": (
                f"İşlem onaylanmadı. Şu kaydı silmek istiyorsunuz: "
                f"{date_str} tarihli '{safe_description}' — {amount} TL. Onaylıyor musunuz?"
            ),
        }

    client = get_client()
    row = client.find_transaction_row(date_str, description, amount)
    if row is None:
        return {"success": False, "message": "Eşleşen işlem bulunamadı. Tarih (YYYY-MM-DD), açıklama ve tutar bilgilerini kontrol edin."}

    success = client.delete_transaction_row(row)
    if success:
        return {"success": True, "message": f"'{safe_description}' açıklamalı işlem başarıyla silindi."}
    return {"success": False, "message": "İşlem Google Sheets'ten silinemedi."}
