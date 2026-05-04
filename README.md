# Finance MCP Server 💰

Google Sheets üzerinden kişisel gelir/gider verilerini okuyabilen ve yazabilen, yapay zeka (Claude vb.) destekli bir finansal analiz MCP (Model Context Protocol) sunucusu.

## Özellikler
- 📊 **Aylık Özet:** Toplam gelir, gider ve net bakiye hesaplama.
- 🍕 **Kategori Analizi:** Harcamaların kategorilere göre yüzdelik dağılımı.
- 🚨 **Bütçe Kontrolü:** Belirlenen limitlerin aşılıp aşılmadığını kontrol etme.
- 🔮 **Tasarruf Tahmini:** Geçmiş 3 aya bakarak gelecek ay için birikim tahmini.
- ✍️ **İşlem Ekleme:** Doğrudan sohbet üzerinden Sheets'e yeni gelir/gider ekleme.

## Kurulum
1. Python 3.11+ yüklü olduğundan emin olun.
2. Repoyu klonlayın ve sanal ortam oluşturun:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .