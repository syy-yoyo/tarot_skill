# Tarot Skill

A Codex skill for reflective Chinese-language tarot consultations.

This skill treats tarot as a symbolic reflection tool rather than deterministic fortune-telling. It supports deterministic card draws, spread selection, Chinese interpretation guidance, safety boundaries, and imported Rider-Waite style source meanings.

## What It Includes

- `tarot/SKILL.md`: core workflow, trigger description, reading rules, and resource map.
- `tarot/scripts/draw-cards.py`: deterministic card drawing with SHA-256 seeding.
- `tarot/scripts/import-tarot-api.py`: importer for `ekelen/tarot-api` card data.
- `tarot/references/spreads.md`: single-card, three-card, relationship, and Celtic Cross spread definitions.
- `tarot/references/safety-boundaries.md`: boundaries for medical, legal, financial, crisis, and other high-stakes topics.
- `tarot/references/interpretation-style.md`: Chinese reading tone, structure, and phrasing rules.
- `tarot/references/card-index.md`: compact 78-card Chinese/English index.
- `tarot/references/cards/*.md`: per-card source meanings generated from `ekelen/tarot-api`.
- `tarot/references/source-data/ekelen-tarot-api-card_data.json`: local source JSON used to generate card files.

## Usage

Copy or link the `tarot/` directory into your Codex skills directory, then ask Codex for a tarot consultation in Chinese.

Example prompts:

```text
帮我做一个三张牌塔罗咨询，我想看看最近工作上的卡点。
```

```text
用关系牌阵看看我和这段关系接下来怎么相处。我的数字是 42。
```

The skill will:

1. clarify the question when needed;
2. recommend a spread;
3. ask for a number as an intention seed;
4. run the draw script;
5. interpret the drawn cards in Chinese;
6. end with open reflective questions.

## Draw Script

Run from the `tarot/` directory:

```bash
python scripts/draw-cards.py --question "我和这段关系接下来怎么相处" --spread relationship --number "42"
```

Supported spreads:

- `single`
- `three-card`
- `relationship`
- `celtic-cross`

Add `--no-reversals` for upright-only readings.

The script uses:

```text
sha256(question + spread + number)
```

as a stable seed, so the same question, spread, and number produce the same draw.

## Safety Stance

This skill is for reflection, journaling, and perspective-taking. It should not provide medical, legal, financial, emergency, surveillance, manipulation, or high-impact decision advice.

For high-stakes requests, it redirects the user toward a reflective version of the question and suggests qualified help when appropriate.

## Sources

The per-card source meanings are generated from [`ekelen/tarot-api`](https://github.com/ekelen/tarot-api), which provides data parsed from A. E. Waite's public-domain _The Pictorial Key to the Tarot_.

Other design references:

- [`lawreka/ascii-tarot`](https://github.com/lawreka/ascii-tarot)
- [`searge/tarot`](https://github.com/searge/tarot)
- [`MarketingPipeline/Tarot.js`](https://github.com/MarketingPipeline/Tarot.js)

## Repository Status

This repository contains a Codex skill, not a standalone tarot app. The primary artifact is the `tarot/` skill directory.
