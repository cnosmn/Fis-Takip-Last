import shutil
import uuid
from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import config
from app.db import get_db,init_db,save_receipt
from app.models import Receipt
from app.schemas import ReceiptData, ReceiptOut
from app.validators import validate
from app.vlm_client import parse_receipt


app = FastAPI(title="Fiş Takip API", version="0.1.0")
Path(config.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
init_db()  # Veritabanını başlat

@app.post("/receipts",response_model=ReceiptOut)
def fis_yukle(dosya:UploadFile=File(...), db: Session = Depends(get_db)):
    if dosya.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, 
            detail="Sadece JPEG ve PNG formatları desteklenmektedir.")
    yol = Path(config.UPLOAD_DIR) / f"{uuid.uuid4().hex}{Path(dosya.filename).suffix.lower()}.jpg"
    with open (yol,"wb") as f:
        shutil.copyfileobj(dosya.file,f)
    try :
        veri = parse_receipt(str(yol))
        hatalar = validate(veri)

    except ValueError as e:
        veri = ReceiptData()
        hatalar = [f"VLM çıktısı okunamadı: {type(e).__name__}"]
    return save_receipt(db, veri, hatalar, str(yol), config.VLM_MODEL)

@app.get("/receipts",response_model=list[ReceiptOut])
def listele(
    tarih_bas:date|None = None, 
    tarih_bit:date|None = None,
    kategori:str|None= None,
    durum:str|None = None,
    db: Session = Depends(get_db)
    ):
    query = select(Receipt).order_by(Receipt.id.desc())
    if tarih_bas:
        query = query.where(Receipt.tarih >= tarih_bas)
    if tarih_bit:
        query = query.where(Receipt.tarih <= tarih_bit)
    if kategori:
        query = query.where(Receipt.kategori == kategori)
    if durum:
        query = query.where(Receipt.durum == durum)
    return db.scalars(query).all()

@app.get("/receipts/{receipt_id}",response_model=ReceiptOut)
def detay_al(receipt_id: int, db: Session = Depends(get_db)):
    r = db.get(Receipt, receipt_id)
    if not r:
        raise HTTPException(status_code=404, detail="Fiş bulunamadı")
    return r
