
import base64
import io
import json

from openai import OpenAI
from PIL import Image

from app import config
from app.schemas import ReceiptData
from pathlib import Path
from app.image_utils import prepare_image_b64
client = OpenAI(
    base_url=config.VLM_BASE_URL,
    api_key=config.VLM_API_KEY
)

PROMPT = """Sen bir fiş okuma sistemisin. Görseldeki fişi oku ve SADECE JSON döndür.
Şema:
{"magaza": string|null, "tarih": "YYYY-MM-DD"|null,
 "kalemler": [{"ad": string, "adet": number|null, "tutar": number}],
 "kdv": [{"oran": number, "tutar": number}],
 "toplam": number|null,
 "kategori": "market"|"yakıt"|"yemek"|"diğer"|null}
Kurallar:
- Okuyamadığın alanı , null yaz.
- Sayıları noktayla yaz (12.50), para birimi yazma.
- "tutar", kalemin satır toplamıdır.
- JSON dışında hiçbir şey yazma."""

"""
python -m scripts.test_receipt eval/test_set/fis_1.jpg
"""

def extract_json(text:str) -> dict:
    start, end = text.find("{") , text.rfind("}")
    return json.loads(text[start:end+1])

def _call_vlm(b64: str) ->str:
    resp = client.chat.completions.create(
        model = config.VLM_MODEL,
        temperature=0,
        messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (
                                    f"data:image/jpeg;base64,{b64}"
    
                                )
                            }
                        }
                    ]
                }]
                )
        # print("extract_json sonucu : ",extract_json(resp.choices[0].message.content))
    return (resp.choices[0].message.content)

def parse_receipt(image_path:str,deneme:int = 2) -> ReceiptData:
    b64 = prepare_image_b64(image_path)
    son_hata = None
    for i in range(deneme):
        try:
            return ReceiptData.model_validate(extract_json(_call_vlm(b64)))
        except ValueError as e:
            son_hata = e
    raise son_hata
   



