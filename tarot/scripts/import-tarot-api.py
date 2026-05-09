#!/usr/bin/env python3
"""Import ekelen/tarot-api card_data.json into per-card Markdown files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CARD_ORDER = [
    ("00-the-fool", "The Fool", "愚者"),
    ("01-the-magician", "The Magician", "魔术师"),
    ("02-the-high-priestess", "The High Priestess", "女祭司"),
    ("03-the-empress", "The Empress", "皇后"),
    ("04-the-emperor", "The Emperor", "皇帝"),
    ("05-the-hierophant", "The Hierophant", "教皇"),
    ("06-the-lovers", "The Lovers", "恋人"),
    ("07-the-chariot", "The Chariot", "战车"),
    ("08-strength", "Strength", "力量"),
    ("09-the-hermit", "The Hermit", "隐士"),
    ("10-wheel-of-fortune", "Wheel of Fortune", "命运之轮"),
    ("11-justice", "Justice", "正义"),
    ("12-the-hanged-man", "The Hanged Man", "倒吊人"),
    ("13-death", "Death", "死神"),
    ("14-temperance", "Temperance", "节制"),
    ("15-the-devil", "The Devil", "恶魔"),
    ("16-the-tower", "The Tower", "高塔"),
    ("17-the-star", "The Star", "星星"),
    ("18-the-moon", "The Moon", "月亮"),
    ("19-the-sun", "The Sun", "太阳"),
    ("20-judgement", "Judgement", "审判"),
    ("21-the-world", "The World", "世界"),
    ("wands-ace", "Ace of Wands", "权杖王牌"),
    ("wands-two", "Two of Wands", "权杖二"),
    ("wands-three", "Three of Wands", "权杖三"),
    ("wands-four", "Four of Wands", "权杖四"),
    ("wands-five", "Five of Wands", "权杖五"),
    ("wands-six", "Six of Wands", "权杖六"),
    ("wands-seven", "Seven of Wands", "权杖七"),
    ("wands-eight", "Eight of Wands", "权杖八"),
    ("wands-nine", "Nine of Wands", "权杖九"),
    ("wands-ten", "Ten of Wands", "权杖十"),
    ("wands-page", "Page of Wands", "权杖侍从"),
    ("wands-knight", "Knight of Wands", "权杖骑士"),
    ("wands-queen", "Queen of Wands", "权杖王后"),
    ("wands-king", "King of Wands", "权杖国王"),
    ("cups-ace", "Ace of Cups", "圣杯王牌"),
    ("cups-two", "Two of Cups", "圣杯二"),
    ("cups-three", "Three of Cups", "圣杯三"),
    ("cups-four", "Four of Cups", "圣杯四"),
    ("cups-five", "Five of Cups", "圣杯五"),
    ("cups-six", "Six of Cups", "圣杯六"),
    ("cups-seven", "Seven of Cups", "圣杯七"),
    ("cups-eight", "Eight of Cups", "圣杯八"),
    ("cups-nine", "Nine of Cups", "圣杯九"),
    ("cups-ten", "Ten of Cups", "圣杯十"),
    ("cups-page", "Page of Cups", "圣杯侍从"),
    ("cups-knight", "Knight of Cups", "圣杯骑士"),
    ("cups-queen", "Queen of Cups", "圣杯王后"),
    ("cups-king", "King of Cups", "圣杯国王"),
    ("swords-ace", "Ace of Swords", "宝剑王牌"),
    ("swords-two", "Two of Swords", "宝剑二"),
    ("swords-three", "Three of Swords", "宝剑三"),
    ("swords-four", "Four of Swords", "宝剑四"),
    ("swords-five", "Five of Swords", "宝剑五"),
    ("swords-six", "Six of Swords", "宝剑六"),
    ("swords-seven", "Seven of Swords", "宝剑七"),
    ("swords-eight", "Eight of Swords", "宝剑八"),
    ("swords-nine", "Nine of Swords", "宝剑九"),
    ("swords-ten", "Ten of Swords", "宝剑十"),
    ("swords-page", "Page of Swords", "宝剑侍从"),
    ("swords-knight", "Knight of Swords", "宝剑骑士"),
    ("swords-queen", "Queen of Swords", "宝剑王后"),
    ("swords-king", "King of Swords", "宝剑国王"),
    ("pentacles-ace", "Ace of Pentacles", "星币王牌"),
    ("pentacles-two", "Two of Pentacles", "星币二"),
    ("pentacles-three", "Three of Pentacles", "星币三"),
    ("pentacles-four", "Four of Pentacles", "星币四"),
    ("pentacles-five", "Five of Pentacles", "星币五"),
    ("pentacles-six", "Six of Pentacles", "星币六"),
    ("pentacles-seven", "Seven of Pentacles", "星币七"),
    ("pentacles-eight", "Eight of Pentacles", "星币八"),
    ("pentacles-nine", "Nine of Pentacles", "星币九"),
    ("pentacles-ten", "Ten of Pentacles", "星币十"),
    ("pentacles-page", "Page of Pentacles", "星币侍从"),
    ("pentacles-knight", "Knight of Pentacles", "星币骑士"),
    ("pentacles-queen", "Queen of Pentacles", "星币王后"),
    ("pentacles-king", "King of Pentacles", "星币国王"),
]

ALIASES = {
    "Fortitude": "Strength",
    "Wheel Of Fortune": "Wheel of Fortune",
    "The Last Judgment": "Judgement",
}


def normalize_name(name: str) -> str:
    return ALIASES.get(name, name)


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def render_card(slug: str, english: str, zh: str, source: dict) -> str:
    source_name = source["name"]
    type_label = "Major Arcana" if source["type"] == "major" else f"Minor Arcana / {source.get('suit', '')}"
    lines = [
        f"# {english} / {zh}",
        "",
        f"- Slug: `{slug}`",
        f"- Source name: {source_name}",
        f"- Type: {type_label}",
        f"- Source short name: `{source.get('name_short', '')}`",
        "",
        "## Upright Meaning",
        "",
        compact(source.get("meaning_up", "")),
        "",
        "## Reversed Meaning",
        "",
        compact(source.get("meaning_rev", "")),
        "",
        "## Pictorial Description",
        "",
        compact(source.get("desc", "")),
        "",
        "## Reading Note",
        "",
        "Use this source text as symbolic material. Translate, soften, and contextualize it in Chinese; do not copy fatalistic or high-stakes claims directly into the reading.",
        "",
        "Source: `ekelen/tarot-api/static/card_data.json`, based on A. E. Waite's public-domain _The Pictorial Key to the Tarot_.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    data = json.loads(args.json.read_text(encoding="utf-8"))
    by_name = {normalize_name(card["name"]): card for card in data["cards"]}
    args.out.mkdir(parents=True, exist_ok=True)

    missing = []
    for slug, english, zh in CARD_ORDER:
        source = by_name.get(english)
        if source is None:
            missing.append(english)
            continue
        (args.out / f"{slug}.md").write_text(render_card(slug, english, zh, source), encoding="utf-8", newline="\n")

    if missing:
        raise SystemExit(f"Missing cards: {', '.join(missing)}")

    print(f"Imported {len(CARD_ORDER)} cards into {args.out}")


if __name__ == "__main__":
    main()
