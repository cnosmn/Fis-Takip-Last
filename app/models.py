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
    kdv: Mapped[list["Vat"]] = relationship(cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipts.id"))
    ad: Mapped[str]
    adet: Mapped[Decimal | None] = mapped_column(Numeric(10,3))
    tutar: Mapped[Decimal] = mapped_column(Numeric(12,2))

class Vat(Base):
    __tablename__="vats"
    id: Mapped[int] = mapped_column(primary_key=True)
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipts.id"))
    oran: Mapped[Decimal] = mapped_column(Numeric(5,2))
    tutar: Mapped[Decimal] = mapped_column(Numeric(12,2))

