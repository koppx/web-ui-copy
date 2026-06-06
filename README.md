<div align="center">

# ✨ web-ui-copy

### Pixel-perfect UI cloning Agent Skill
### 高保真网页复制 Agent Skill

**Exact clone · Style copy · Font fidelity · Layout parity · Screenshot recreation**

**一比一复制 · 风格迁移 · 字体还原 · 布局对齐 · 截图复刻**

</div>

---

## 🚀 What is this?

`web-ui-copy` is an **Agent Skill** for copying frontend UI with high visual fidelity. It turns UI cloning into a repeatable agent workflow: capture the source, mirror the assets, preserve the visual system, and validate the result like a frontend engineer.

It is designed for two common but very different tasks:

1. **Exact clone** — copy a live webpage as closely as possible, including content, fonts, layout, colors, images, and framework assets.
2. **Style copy with new content** — keep the source page's visual system exactly, but replace the text/content with your own.

## 🚀 这是什么？

`web-ui-copy` 是一个用于 **高保真复制前端页面** 的 **Agent Skill**。它把 UI 复制变成可复用的 Agent 工作流：抓取源站、镜像资源、保留视觉系统，并像前端工程师一样验证还原结果。

它主要解决两类需求：

1. **一比一复制网页**：内容、字体、排版、颜色、图片、组件、响应式都尽量和原网页一致。
2. **风格 copy，内容替换**：保留原网页的字体、版式、颜色、组件风格，但换成你自己的内容。

---

## 🤖 Built as Agent Skills / 以 Agent Skills 方式构建

`web-ui-copy` packages a battle-tested UI cloning methodology into an **Agent Skill**:

- clear mode selection for exact clone, style copy, screenshot recreation, and clone debugging;
- source-mirror-first workflow for pixel-level fidelity;
- computed-style validation for fonts, spacing, colors, and layout;
- reusable instructions that can be dropped into agent platforms, coding assistants, and automation pipelines.

`web-ui-copy` 将一套经过实战验证的 UI 复制方法封装成 **Agent Skills**：

- 明确区分一比一复制、风格 copy、截图复刻、差异修复；
- 源码镜像优先，追求像素级还原；
- 用 computed style 校验字体、间距、颜色和布局；
- 可作为 Agent 平台、Coding Assistant、自动化流水线里的复用能力。

## ⚡ Core modes / 核心模式

| Mode | English | 中文 |
| --- | --- | --- |
| 🧬 **Exact Clone** | Mirror the original page source and assets for maximum fidelity. | 镜像原网页源码和资源，实现尽量一比一还原。 |
| 🎨 **Style Copy** | Preserve typography, spacing, colors, layout, and components while changing content. | 字体、间距、颜色、布局、组件保持一致，但内容可替换。 |
| 🖼️ **Screenshot Recreation** | Recreate UI from a screenshot or design image when source is unavailable. | 只有截图或设计稿时，根据图片复刻页面。 |
| 🔍 **Clone Debugging** | Compare original vs clone using computed styles, resources, and browser rendering. | 对比原网页和复制页，修复字体、颜色、间距、资源缺失等问题。 |

---

## 🧠 Why this skill exists / 为什么需要它？

Handwritten UI recreation often looks close at first, but fails on details:

- heading resets are missing;
- fonts silently fall back;
- colors and gradients are slightly off;
- framework hydration changes the DOM;
- responsive breakpoints choose a different layout;
- cards, chips, buttons, and shadows drift by a few pixels.

手写复刻页面通常“看起来差不多”，但细节很容易翻车：

- 标题默认样式没有 reset；
- 字体没有真正加载，悄悄 fallback；
- 颜色、渐变、阴影差一点；
- 框架 hydrate 后 DOM 变了；
- 响应式断点不一致；
- 卡片、标签、按钮、间距差几像素。

`web-ui-copy` fixes this by preferring **source mirror mode** for exact clones.

`web-ui-copy` 的核心策略是：**能镜像源码就先镜像源码，不轻易手写猜测。**

---

## 🧬 Exact clone workflow / 一比一复制流程

For exact clones, the skill follows a source-mirror-first workflow:

1. Capture the server-rendered HTML.
2. Mirror CSS, JavaScript, images, SVGs, videos, fonts, manifests, and framework runtime assets.
3. Preserve original paths and hashed asset filenames where possible.
4. Remove only non-visual analytics/beacon scripts.
5. Load the local copy and fix missing resources or console errors.
6. Validate key elements with computed styles and bounding boxes.

一比一复制时，它会优先走源码镜像流程：

