import unicodedata

import pymupdf
from pypdf import PdfReader

PDF = "tests/fixtures/05_sla_support_policy_ar.pdf"

CORRECT = {
    "alisdar": "\u0627\u0644\u0625\u0635\u062f\u0627\u0631",  # version
    "ila": "\u0625\u0644\u0649",  # to
    "alfanni": "\u0627\u0644\u0641\u0646\u064a",  # the technical
    "iltizamat": "\u0627\u0644\u062a\u0632\u0627\u0645\u0627\u062a",  # commitments
    "alsharika": "\u0627\u0644\u0634\u0631\u0643\u0629",  # the company
}


def norm(text):
    return unicodedata.normalize("NFKC", text)


with pymupdf.open(PDF) as doc:
    mu = norm(" ".join(w[4] for p in doc for w in p.get_text("words")))
    py = norm(" ".join(p.extract_text() for p in PdfReader(PDF).pages))

print("word        MuPDF  pypdf   (count of correct spelling in the whole file)")
for name, word in CORRECT.items():
    print(f"{name:12}{mu.count(word):5}{py.count(word):7}")