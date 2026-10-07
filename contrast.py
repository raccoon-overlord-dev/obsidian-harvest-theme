#!/usr/bin/env python3
"""WCAG contrast check for the --ember-* tokens in src/theme.css.

Checks every text color against the background it's drawn on, in all four
palettes (Leaves and Hallows, dark and light). Hallows palettes inherit the
Leaves tokens they don't redeclare. Exits non-zero if any pair is below 4.5:1.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
MIN_RATIO = 4.5
PALETTES = {
    "leaves dark": [".theme-dark"],
    "leaves light": [".theme-light"],
    "hallows dark": [".theme-dark", "body.ember-decor-hallows.theme-dark"],
    "hallows light": [".theme-light", "body.ember-decor-hallows.theme-light"],
}
# background token: foreground tokens drawn on it
PAIRS = {
    "bg": ["text", "muted", "h1", "h2", "h3", "h4", "link", "comment"],
    "side": ["folder-text", "file-text", "text"],
    "active-bg": ["text", "folder-text"],
    "tag-bg": ["tag"],
    "inline-bg": ["inline"],
    "code-bg": ["code-text", "kw", "str", "fn", "num", "comment"],
    # callout titles: callout, h1, accent, str, num, h4, muted (see the --callout-* mapping)
    "callout-bg": ["text", "callout", "h1", "accent", "str", "num", "h4", "muted"],
    # buttons: text on the accent fill (dark ink in dark mode, light ink in light mode)
    "accent": ["ink"],
}


def rgb(value):
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", value.strip())
    if not m:
        raise ValueError(f"unsupported color: {value}")
    return [int(m[1][i:i + 2], 16) / 255 for i in (0, 2, 4)]


def luminance(c):
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(fg, bg):
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def rule_tokens(css, selector):
    tokens = {}
    for block in re.findall(r"(?m)^" + re.escape(selector) + r"\s*\{([^}]*)\}", css):
        tokens.update(re.findall(r"--ember-([\w-]+):\s*(#[0-9a-fA-F]{6})\s*;", block))
    if not tokens:
        sys.exit(f"error: no tokens for {selector} in src/theme.css")
    return tokens


def main():
    css = (ROOT / "src" / "theme.css").read_text(encoding="utf-8")
    failed = 0
    for name, selectors in PALETTES.items():
        t = {}
        for sel in selectors:
            t.update(rule_tokens(css, sel))
        # Ink on accent fills: the ember accents pick dark ink in dark mode and
        # light ink in light mode (--text-on-accent), and both inks are the bg.
        t["ink"] = t["bg"]
        print(name)
        for bg, fgs in PAIRS.items():
            for fg in fgs:
                r = ratio(rgb(t[fg]), rgb(t[bg]))
                ok = r >= MIN_RATIO
                failed += not ok
                print(f"  {fg:>12} on {bg:<11} {t[fg]} on {t[bg]}  {r:5.2f}:1  {'ok' if ok else 'FAIL'}")
    if failed:
        sys.exit(f"contrast check failed: {failed} pairs below {MIN_RATIO}:1")
    print("all pairs pass")


if __name__ == "__main__":
    assert round(ratio([0, 0, 0], [1, 1, 1]), 2) == 21.0  # sanity: black on white
    main()
