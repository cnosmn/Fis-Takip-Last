import sys
from app.vlm_client import parse_receipt
from app.validators import validate

fis = parse_receipt(sys.argv[1])
print(fis.model_dump_json(indent=2))

hatalar = validate(fis)
print("\n--- SONUÇ ---")
print("ONAYLANDI" if not hatalar else "ONAY BEKLİYOR")
for h in hatalar:
    print(" -", h)