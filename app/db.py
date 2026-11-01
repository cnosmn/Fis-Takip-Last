from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import config
from app.models import Base, Receipt, Item, Vat
from app.schemas import ReceiptData

_args = {"check_same_thread":False} if config.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(config.DATABASE_URL, connect_args=_args)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_receipt(db,veri:ReceiptData,
                hatalar:list[str],
                gorsel_yolu:str,
                saglayici:str)-> Receipt:
    r = Receipt(
        magaza=veri.magaza,
        tarih=veri.tarih,
        toplam=veri.toplam,
        kategori=veri.kategori,
        durum="onaylandi" if not hatalar else "onay bekliyor",
        hatalar=hatalar,
        gorsel_yolu=gorsel_yolu,
        kalemler=[Item(**k.model_dump()) for k in veri.kalemler],
        kdv=[Vat(**k.model_dump()) for k in veri.kdv],
        saglayici=saglayici
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return r