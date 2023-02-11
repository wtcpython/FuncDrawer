"""
    语言转换文件
"""
import json
import tempfile
from pathlib import Path

tmp_dir = list(Path(tempfile.gettempdir()).glob("_MEI*"))
if tmp_dir:
    tmp_path = tmp_dir[0]
else:
    tmp_path = Path("./")

with open("./settings.json", encoding="UTF-8") as f:
    settings: dict = json.load(f)
    LANG = settings["language"]
path = Path(tmp_path/f"language/{LANG}.json")
if path.exists():
    with open(path, encoding="UTF-8") as g:
        lang_pack = json.load(g)
else:
    LANG = "English"


def tras(text: str) -> str:
    """
    语言转换
    """
    if LANG == "English":
        return text
    if text not in lang_pack:
        print(f"{text}未被翻译！")
        return text
    return lang_pack[text]
