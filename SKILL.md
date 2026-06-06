---
name: web-ui-copy
description: Pixel- and content-faithful cloning of a live webpage or design screenshot into a local frontend. Use when copying exact webpage content, fonts, typography, spacing, colors, cards, chips, images, layout, responsive behavior, or when debugging clone mismatches; supports exact source-mirror mode, style-copy-with-new-content mode, and screenshot/design recreation mode.
---

# Web UI Copy

## Non-negotiable rule
If the user asks for `完全一致`, `一比一`, `exact`, `pixel perfect`, or complains that a clone differs from the original, use **source mirror mode first**. Do not hand-recreate DOM/CSS from screenshots unless source mirroring is impossible or the user explicitly asks for style-only copying.

Handwritten reconstruction is only a fallback. It commonly drifts in heading resets, framework-scoped CSS, hydration output, responsive grids, chip gradients, text wrapping, and generated content.

## Mode selection
- **Exact clone / content clone**: mirror original HTML, CSS, JS, images, fonts, and framework runtime assets. Preserve visible text and DOM shape; only rewrite URLs needed for local serving.
- **Style copy / new content clone**: copy the source visual language exactly, especially fonts, typography, colors, spacing, component structure, responsive behavior, and interaction style, but replace visible text/content with user-provided or generated content. Use when the user says `风格copy`, `风格复制`, `字体一致但内容不一样`, `same style different content`, `use this style for my content`, or similar.
- **Style-only clone**: recreate layout/components after extracting computed styles. Use this only when the user wants a new implementation or the original source/assets cannot be mirrored.
- **Screenshot-only design clone**: infer layout from image, then validate against screenshot. Warn that dynamic text/content cannot be guaranteed without source.

## Style copy / new content workflow
Use this when the user wants the copied page to look like the source, with **identical font rendering and component styling**, but with different text/content.

1. **Mirror first, then edit content**
   - Still start from source mirror mode whenever the live source is available.
   - Keep the original CSS, font files, CSS variables, resets, layout classes, component classes, breakpoints, and visual JS.
   - Do not hand-rewrite typography unless source assets are unavailable.
   - Replace only semantic content nodes: headings, paragraphs, labels, card text, list items, CTA text, alt text, metadata, and data arrays.
   - Preserve DOM nesting and class names where possible so original CSS continues to apply.

2. **Font fidelity is mandatory**
   - Download or preserve the same `@font-face` declarations and font files used by the source.
   - Keep the same `font-family` fallback chain, `font-size`, `font-weight`, `line-height`, `letter-spacing`, text transform, smoothing, and language-specific font choices.
   - If the new content uses a different language/script, verify the source font supports it. If not, choose the closest compatible font and document the substitution.
   - Never rely on browser defaults for headings; copy source resets such as `h1,h2,h3 { font-size: inherit; font-weight: inherit; }` when present.

3. **Content replacement rules**
   - Keep text length close to the original when the layout depends on wrapping. If the new content is longer/shorter, adjust only within the source system: existing responsive widths, max-widths, line-height, and spacing tokens.
   - For cards, chips, badges, tabs, stats, and nav items, keep the original element type and CSS class names.
   - For images/icons, either mirror the original visual treatment or replace assets with same aspect ratio, object-fit, radius, shadow, and crop behavior.
   - For generated content stored in JSON scripts, framework props, Astro/Vue/React islands, or inline state, update the data source rather than patching hydrated DOM output.

4. **Validate with computed styles**
   - Compare representative source-vs-copy nodes at the same viewport:
     - main heading
     - paragraph/body text
     - CTA/button
     - card title/body
     - badge/chip/stat block
     - nav/footer text
   - `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`, `color`, `background`, `padding`, `margin`, `borderRadius`, `display`, `gap`, and bounding boxes should match the source style system.
   - Expected differences should be limited to text content and any intentionally replaced media.

5. **When not to use this mode**
   - If the user says `完全一致`, `一比一`, `内容也一样`, or points out missing content, use exact clone mode instead.
   - If only a screenshot/design is provided and no live source exists, use screenshot-only design clone and explicitly state that font/content fidelity depends on inferred or provided assets.

## Exact source mirror workflow
1. **Capture immutable source artifacts**
   - Save the server-rendered HTML to `source-capture/source.html`.
   - Save all same-origin CSS, JS modules, images, SVGs, videos, fonts, and manifest assets referenced by `src`, `href`, CSS `url(...)`, JS static imports, preloads, and framework islands.
   - Keep original filenames and hashed asset names when possible (`/_astro/foo.hash.js`, `/assets/foo.hash.css`, etc.).

