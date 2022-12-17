"""
    语言转换文件
"""
import json
from pathlib import Path

with open("./settings.json", encoding="UTF-8") as f:
    settings: dict = json.load(f)
    lang = settings["language"]
path = Path(f"./language/{lang}.json")
if path.exists():
    with open(path, encoding="UTF-8") as g:
        lang_pack = json.load(g)
else:
    lang = "English"


def tras(text: str) -> str:
    """
    语言转换
    """
    if lang == "English":
        return text
    if text not in lang_pack:
        print(f"{text}未被翻译！")
        return text
    return lang_pack[text]
