import base64
import io
from PIL import Image, ImageOps


MAX_KENAR = 1800

def prepare_image_b64(path:str) -> str:
    img = Image.open(path)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((MAX_KENAR,MAX_KENAR))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()
