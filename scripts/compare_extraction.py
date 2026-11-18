from pathlib import Path

import pymupdf

PDF = "tests/fixtures/05_sla_support_policy_ar.pdf"
OUT = Path("data/inspect")
OUT.mkdir(parents=True, exist_ok=True)

with pymupdf.open(PDF) as doc:
    page = doc[0]
    a = page.get_text("text")
    b = "\n".join(blk[4] for blk in page.get_text("blocks"))
    # words: (x0, y0, x1, y1, word, block_no, line_no, word_no)
    lines = {}
    for w in page.get_text("words"):
        lines.setdefault((w[5], w[6]), []).append(w)
    c = "\n".join(
        " ".join(w[4] for w in sorted(ws, key=lambda w: -w[0]))  # right to left
        for _, ws in sorted(lines.items())
    )

(OUT / "cmp_text.txt").write_text(a, encoding="utf-8")
(OUT / "cmp_blocks.txt").write_text(b, encoding="utf-8")
(OUT / "cmp_words_rtl.txt").write_text(c, encoding="utf-8")
print("saved 3 files")