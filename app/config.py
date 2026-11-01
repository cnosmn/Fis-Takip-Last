import os
from decimal import Decimal

from dotenv import load_dotenv

load_dotenv()

# --- VLM sağlayıcısı: .env içinde SAGLAYICI=yerel veya SAGLAYICI=bulut ---
SAGLAYICI = os.getenv("SAGLAYICI", "bulu").lower()

_PROFILLER = {
    "yerel": {"base_url": "http://localhost:11434/v1", "api_key": "ollama",
              "model": "qwen2.5vl:7b"},
    "bulut": {"base_url": "https://api.openai.com/v1", "api_key": "",
              "model": "gpt-4o-mini"},
}

if SAGLAYICI not in _PROFILLER:
    raise ValueError(f"SAGLAYICI 'yerel' veya 'bulut' olmalı, gelen: {SAGLAYICI!r}")

_p = _PROFILLER[SAGLAYICI]
_on = SAGLAYICI.upper()  # YEREL_ veya BULUT_ ile başlayan .env değişkenleri

VLM_BASE_URL = os.getenv(f"{_on}_BASE_URL", _p["base_url"])
VLM_API_KEY = os.getenv(f"{_on}_API_KEY", _p["api_key"])
VLM_MODEL = os.getenv(f"{_on}_MODEL", _p["model"])
VLM_TIMEOUT = float(os.getenv("VLM_TIMEOUT", "120"))

if not VLM_API_KEY:
    raise ValueError(f".env içinde {_on}_API_KEY tanımlı değil")

# Veritabanına "hangi model okudu" diye yazılan etiket (örn. "bulut:gpt-4o-mini")
SAGLAYICI_ETIKETI = f"{SAGLAYICI}:{VLM_MODEL}"

# --- Doğrulama ---
TOPLAM_TOLERANS = Decimal("0.05")
# Türkiye KDV oranları değişebilir: kullanmadan önce güncel oranları kontrol et
GECERLI_KDV_ORANLARI = [Decimal(x) for x in (0, 1, 10, 20)]

# --- Veritabanı ve dosyalar ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///fis_takip.db")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")