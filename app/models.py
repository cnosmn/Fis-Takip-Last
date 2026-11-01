from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import JSON, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship , DeclarativeBase

class Base(DeclarativeBase):
    pass

class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    magaza: Mapped[str | None]
    tarih: Mapped[date | None]
    durum: Mapped[str] = mapped_column(default="onay bekliyor")
    hatalar : Mapped[list] = mapped_column(JSON, default=list)
    gorsel_yolu: Mapped[str | None]
    saglayici: Mapped[str ]
    olusturma_zamani: Mapped[datetime] = mapped_column(default=datetime.now)
    toplam: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    kategori: Mapped[str | None]
    kalemler: Mapped[list["Item"]] = relationship(cascade="all, delete-orphan")
    kdv: Mapped[list["Vat"]] = relationship(back_populates="receipt", cascade="all, delete-orphan")
