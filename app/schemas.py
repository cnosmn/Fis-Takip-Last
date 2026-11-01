from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field

class ItemData(BaseModel):
    ad: str
    adet: Decimal | None = None
    tutar: Decimal
    
class VatData(BaseModel):
    oran: Decimal
    tutar: Decimal
    
class ReceiptData(BaseModel):
    magaza: str | None = None
    tarih: date | None = None
    kalemler: list[ItemData] = Field(default_factory=list)
    kdv: list[VatData] = Field(default_factory=list)
    toplam: Decimal | None = None
    kategori: str | None = None