1. 抓取服务端渲染后的 HTML。
2. 镜像 CSS、JS、图片、SVG、视频、字体、manifest、框架运行时资源。
3. 尽量保留原始路径和 hash 文件名。
4. 只移除不影响视觉的 analytics / beacon 脚本。
5. 本地打开页面，修复缺失资源和控制台错误。
6. 用 computed style 和元素位置验证关键节点。

---

## 🎨 Style copy workflow / 风格 copy 流程

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

风格 copy 的目标是：

> **内容可以不同，但视觉系统必须一致。**

它会保留：

- 相同的 `@font-face` 和字体文件；
- 相同的字体族、字号、字重、行高、字距；
- 相同的 CSS 变量、reset、响应式断点；
- 尽量相同的组件 class 和 DOM 结构；
- 相同的颜色、背景、渐变、圆角、阴影、间距和布局规则。

然后只替换语义内容：

- 标题；
- 段落；
- 卡片文字；
- 导航文案；
- CTA 按钮文案；
- 列表；
- metadata；
- 必要时修改框架 props 或 JSON 数据源。

---

## 🪄 Example prompts / 使用示例

### 1. Exact clone / 一比一复制

```text
Use web-ui-copy to clone https://example.com exactly.
Keep all content, fonts, colors, images, spacing, and layout identical.
```

```text
用 web-ui-copy 一比一复制 https://example.com。
内容、字体、颜色、图片、间距、布局都要保持一致。
```

### 2. Style copy with new content / 风格复制但换内容

```text
Use web-ui-copy to copy the style of https://example.com,
but replace the content with my AI SaaS landing page copy.
Fonts, layout, cards, buttons, and spacing must stay identical.
```

```text
用 web-ui-copy 复制 https://example.com 的网页风格，
但内容换成我的 AI SaaS 产品介绍。
字体、排版、卡片、按钮、间距都要保持一致。
```

### 3. Debug clone mismatch / 修复复制页差异

```text
Use web-ui-copy to compare my local clone with the original page.
Fix mismatched fonts, chip colors, card backgrounds, and spacing.
```

```text
用 web-ui-copy 对比我的本地复制页和原网页。
修复字体不一致、标签颜色不一致、卡片背景不一致、间距不一致的问题。
```

---

## ✅ Quality checklist / 质量检查清单

A good clone should pass these checks:

- no missing visual CSS/JS/image/font/video assets;
- no console errors caused by missing local modules;
- key headings use the same computed font styles;
- cards, chips, buttons, and sections match source geometry;
- responsive breakpoints match the original viewport behavior;
- expected differences are documented when content or media is intentionally changed.

一个合格的复制页面应该满足：

- 没有缺失的视觉 CSS / JS / 图片 / 字体 / 视频资源；
- 没有因为本地模块缺失导致的控制台错误；
- 关键标题的 computed font style 一致；
- 卡片、标签、按钮、区块的尺寸和位置接近原网页；
- 响应式断点行为和原网页一致；
- 如果内容或媒体被有意替换，需要明确说明差异。

---

## 📦 Repository structure / 仓库结构

```text
web-ui-copy/
├── README.md
└── SKILL.md
```

`SKILL.md` is the actual Agent Skill definition: the reusable workflow that tells an AI agent how to perform high-fidelity UI cloning.

`README.md` is human-facing documentation.

`SKILL.md` 是实际的 Agent Skill 定义文件：它定义了 AI Agent 如何执行高保真 UI 复制的可复用工作流。

`README.md` 是给人看的说明文档。

---

## 🛠️ Installation / 安装

Copy this repository into your agent skills directory, or adapt `SKILL.md` into your preferred AI-agent workflow system.

将本仓库复制到你的 agent skills 目录，或者把 `SKILL.md` 适配到你使用的 AI Agent 工作流系统中。

Required file:

```text
SKILL.md
```

---

## ⚠️ Notes / 注意事项

- Exact fidelity depends on access to the original page and its assets.
- Some pages use A/B tests, geolocation, login-only states, live counters, or time-sensitive content; these may need to be captured or frozen.
- Screenshot-only recreation cannot guarantee exact fonts or dynamic content unless assets are provided.
- For style-copy tasks with a different language/script, font support must be verified.

- 一比一还原依赖能否访问原网页及其资源。
- 有些网页存在 A/B 测试、地理位置差异、登录态、实时计数、时效性内容，需要额外冻结或捕获。
- 只有截图时，无法保证字体和动态内容完全准确，除非额外提供资源。
- 风格 copy 如果换成不同语言或文字系统，需要确认原字体是否支持。

---

<div align="center">

## Built for obsessive UI fidelity.
## 为极致 UI 还原而生。

</div>
