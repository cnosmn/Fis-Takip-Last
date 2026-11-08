from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field,ConfigDict

"""
sozluk {
    "magaza": "A101",
    "tarih": "2023-01-01",}
    sozluk["magaza"]
    sqlalchemy nesnesi 
    sozluk.magaza
"""
class ItemData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ad: str
    adet: Decimal | None = None
    tutar: Decimal
    
class VatData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    oran: Decimal
    tutar: Decimal
    
class ReceiptData(BaseModel):
    magaza: str | None = None
    tarih: date | None = None
    kalemler: list[ItemData] = Field(default_factory=list)
    kdv: list[VatData] = Field(default_factory=list)
    toplam: Decimal | None = None
    kategori: str | None = None

class ReceiptOut(BaseModel):
    #api nin dışarı verdiği fiş (veritabanından üretilir)
    model_config = ConfigDict(from_attributes=True)
    id: int
    magaza: str | None = None
    tarih: date | None = None
    toplam: Decimal | None
    kategori: str | None
    durum: str
    hatalar: list[str]
    gorsel_yolu: str
    saglayici: str
    olusturma_zamani: datetime
    kalemler: list[ItemData]
    kdv: list[VatData]
    