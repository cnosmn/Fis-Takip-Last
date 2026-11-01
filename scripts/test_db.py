import sys
from app import config
from app.db import SessionLocal, init_db, save_receipt
from app.validators import validate
from app. vlm_client import parse_receipt

init_db()
veri = parse_receipt(sys.argv[1])
hatalar = validate(veri)
with SessionLocal() as db:
    r = save_receipt(db, veri, hatalar, sys.argv[1], config.SAGLAYICI)
    print(f"Fiş kaydedildi ID: {r.id} durum : {r.durum} toplam: {r.toplam}")
    