<div align="center">

# ✨ web-ui-copy

### Pixel-perfect UI cloning Agent Skill

**Exact clone · Style copy · Font fidelity · Layout parity · Screenshot recreation**

<br />

[中文文档](README.zh-CN.md)

</div>

---

### 🚀 What is this?

`web-ui-copy` is an **Agent Skill** for copying frontend UI with high visual fidelity. It turns UI cloning into a repeatable agent workflow: capture the source, mirror the assets, preserve the visual system, and validate the result like a frontend engineer.

It is designed for two common but very different tasks:

1. **Exact clone** — copy a live webpage as closely as possible, including content, fonts, layout, colors, images, and framework assets.
2. **Style copy with new content** — keep the source page's visual system exactly, but replace the text/content with your own.

### 🤖 Built as Agent Skills

`web-ui-copy` packages a battle-tested UI cloning methodology into an **Agent Skill**:

- clear mode selection for exact clone, style copy, screenshot recreation, and clone debugging;
- source-mirror-first workflow for pixel-level fidelity;
- computed-style validation for fonts, spacing, colors, and layout;
- reusable instructions that can be dropped into agent platforms, coding assistants, and automation pipelines.

### ⚡ Core modes

| Mode | What it does |
| --- | --- |
| 🧬 **Exact Clone** | Mirror the original page source and assets for maximum fidelity. |
| 🎨 **Style Copy** | Preserve typography, spacing, colors, layout, and components while changing content. |
| 🖼️ **Screenshot Recreation** | Recreate UI from a screenshot or design image when source is unavailable. |
| 🔍 **Clone Debugging** | Compare original vs clone using computed styles, resources, and browser rendering. |

### 🧰 Included scripts

This is not just a prompt. `web-ui-copy` ships with practical scripts for repeatable UI cloning work:

| Script | Purpose |
| --- | --- |
| `scripts/mirror_webpage.py` | Capture HTML and mirror visual assets into a local `site/` tree. |
| `scripts/style_snapshot.js` | Capture computed styles and bounding boxes for selected DOM nodes. |
| `scripts/compare_style_snapshots.py` | Compare source vs copy snapshots and report style/geometry drift. |
| `scripts/extract_layout_blueprint.py` | Convert screenshot regions into a layout blueprint JSON. |

Quick mirror:

```bash
python scripts/mirror_webpage.py --url https://example.com --out captures/example
python3 -m http.server 8080 -d captures/example/site
```

Quick style QA:

```bash
python scripts/compare_style_snapshots.py \
  --source source-style.json \
  --copy copy-style.json \
  --out style-diff.json \
  --ignore-text
```

### 🧠 Why this skill exists

Handwritten UI recreation often looks close at first, but fails on details:

- heading resets are missing;
- fonts silently fall back;
- colors and gradients are slightly off;
- framework hydration changes the DOM;
- responsive breakpoints choose a different layout;
- cards, chips, buttons, and shadows drift by a few pixels.

`web-ui-copy` fixes this by preferring **source mirror mode** for exact clones.

### 🧬 Exact clone workflow

For exact clones, the skill follows a source-mirror-first workflow:

1. Capture the server-rendered HTML.
2. Mirror CSS, JavaScript, images, SVGs, videos, fonts, manifests, and framework runtime assets.
3. Preserve original paths and hashed asset filenames where possible.
4. Remove only non-visual analytics/beacon scripts.
5. Load the local copy and fix missing resources or console errors.
6. Validate key elements with computed styles and bounding boxes.

### 🎨 Style copy workflow

For style-copy tasks, the goal is:

> **Different content, same visual system.**

The skill keeps:

- same `@font-face` and font files;
- same font family, size, weight, line-height, and letter-spacing;
- same CSS variables, resets, and breakpoints;
- same component classes and DOM structure where possible;
- same colors, backgrounds, gradients, radius, shadows, spacing, and layout rules.

Then it replaces only semantic content:

- headings;
- paragraphs;
- card text;
- nav labels;
- CTA labels;
- lists;
- metadata;
- framework props or JSON data sources when needed.

### 🪄 Example prompts

#### 1. Exact clone

```text
Use web-ui-copy to clone https://example.com exactly.
Keep all content, fonts, colors, images, spacing, and layout identical.
```

#### 2. Style copy with new content

```text
Use web-ui-copy to copy the style of https://example.com,
but replace the content with my AI SaaS landing page copy.
Fonts, layout, cards, buttons, and spacing must stay identical.
```

#### 3. Debug clone mismatch

```text
Use web-ui-copy to compare my local clone with the original page.
Fix mismatched fonts, chip colors, card backgrounds, and spacing.
```

### ✅ Quality checklist

A good clone should pass these checks:

- no missing visual CSS/JS/image/font/video assets;
- no console errors caused by missing local modules;
- key headings use the same computed font styles;
- cards, chips, buttons, and sections match source geometry;
- responsive breakpoints match the original viewport behavior;
- expected differences are documented when content or media is intentionally changed.

### 📦 Repository structure

```text
web-ui-copy/
├── README.md
├── README.zh-CN.md
├── SKILL.md
└── scripts/
    ├── mirror_webpage.py
    ├── style_snapshot.js
    ├── compare_style_snapshots.py
    └── extract_layout_blueprint.py
```

`SKILL.md` is the actual Agent Skill definition: the reusable workflow that tells an AI agent how to perform high-fidelity UI cloning.

`README.md` and `README.zh-CN.md` are human-facing documentation in English and Chinese.

### 🛠️ Installation

Copy this repository into your agent skills directory, or adapt `SKILL.md` into your preferred AI-agent workflow system.

Required file:

```text
SKILL.md
```

### ⚠️ Notes

- Exact fidelity depends on access to the original page and its assets.
- Some pages use A/B tests, geolocation, login-only states, live counters, or time-sensitive content; these may need to be captured or frozen.
- Screenshot-only recreation cannot guarantee exact fonts or dynamic content unless assets are provided.
- For style-copy tasks with a different language/script, font support must be verified.

---

<div align="center">

## Built for obsessive UI fidelity.

[中文文档](README.zh-CN.md)

</div>
