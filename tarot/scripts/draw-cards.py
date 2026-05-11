#!/usr/bin/env python3
"""Draw tarot cards deterministically from a question, spread, and user number."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    slug: str
    name: str
    zh: str
    arcana: str
    suit: str | None = None


CARDS: list[Card] = [
    Card("00-the-fool", "The Fool", "愚者", "major"),
    Card("01-the-magician", "The Magician", "魔术师", "major"),
    Card("02-the-high-priestess", "The High Priestess", "女祭司", "major"),
    Card("03-the-empress", "The Empress", "皇后", "major"),
    Card("04-the-emperor", "The Emperor", "皇帝", "major"),
    Card("05-the-hierophant", "The Hierophant", "教皇", "major"),
    Card("06-the-lovers", "The Lovers", "恋人", "major"),
    Card("07-the-chariot", "The Chariot", "战车", "major"),
    Card("08-strength", "Strength", "力量", "major"),
    Card("09-the-hermit", "The Hermit", "隐士", "major"),
    Card("10-wheel-of-fortune", "Wheel of Fortune", "命运之轮", "major"),
    Card("11-justice", "Justice", "正义", "major"),
    Card("12-the-hanged-man", "The Hanged Man", "倒吊人", "major"),
    Card("13-death", "Death", "死神", "major"),
    Card("14-temperance", "Temperance", "节制", "major"),
    Card("15-the-devil", "The Devil", "恶魔", "major"),
    Card("16-the-tower", "The Tower", "高塔", "major"),
    Card("17-the-star", "The Star", "星星", "major"),
    Card("18-the-moon", "The Moon", "月亮", "major"),
    Card("19-the-sun", "The Sun", "太阳", "major"),
    Card("20-judgement", "Judgement", "审判", "major"),
    Card("21-the-world", "The World", "世界", "major"),
    Card("wands-ace", "Ace of Wands", "权杖王牌", "minor", "wands"),
    Card("wands-two", "Two of Wands", "权杖二", "minor", "wands"),
    Card("wands-three", "Three of Wands", "权杖三", "minor", "wands"),
    Card("wands-four", "Four of Wands", "权杖四", "minor", "wands"),
    Card("wands-five", "Five of Wands", "权杖五", "minor", "wands"),
    Card("wands-six", "Six of Wands", "权杖六", "minor", "wands"),
    Card("wands-seven", "Seven of Wands", "权杖七", "minor", "wands"),
    Card("wands-eight", "Eight of Wands", "权杖八", "minor", "wands"),
    Card("wands-nine", "Nine of Wands", "权杖九", "minor", "wands"),
    Card("wands-ten", "Ten of Wands", "权杖十", "minor", "wands"),
    Card("wands-page", "Page of Wands", "权杖侍从", "minor", "wands"),
    Card("wands-knight", "Knight of Wands", "权杖骑士", "minor", "wands"),
    Card("wands-queen", "Queen of Wands", "权杖王后", "minor", "wands"),
    Card("wands-king", "King of Wands", "权杖国王", "minor", "wands"),
    Card("cups-ace", "Ace of Cups", "圣杯王牌", "minor", "cups"),
    Card("cups-two", "Two of Cups", "圣杯二", "minor", "cups"),
    Card("cups-three", "Three of Cups", "圣杯三", "minor", "cups"),
    Card("cups-four", "Four of Cups", "圣杯四", "minor", "cups"),
    Card("cups-five", "Five of Cups", "圣杯五", "minor", "cups"),
    Card("cups-six", "Six of Cups", "圣杯六", "minor", "cups"),
    Card("cups-seven", "Seven of Cups", "圣杯七", "minor", "cups"),
    Card("cups-eight", "Eight of Cups", "圣杯八", "minor", "cups"),
    Card("cups-nine", "Nine of Cups", "圣杯九", "minor", "cups"),
    Card("cups-ten", "Ten of Cups", "圣杯十", "minor", "cups"),
    Card("cups-page", "Page of Cups", "圣杯侍从", "minor", "cups"),
    Card("cups-knight", "Knight of Cups", "圣杯骑士", "minor", "cups"),
    Card("cups-queen", "Queen of Cups", "圣杯王后", "minor", "cups"),
    Card("cups-king", "King of Cups", "圣杯国王", "minor", "cups"),
    Card("swords-ace", "Ace of Swords", "宝剑王牌", "minor", "swords"),
    Card("swords-two", "Two of Swords", "宝剑二", "minor", "swords"),
    Card("swords-three", "Three of Swords", "宝剑三", "minor", "swords"),
    Card("swords-four", "Four of Swords", "宝剑四", "minor", "swords"),
    Card("swords-five", "Five of Swords", "宝剑五", "minor", "swords"),
    Card("swords-six", "Six of Swords", "宝剑六", "minor", "swords"),
    Card("swords-seven", "Seven of Swords", "宝剑七", "minor", "swords"),
    Card("swords-eight", "Eight of Swords", "宝剑八", "minor", "swords"),
    Card("swords-nine", "Nine of Swords", "宝剑九", "minor", "swords"),
    Card("swords-ten", "Ten of Swords", "宝剑十", "minor", "swords"),
    Card("swords-page", "Page of Swords", "宝剑侍从", "minor", "swords"),
    Card("swords-knight", "Knight of Swords", "宝剑骑士", "minor", "swords"),
    Card("swords-queen", "Queen of Swords", "宝剑王后", "minor", "swords"),
    Card("swords-king", "King of Swords", "宝剑国王", "minor", "swords"),
    Card("pentacles-ace", "Ace of Pentacles", "星币王牌", "minor", "pentacles"),
    Card("pentacles-two", "Two of Pentacles", "星币二", "minor", "pentacles"),
    Card("pentacles-three", "Three of Pentacles", "星币三", "minor", "pentacles"),
    Card("pentacles-four", "Four of Pentacles", "星币四", "minor", "pentacles"),
    Card("pentacles-five", "Five of Pentacles", "星币五", "minor", "pentacles"),
    Card("pentacles-six", "Six of Pentacles", "星币六", "minor", "pentacles"),
    Card("pentacles-seven", "Seven of Pentacles", "星币七", "minor", "pentacles"),
    Card("pentacles-eight", "Eight of Pentacles", "星币八", "minor", "pentacles"),
    Card("pentacles-nine", "Nine of Pentacles", "星币九", "minor", "pentacles"),
    Card("pentacles-ten", "Ten of Pentacles", "星币十", "minor", "pentacles"),
    Card("pentacles-page", "Page of Pentacles", "星币侍从", "minor", "pentacles"),
    Card("pentacles-knight", "Knight of Pentacles", "星币骑士", "minor", "pentacles"),
    Card("pentacles-queen", "Queen of Pentacles", "星币王后", "minor", "pentacles"),
    Card("pentacles-king", "King of Pentacles", "星币国王", "minor", "pentacles"),
]


SPREADS: dict[str, list[str]] = {
    "single": ["核心提示"],
    "three-card": ["现在情况", "需要注意", "可以做的事"],
    "relationship": ["你的位置", "对方的位置", "你们之间的互动", "阻碍或盲点", "可尝试的行动"],
    "celtic-cross": [
        "现状",
        "挑战",
        "根基",
        "近期过去",
        "显意识目标",
        "近期发展",
        "自我位置",
        "环境影响",
        "希望与恐惧",
        "整合趋势",
    ],
}


def stable_seed(question: str, spread: str, number: str) -> int:
    material = f"{question}\n{spread}\n{number}".encode("utf-8")
    digest = hashlib.sha256(material).hexdigest()
    return int(digest[:16], 16)


def draw(question: str, spread: str, number: str, reversals: bool) -> dict:
    if spread not in SPREADS:
        allowed = ", ".join(SPREADS)
        raise SystemExit(f"Unknown spread '{spread}'. Choose one of: {allowed}")

    rng = random.Random(stable_seed(question, spread, number))
    cards = rng.sample(CARDS, len(SPREADS[spread]))
    items = []
    for position, card in zip(SPREADS[spread], cards):
        reversed_card = rng.choice([False, True]) if reversals else False
        items.append(
            {
                "position": position,
                "slug": card.slug,
                "name": card.name,
                "zh": card.zh,
                "orientation": "reversed" if reversed_card else "upright",
                "orientation_zh": "逆位" if reversed_card else "正位",
                "arcana": card.arcana,
                "suit": card.suit,
            }
        )

    return {
        "spread": spread,
        "question": question,
        "number": number,
        "seed_sha256_prefix": hashlib.sha256(f"{question}\n{spread}\n{number}".encode("utf-8")).hexdigest()[:12],
        "cards": items,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw tarot cards deterministically.")
    parser.add_argument("--question", required=True)
    parser.add_argument("--spread", required=True, choices=sorted(SPREADS))
    parser.add_argument("--number", required=True)
    parser.add_argument("--no-reversals", action="store_true")
    args = parser.parse_args()

    result = draw(args.question, args.spread, args.number, not args.no_reversals)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