2. **Build local mirror tree**
   - Copy the captured HTML to the local entry point (usually `index.html`).
   - Recreate source paths locally: `/_astro/...`, `/img/...`, `/fonts/...`, `/assets/...`.
   - Rewrite only what is necessary:
     - remove analytics/beacon scripts that do not affect visuals;
     - stub non-visual platform scripts such as Cloudflare email decode if needed;
     - keep visual/app scripts intact.
   - Do not replace source CSS with handcrafted CSS for exact mode.

3. **Resolve dependency closure**
   - For every mirrored JS file, scan static imports like `from "./..."` and `import("./...")`; download/copy those dependencies too.
   - For every mirrored CSS file, scan `url(...)`; download/copy fonts and background images.
   - Load the local page and check console/network errors; missing module or missing stylesheet errors must be fixed before visual tweaking.

4. **Preserve framework hydration**
   - Astro/Vue/React/Svelte islands often contain SSR HTML plus client modules. Keep island attributes (`component-url`, `renderer-url`, `props`, `ssr`, `client`, scoped attributes) unchanged unless a local path rewrite is required.
   - Hydration should complete without errors. If hydration changes DOM, treat the hydrated DOM as the visual truth only if the original also hydrates the same way.

5. **Validate source parity**
   - Same viewport width, height, DPR, zoom, locale, color scheme, and scroll offsets.
   - Check:
     - no console errors from missing local modules/assets;
     - key selectors have matching computed styles and bounding boxes;
     - article/card/chip grids use source classes and source CSS;
     - images/fonts are loaded from local mirror or intentionally remote.

## Computed-style fallback workflow
Use only for style-only clone, missing source, or small patches after exact mirror.

1. **Map important nodes**
   - Page shell, hero, headings, paragraphs, buttons, ranking rows, cards, chips, article lists/grids, tables, footer.
   - For scoped/framework CSS, map semantic source nodes to clone nodes.

2. **Extract computed style truth**
   At the same viewport/zoom/scroll, collect at least:
   `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`, `color`, `background-color`, `background-image`, `border`, `border-radius`, `box-shadow`, `padding`, `margin`, `display`, `gap`, `width`, `height`, `grid-template-columns`, `justify-content`, `align-items`, `text-align`, plus `getBoundingClientRect()`.

   ```js
   const props = [
     'fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','color',
     'backgroundColor','backgroundImage','borderTopColor','borderTopWidth',
     'borderTopStyle','borderRadius','boxShadow','padding','margin','display',
     'gap','width','height','gridTemplateColumns','justifyContent','alignItems','textAlign'
   ];
   function styleOf(selector) {
     const el = document.querySelector(selector);
     if (!el) return null;
     const s = getComputedStyle(el);
     const r = el.getBoundingClientRect();
     return {
       selector,
       text: el.textContent?.trim().slice(0, 120),
       rect: { x: r.x, y: r.y, w: r.width, h: r.height },
       style: Object.fromEntries(props.map(p => [p, s[p]]))
     };
   }
   ```

3. **Patch by evidence**
   - Copy exact source CSS rules where possible; do not guess.
   - Include reset effects. Example: Tailwind sets `h1,h2,h3,h4,h5,h6 { font-size: inherit; font-weight: inherit; }`; missing it makes headings too bold.
   - For chips/badges, preserve `background-image` gradients, border colors, text colors, opacity, radius, padding, and special-state classes.
   - Patch shared components after fixing a pointed-out mismatch.

## Quality gates
- Exact mode: local DOM/resource tree is a mirror of the captured original except documented local path rewrites and removed non-visual analytics.
- No missing CSS, JS modules, images, fonts, or visible text in the copied scope.
- Hydration has no console errors.
- Headings, chips, cards, and article sections match original computed styles and bounding boxes at target viewport.
- Responsive behavior is checked at relevant desktop/mobile breakpoints.

## Known pitfalls
- Screenshots alone hide CSS reset and hydration differences; compare computed styles and resource loading.
- A page can look close while using the wrong responsive branch; always match viewport width and zoom.
- Lazy images may not load until scrolled into view; verify after scrolling.
- External analytics, ads, A/B tests, geolocation, live counts, and time-sensitive data can change; freeze captured values for reproducible clones.
