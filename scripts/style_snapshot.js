/*
Capture computed-style snapshots for high-fidelity UI clone validation.

Usage in a browser/Playwright page context:
  const selectors = ['h1', '.hero', '.card', '.button'];
  const snapshot = window.webUiCopyStyleSnapshot(selectors);

The script can also be pasted into DevTools before calling the function.
*/
(function installWebUiCopyStyleSnapshot(global) {
  const DEFAULT_PROPS = [
    'fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'lineHeight', 'letterSpacing',
    'textTransform', 'textAlign', 'color', 'backgroundColor', 'backgroundImage',
    'borderTopColor', 'borderTopWidth', 'borderTopStyle', 'borderRadius', 'boxShadow',
    'opacity', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
    'marginTop', 'marginRight', 'marginBottom', 'marginLeft', 'display', 'position',
    'gap', 'rowGap', 'columnGap', 'width', 'height', 'maxWidth', 'minHeight',
    'gridTemplateColumns', 'justifyContent', 'alignItems', 'objectFit', 'objectPosition'
  ];

  function snapshotOne(selector, index, props) {
    const nodes = Array.from(document.querySelectorAll(selector));
    const el = nodes[index || 0];
    if (!el) {
      return { selector, index: index || 0, found: false, count: nodes.length };
    }
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return {
      selector,
      index: index || 0,
      found: true,
      count: nodes.length,
      tagName: el.tagName.toLowerCase(),
      className: typeof el.className === 'string' ? el.className : '',
      text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 180),
      rect: {
        x: Number(rect.x.toFixed(3)),
        y: Number(rect.y.toFixed(3)),
        w: Number(rect.width.toFixed(3)),
        h: Number(rect.height.toFixed(3))
      },
      style: Object.fromEntries(props.map((prop) => [prop, style[prop]]))
    };
  }

  global.webUiCopyStyleSnapshot = function webUiCopyStyleSnapshot(targets, options) {
    const opts = options || {};
    const props = opts.props || DEFAULT_PROPS;
    const normalizedTargets = (targets || []).map((target) => {
      if (typeof target === 'string') return { selector: target, index: 0 };
      return { selector: target.selector, index: target.index || 0 };
    });
    return {
      url: location.href,
      title: document.title,
      capturedAt: new Date().toISOString(),
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight,
        dpr: window.devicePixelRatio,
        scrollX: window.scrollX,
        scrollY: window.scrollY
      },
      targets: normalizedTargets.map((target) => snapshotOne(target.selector, target.index, props))
    };
  };
})(window);
