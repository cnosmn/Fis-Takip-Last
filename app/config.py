import os
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

vlm_base_url = os.getenv("VLM_BASE_URL", "https://localhost:11434/v1")
vlm_api_key = os.getenv("VLM_API_KEY", "ollama")
vlm_model = os.getenv("VLM_MODEL","qwen2.5vl:3b")

TOPLAM_TOLERANS = Decimal("0.05")
GECERLI_KDV_ORANLARI = [Decimal(x) for x in (0,1,10,20)]

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///fis_takip.db")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

