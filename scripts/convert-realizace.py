"""Convert realizace photos to optimized WebP for web gallery."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from PIL import Image

SOURCE = Path(r"C:\Users\skocourkova\Documents\Marketing\Web,domény\cihlovadlazba\realizace")
ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "cihlovadlazba" / "realizace"
MAX_WIDTH = 1400
QUALITY = 82
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

PROJECT_LABELS: dict[str, str] = {
    "obdelnik habanske sklepy": "Habánské sklepy · Velké Bílovice",
    "obdelnik zamek zdar nad sazavou": "Zámek · Žďár nad Sázavou",
    "obdelnikova - individualni vyroba": "Chateau Valtice · Vinařská 100dola",
    "sestiuhelnik hrad roztejn": "Hrad Rožtejn",
    "sestiuhelnik zamek slavkov": "Zámek Slavkov",
    "ctverec hrebcin hermanuv mestec": "Hřebčín · Heřmanův Městec",
    "ctverec pivovat cesky krumlov": "Pivovar · Český Krumlov",
    "ctverec radnice sklepeni brandys nad labem": "Sklepení radnice · Brandýs nad Labem",
    "ctverec_kaple sv. anny vyskov": "Kaple sv. Anny · Vyškov",
    "obdelnik_restaurace": "Stylová restaurace",
}


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    return ascii_text.strip("-")


def project_key(folder_name: str, file_name: str) -> str:
    if folder_name == ".":
        return slugify(Path(file_name).stem)
    return slugify(folder_name)


def project_label(key: str, folder_name: str, file_name: str) -> str:
    if key in PROJECT_LABELS:
        return PROJECT_LABELS[key]
    if folder_name != ".":
        return folder_name
    return Path(file_name).stem


def optimize_image(src: Path, dest: Path) -> tuple[int, int, int]:
    with Image.open(src) as img:
        img = img.convert("RGB")
        width, height = img.size
        if width > MAX_WIDTH:
            new_height = round(height * MAX_WIDTH / width)
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
            width, height = img.size
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, "WEBP", quality=QUALITY, method=6)
    return width, height, dest.stat().st_size


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str | int]] = []

    files = sorted(
        p
        for p in SOURCE.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )

    counters: dict[str, int] = {}

    for src in files:
        rel = src.relative_to(SOURCE)
        folder = "." if rel.parent == Path(".") else str(rel.parent)
        key = project_key(folder, src.name)
        counters[key] = counters.get(key, 0) + 1
        index = counters[key]
        out_name = f"{key}-{index:02d}.webp"
        dest = DEST / out_name

        width, height, size = optimize_image(src, dest)
        label = project_label(key, folder, src.name)
        manifest.append(
            {
                "file": out_name,
                "label": label,
                "project": key,
                "width": width,
                "height": height,
                "bytes": size,
                "source": str(rel),
            }
        )
        print(f"{rel} -> {out_name} ({size // 1024} KB, {width}x{height})")

    manifest_path = DEST / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    total_kb = sum(item["bytes"] for item in manifest) // 1024
    print(f"\nConverted {len(manifest)} images, total {total_kb} KB")


if __name__ == "__main__":
    main()
