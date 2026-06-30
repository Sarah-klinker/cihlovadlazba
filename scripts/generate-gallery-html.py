import json
from collections import OrderedDict
from pathlib import Path

LABELS = {
    "obdelnikova-individualni-vyroba": "Obdélníková cihlová dlažba s individuální povrchovou úpravou · Chateau Valtice · Vinařská 100dola",
    "ctverec-pivovat-cesky-krumlov": "Čtvercová cihlová dlažba · Historický pivovar · PORT1560 · Český Krumlov",
    "obdelnik-zamek-zdar-nad-sazavou": "Obdélníková cihlová dlažba · Zámek · Žďár nad Sázavou · design Alexandra Dýcková",
    "ctverec-radnice-sklepeni-brandys-nad-labem": "Obdélníková cihlová dlažba · Sklepení radnice · Brandýs nad Labem · EHL & KOUMAR ARCHITEKTI",
    "ctverec-hrebcin-hermanuv-mestec": "Čtvercová cihlová dlažba · Hřebčín · Heřmanův Městec",
    "sestiuhelnik-hrad-rostejn": "Šestiúhelníková cihlová dlažba · Hrad Roštejn · Jakub Žák SGL Projekt",
    "obdelnik-habanske-sklepy": "Obdélníková cihlová dlažba · Habánské sklepy · Velké Bílovice",
    "sestiuhelnik-zamek-slavkov": "Šestiúhelníková cihlová dlažba · Zámek Slavkov",
    "ctverec-kaple-sv-anny-vyskov": "Čtvercová cihlová dlažba · Kaple sv. Anny · Vyškov",
    "obdelnik-restaurace": "Obdélníková cihlová dlažba · Stylová restaurace",
}

ROOT = Path(__file__).resolve().parent.parent
manifest_path = ROOT / "assets" / "cihlovadlazba" / "realizace" / "manifest.json"
out_path = ROOT / "scripts" / "gallery-snippet.html"

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
groups = OrderedDict((key, []) for key in LABELS)
for item in manifest:
    groups.setdefault(item["project"], []).append(item)

parts: list[str] = []
for project, items in groups.items():
    if not items:
        continue
    label = LABELS.get(project, project)
    parts.append('      <div class="gallery-group">')
    parts.append(f'        <h3 class="gallery-group-title">{label}</h3>')
    parts.append('        <div class="gallery">')
    for index, item in enumerate(items):
        featured = " featured" if index == 0 and len(items) > 1 else ""
        alt = label if len(items) == 1 else f"{label} — fotografie {index + 1}"
        parts.append(f'          <article class="gallery-item{featured}">')
        parts.append(
            f'            <img src="assets/cihlovadlazba/realizace/{item["file"]}" '
            f'alt="{alt}" loading="lazy" width="{item["width"]}" height="{item["height"]}" />'
        )
        parts.append("          </article>")
    parts.append("        </div>")
    parts.append("      </div>")
    parts.append("")

out_path.write_text("\n".join(parts), encoding="utf-8")
print(f"Wrote {out_path}")
