
from datetime import date
from app import config
from app.schemas import ReceiptData


def validate(receipt: ReceiptData) -> list[str]:
    errors = []

    if receipt.toplam is None:
        errors.append("Toplam Okunamadı")
    if not receipt.magaza:
        errors.append("Mağaza adı okunamadı.")

    if receipt.tarih is None:
        errors.append("Fiş tarihi okunamadı.")
    elif receipt.tarih > date.today():
        errors.append("Fiş tarihi gelecekte olamaz.")

    if receipt.toplam is not None and receipt.kalemler:
        fark = abs(sum(k.tutar for k in receipt.kalemler) - receipt.toplam)
        if fark >= config.TOPLAM_TOLERANS:
            errors.append(f"Kalem toplamı tutmuyor (fark: {fark})")

    if receipt.toplam is None or receipt.toplam <= 0:
        errors.append("Toplam tutar geçersiz.")

    for vat in receipt.kdv:
        if vat.oran is not None:
            if vat.oran not in config.GECERLI_KDV_ORANLARI:
                errors.append("KDV oranı izin verilen listede değil.")

    return errors
