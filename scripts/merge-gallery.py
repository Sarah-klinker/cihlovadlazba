import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html_path = ROOT / "realizace.html"
snippet_path = ROOT / "scripts" / "gallery-snippet.html"

html = html_path.read_text(encoding="utf-8")
snippet = snippet_path.read_text(encoding="utf-8")
html = re.sub(
    r'(<div class="wrap gallery-stack">).*?(</div>\s*</section>)',
    rf"\1\n{snippet}    \2",
    html,
    count=1,
    flags=re.DOTALL,
)
html_path.write_text(html, encoding="utf-8")
print("Updated gallery in realizace.html")
