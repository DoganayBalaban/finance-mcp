from ..sheets.client import get_client
from ..models import Budget


async def create_budget(category: str, monthly_limit: float, year: int, month: int, confirmed: bool = False) -> dict:
    """Bir kategori için aylık bütçe limiti oluşturur veya günceller.
    Aynı kategori/ay/yıl kombinasyonu zaten mevcutsa limitini günceller.
    ÖNEMLİ GÜVENLİK KURALI: Bu aracı çalıştırmadan önce MUTLAKA kullanıcıya kategori, limit ve dönemi göster,
    'Onaylıyor musun?' diye sor. Kullanıcı açıkça onay vermeden bu aracı ASLA çağırma.
    confirmed parametresi kullanıcının açık onayını temsil eder; False ise işlem gerçekleştirilmez.
    """
    if monthly_limit <= 0:
        return {"success": False, "message": "Bütçe limiti sıfırdan büyük olmalıdır."}
    if not (1 <= month <= 12):
        return {"success": False, "message": "Ay değeri 1-12 arasında olmalıdır."}

    try:
        validated = Budget(category=category, monthly_limit=monthly_limit, year=year, month=month)
    except Exception as e:
        return {"success": False, "message": f"Doğrulama hatası: {e}"}

    if not confirmed:
        return {
            "success": False,
            "message": (
                f"İşlem onaylanmadı. {year}-{month:02d} dönemi için '{validated.category}' kategorisine "
                f"{monthly_limit} TL bütçe limiti belirlenecek. Onaylıyor musunuz?"
            ),
        }

    client = get_client()
    success = client.upsert_budget(validated.category, year, month, monthly_limit)
    if success:
        return {"success": True, "message": f"'{validated.category}' kategorisi için {year}-{month:02d} dönemi bütçesi {monthly_limit} TL olarak kaydedildi."}
    return {"success": False, "message": "Bütçe Google Sheets'e kaydedilemedi."}
