"""Convert remaining project images to optimized WebP."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent / "assets" / "cihlovadlazba"
QUALITY = 82

JOBS: list[tuple[str, int | None]] = [
    ("hero/dlazba_valtice_hero.jpg", 1920),
    ("o-dlazbe/vyroba_cihlovas_dlazba_1.jpg", 1400),
    ("ikony/ikona_vlevo_nahore.png", 128),
    ("ikony/ikona_prirodni_material.png", 128),
    ("ikony/ikona_remeslna_vyroba.png", 128),
    ("ikony/ikona_poradenstvi.png", 128),
    ("ikony/ikona_dostupnost.png", 128),
    ("formaty/sestiuhelnik.png", 88),
    ("logo-klinkercentrum.png", 300),
]


def convert(relative_path: str, max_width: int | None) -> None:
    source = ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)

    destination = source.with_suffix(".webp")
    with Image.open(source) as image:
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        width, height = image.size
        if max_width and width > max_width:
            new_height = round(height * max_width / width)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)

        save_kwargs: dict[str, object] = {"quality": QUALITY, "method": 6}
        if image.mode == "RGBA":
            save_kwargs["lossless"] = False

        image.save(destination, "WEBP", **save_kwargs)

    before_kb = source.stat().st_size // 1024
    after_kb = destination.stat().st_size // 1024
    print(f"{relative_path} -> {destination.name} ({before_kb} KB -> {after_kb} KB)")


def main() -> None:
    for path, max_width in JOBS:
        convert(path, max_width)


if __name__ == "__main__":
    main()
