# web-ui-copy

`web-ui-copy` is a Codex skill for copying frontend UI with high visual fidelity. It supports both exact webpage cloning and style-copy workflows where the source design system is preserved while the content is changed.

## What it does

- **Exact clone / content clone**: mirror a live page's HTML, CSS, JavaScript, images, fonts, videos, and framework assets so the local copy matches the original as closely as possible.
- **Style copy with new content**: keep the source site's typography, spacing, colors, components, layout, responsive behavior, and interaction style, but replace the visible text/content.
- **Screenshot/design recreation**: recreate a page from a screenshot or design image when source code is unavailable.
- **Clone debugging**: compare source and copy using computed styles, bounding boxes, loaded resources, console errors, fonts, and responsive breakpoints.

## When to use it

Use this skill when you ask Codex to:

- copy or clone a webpage exactly;
- preserve all content, fonts, colors, spacing, and layout;
- copy only the visual style but change the content;
- fix differences between an original webpage and a cloned page;
- recreate a frontend page from a design screenshot.

Example prompts:

```text
Use web-ui-copy to clone https://example.com exactly. Keep all content, fonts, colors, and layout identical.
```

```text
Use web-ui-copy to copy the style of https://example.com, but replace the content with my SaaS product copy. Fonts and layout must stay identical.
```

```text
Use web-ui-copy to compare my local clone with the original page and fix mismatched fonts, card colors, and spacing.
```

## Core approach

For exact clones, the skill prefers **source mirror mode** instead of hand-written recreation:

1. Capture the server-rendered HTML.
2. Mirror CSS, JS, images, videos, fonts, framework runtimes, and other visual assets.
3. Preserve original paths and hashed filenames where possible.
4. Remove only non-visual analytics/beacon scripts.
5. Validate local rendering by checking missing resources, console errors, computed styles, bounding boxes, and responsive breakpoints.

For style-copy tasks, the skill still mirrors source assets first, then replaces semantic content nodes while keeping the original classes, CSS variables, font files, resets, component structure, and responsive system.

## Installation

Copy this repository into your Codex skills directory, or install it using your preferred Codex skill installation flow.

The required skill file is:

```text
SKILL.md
```

## Repository structure

```text
web-ui-copy/
├── README.md
└── SKILL.md
```

## Notes

- Exact visual fidelity depends on access to the source page and its assets.
- Dynamic content, A/B tests, geolocation, login-only states, live counters, and time-sensitive data may need to be captured or frozen for reproducible clones.
- Screenshot-only recreation cannot guarantee exact fonts or dynamic content unless the source assets are provided.
