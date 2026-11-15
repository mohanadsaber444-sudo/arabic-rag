import re
import unicodedata

_DIACRITICS = re.compile("[\u064b-\u0652\u0670]")
_TATWEEL = "\u0640"
_ALEF = str.maketrans({"\u0623": "\u0627", "\u0625": "\u0627", "\u0622": "\u0627", "\u0671": "\u0627"})
_YA = str.maketrans({"\u0649": "\u064a"})
_DIGITS = str.maketrans("\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669", "0123456789")
_SPACES = re.compile(r"[ \t]+")
_BLANK_LINES = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    # NFKC converts Arabic presentation forms (common in PDFs) to normal letters
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\u00a0", " ")
    text = re.sub(r"-\n(?=\w)", "", text)  # join words split by a hyphen at line end
    text = _SPACES.sub(" ", text)
    text = _BLANK_LINES.sub("\n\n", text)
    return text.strip()


def normalize_for_embedding(text: str) -> str:
    text = clean_text(text)
    text = text.replace(_TATWEEL, "")
    text = _DIACRITICS.sub("", text)
    text = text.translate(_ALEF).translate(_YA).translate(_DIGITS)
    return text