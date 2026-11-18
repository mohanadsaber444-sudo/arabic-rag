from pathlib import Path

from pypdf import PdfReader

OUT = Path("data/inspect")
OUT.mkdir(parents=True, exist_ok=True)

for path in sorted(Path("tests/fixtures").glob("*.pdf")):
    pages = [p.extract_text() or "" for p in PdfReader(str(path)).pages]
    text = "\n\n--- page ---\n\n".join(pages)
    (OUT / f"pypdf_{path.stem}.txt").write_text(text, encoding="utf-8")
    print(f"{path.name}: pages={len(pages)} chars={len(text)}")