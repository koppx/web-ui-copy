<div align="center">

# ✨ web-ui-copy

### 高保真网页复制 Agent Skill

**一比一复制 · 风格迁移 · 字体还原 · 布局对齐 · 截图复刻**

<br />

[English README](README.md)

</div>

---

### 🚀 这是什么？

`web-ui-copy` 是一个用于 **高保真复制前端页面** 的 **Agent Skill**。它把 UI 复制变成可复用的 Agent 工作流：抓取源站、镜像资源、保留视觉系统，并像前端工程师一样验证还原结果。

它主要解决两类需求：

1. **一比一复制网页**：内容、字体、排版、颜色、图片、组件、响应式都尽量和原网页一致。
2. **风格 copy，内容替换**：保留原网页的字体、版式、颜色、组件风格，但换成你自己的内容。

### 🤖 以 Agent Skills 方式构建

`web-ui-copy` 将一套经过实战验证的 UI 复制方法封装成 **Agent Skills**：

- 明确区分一比一复制、风格 copy、截图复刻、差异修复；
- 源码镜像优先，追求像素级还原；
- 用 computed style 校验字体、间距、颜色和布局；
- 可作为 Agent 平台、Coding Assistant、自动化流水线里的复用能力。

### ⚡ 核心模式

| 模式 | 作用 |
| --- | --- |
| 🧬 **一比一复制** | 镜像原网页源码和资源，实现尽量一比一还原。 |
| 🎨 **风格 Copy** | 字体、间距、颜色、布局、组件保持一致，但内容可替换。 |
| 🖼️ **截图复刻** | 只有截图或设计稿时，根据图片复刻页面。 |
| 🔍 **差异修复** | 对比原网页和复制页，修复字体、颜色、间距、资源缺失等问题。 |

### 🧰 内置脚本

这不只是一个 Prompt。`web-ui-copy` 内置了一组实用脚本，让 UI 复制流程更稳定、可复用：

| 脚本 | 用途 |
| --- | --- |
| `scripts/mirror_webpage.py` | 抓取 HTML，并镜像 CSS / JS / 图片 / 字体 / 视频等视觉资源到本地。 |
| `scripts/style_snapshot.js` | 抽取指定 DOM 节点的 computed style 和位置尺寸。 |
| `scripts/compare_style_snapshots.py` | 对比原网页和复制页的字体、颜色、间距、布局差异。 |
| `scripts/extract_layout_blueprint.py` | 从截图中记录区块和元素区域，生成布局蓝图 JSON。 |

快速镜像：

```bash
python scripts/mirror_webpage.py --url https://example.com --out captures/example
python3 -m http.server 8080 -d captures/example/site
```

快速样式 QA：

```bash
python scripts/compare_style_snapshots.py \
  --source source-style.json \
  --copy copy-style.json \
  --out style-diff.json \
  --ignore-text
```

### 🧠 为什么需要它？

手写复刻页面通常“看起来差不多”，但细节很容易翻车：

- 标题默认样式没有 reset；
- 字体没有真正加载，悄悄 fallback；
- 颜色、渐变、阴影差一点；
- 框架 hydrate 后 DOM 变了；
- 响应式断点不一致；
- 卡片、标签、按钮、间距差几像素。

`web-ui-copy` 的核心策略是：**能镜像源码就先镜像源码，不轻易手写猜测。**

### 🧬 一比一复制流程

一比一复制时，它会优先走源码镜像流程：

1. 抓取服务端渲染后的 HTML。
2. 镜像 CSS、JS、图片、SVG、视频、字体、manifest、框架运行时资源。
3. 尽量保留原始路径和 hash 文件名。
4. 只移除不影响视觉的 analytics / beacon 脚本。
5. 本地打开页面，修复缺失资源和控制台错误。
6. 用 computed style 和元素位置验证关键节点。

### 🎨 风格 copy 流程

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

### 🪄 使用示例

#### 1. 一比一复制

```text
用 web-ui-copy 一比一复制 https://example.com。
内容、字体、颜色、图片、间距、布局都要保持一致。
```

#### 2. 风格复制但换内容

```text
用 web-ui-copy 复制 https://example.com 的网页风格，
但内容换成我的 AI SaaS 产品介绍。
字体、排版、卡片、按钮、间距都要保持一致。
```

#### 3. 修复复制页差异

```text
用 web-ui-copy 对比我的本地复制页和原网页。
修复字体不一致、标签颜色不一致、卡片背景不一致、间距不一致的问题。
```

### ✅ 质量检查清单

一个合格的复制页面应该满足：

- 没有缺失的视觉 CSS / JS / 图片 / 字体 / 视频资源；
- 没有因为本地模块缺失导致的控制台错误；
- 关键标题的 computed font style 一致；
- 卡片、标签、按钮、区块的尺寸和位置接近原网页；
- 响应式断点行为和原网页一致；
- 如果内容或媒体被有意替换，需要明确说明差异。

### 📦 仓库结构

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

`SKILL.md` 是实际的 Agent Skill 定义文件：它定义了 AI Agent 如何执行高保真 UI 复制的可复用工作流。

`README.md` 和 `README.zh-CN.md` 是给人看的中英文说明文档。

### 🛠️ 安装

将本仓库复制到你的 agent skills 目录，或者把 `SKILL.md` 适配到你使用的 AI Agent 工作流系统中。

必需文件：

```text
SKILL.md
```

### ⚠️ 注意事项

- 一比一还原依赖能否访问原网页及其资源。
- 有些网页存在 A/B 测试、地理位置差异、登录态、实时计数、时效性内容，需要额外冻结或捕获。
- 只有截图时，无法保证字体和动态内容完全准确，除非额外提供资源。
- 风格 copy 如果换成不同语言或文字系统，需要确认原字体是否支持。

---

<div align="center">

## 为极致 UI 还原而生。

[English README](README.md)

</div>
