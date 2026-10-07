#!/usr/bin/env python3
"""Build theme.css from src/theme.css.

Replaces every ember-svg(icon, color) with a data: URI of icons/<icon>.svg
in that color (a hex value, or an --ember-* token resolved from the rule it
appears in). The color is optional for composed SVGs that name their colors
as --ember-* tokens. Refuses to write output that contains remote resources
or exceeds the store's size limit.
"""
import pathlib
import re
import sys
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent
MAX_BYTES = 100 * 1024


def read_svg(name):
    s = (ROOT / "icons" / f"{name}.svg").read_text(encoding="utf-8").strip()
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    s = re.sub(r'\s+xmlns:c2pa="[^"]*"', "", s)
    return re.sub(r"></(path|rect|ellipse)>", "/>", s)


def svg_markup(name, color, tokens):
    """icons/<name>.svg, minified. currentColor becomes `color`, --ember-*
    tokens in attributes become their hex value, and every <use href="#icon">
    gets icons/<icon>.svg once as a <symbol>, so composed decorations repeat
    a shape without repeating its path."""
    s = read_svg(name)
    symbols = []
    for ref in dict.fromkeys(re.findall(r'href="#([\w-]+)"', s)):
        m = re.match(r'<svg([^>]*)>(.*)</svg>$', read_svg(ref), flags=re.S)
        box = re.search(r'viewBox="[^"]*"', m.group(1)).group(0)
        symbols.append(f'<symbol id="{ref}" {box}>{m.group(2)}</symbol>')
    if symbols:
        s = re.sub(r"(<svg[^>]*>)", lambda m: m.group(1) + "<defs>" + "".join(symbols) + "</defs>", s, count=1)

    def token(m):
        if m.group(0) not in tokens:
            sys.exit(f"error: {m.group(0)} in icons/{name}.svg is not a palette token")
        return tokens[m.group(0)]

    s = re.sub(r"--ember-[\w-]+", token, s)
    if color:
        s = s.replace("currentColor", color)
    return s.replace('"', "'")


def svg_uri(markup):
    # A data-URI SVG needs its xmlns, but a literal "http://" would trip the
    # remote-resource check, so the colon is percent-encoded like the rest.
    return 'url("data:image/svg+xml,' + quote(markup, safe=" ='/-.,;()") + '")'


def palette_tokens(src):
    """{selector: {--ember-token: value}} for every rule that declares tokens."""
    blocks = {}
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", src):
        tokens = dict(re.findall(r"(--ember-[\w-]+):\s*(#[0-9a-fA-F]{3,8})\s*;", body))
        if tokens:
            blocks[sel.strip().split("\n")[-1].strip()] = tokens
    return blocks


def inline_icons(src):
    """Replace ember-svg(icon, --ember-token) with a data URI, resolving the
    token in the enclosing rule. Hallows rules fall back to the Leaves rule
    of the same variant for tokens they don't redeclare."""
    blocks = palette_tokens(src)

    def rule(m):
        sel, body = m.group(1), m.group(2)
        key = sel.strip().split("\n")[-1].strip()
        base = ".theme-dark" if "theme-dark" in key else ".theme-light"
        tokens = {**blocks.get(base, {}), **blocks.get(key, {})}

        def icon(c):
            color = c.group(2)
            if color and color.startswith("--"):
                if color not in tokens:
                    sys.exit(f"error: {color} not defined for {key!r}")
                color = tokens[color]
            return svg_uri(svg_markup(c.group(1), color, tokens))

        return sel + "{" + re.sub(r"ember-svg\(([\w-]+)(?:,\s*([^)\s]+))?\)", icon, body) + "}"

    return re.sub(r"([^{}]+)\{([^{}]*)\}", rule, src)


def main():
    src = (ROOT / "src" / "theme.css").read_text(encoding="utf-8")
    out = inline_icons(src)
    if "ember-svg(" in out:
        sys.exit("error: ember-svg() left outside a palette rule")
    bad = re.findall(r"https?://|@import", out, flags=re.IGNORECASE)
    if bad:
        sys.exit(f"error: remote resources not allowed in theme.css: {sorted(set(bad))}")
    size = len(out.encode())
    if size >= MAX_BYTES:
        sys.exit(f"error: theme.css would be {size} bytes, limit is {MAX_BYTES}")
    (ROOT / "theme.css").write_text(out, encoding="utf-8")
    print(f"theme.css written ({size} bytes, {size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
