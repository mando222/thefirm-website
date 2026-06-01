#!/usr/bin/env python3
"""
build.py — inlines shared header/footer into every practice-area page.

Usage:
  python3 build.py

Edit assets/header.html or assets/footer.html, then re-run this script.
All pages in practice-areas/ will be updated automatically.
"""
import os, glob, re

ROOT  = os.path.dirname(os.path.abspath(__file__))
PAGES = glob.glob(os.path.join(ROOT, 'practice-areas', '*.html'))

with open(os.path.join(ROOT, 'assets', 'header.html')) as f:
    HEADER = f.read().strip()

with open(os.path.join(ROOT, 'assets', 'footer.html')) as f:
    FOOTER = f.read().strip()

HEADER_BLOCK = f'<!-- @@header-start@@ -->\n  {HEADER}\n  <!-- @@header-end@@ -->'
FOOTER_BLOCK = f'<!-- @@footer-start@@ -->\n  {FOOTER}\n  <!-- @@footer-end@@ -->'

def inject(html, tag, block):
    # Replace anything between the markers (inclusive) with fresh content
    pattern = rf'<!-- @@{tag}-start@@ -->.*?<!-- @@{tag}-end@@ -->'
    replaced, n = re.subn(pattern, block, html, flags=re.DOTALL)
    if n:
        return replaced, True
    # No markers yet — replace the placeholder div
    placeholder = f'<div id="site-{tag}"></div>'
    replaced = html.replace(placeholder, block)
    return replaced, placeholder in html

updated = 0
for path in sorted(PAGES):
    with open(path) as f:
        src = f.read()

    out, h_ok = inject(src,  'header', HEADER_BLOCK)
    out, f_ok = inject(out,  'footer', FOOTER_BLOCK)

    # Remove the now-redundant includes.js script tag if present
    out = re.sub(r'\s*<script src="\.\./assets/includes\.js"></script>', '', out)

    with open(path, 'w') as f:
        f.write(out)

    name = os.path.basename(path)
    print(f'  {name}  (header: {h_ok}, footer: {f_ok})')
    updated += 1

print(f'\nDone — {updated} pages updated.')
