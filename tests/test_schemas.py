from app.schemas import ReceiptData

r = ReceiptData.model_validate({
    "magaza":"Migros",
    "tarih":"2026-10-01",
    "toplam":"45.90"
    })
print(r)
# ReceiptData.model_validate({"tarih":"dün"})   -> hata verir 