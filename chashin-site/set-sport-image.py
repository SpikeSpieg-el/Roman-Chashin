#!/usr/bin/env python3
"""Insert a user's sports image into the static HTML, without image dependencies."""
import argparse
import html
from pathlib import Path
import re
import shutil

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description='Replace a Street Code placeholder with your own image.')
parser.add_argument('sport', choices=['skate', 'bmx', 'scooter'])
parser.add_argument('image', type=Path, help='Path to your JPG, PNG, or WebP image')
args = parser.parse_args()
source = args.image.expanduser().resolve()
if not source.is_file() or source.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.webp']:
    parser.error('Select an existing JPG, PNG, or WebP file.')
name = 'street-' + args.sport + source.suffix.lower()
destination = root / 'assets' / name
if source != destination.resolve():
    shutil.copy2(source, destination)
page = root / 'index.html'
text = page.read_text(encoding='utf-8')
pattern = r'(<article class="street-card" data-sport="' + args.sport + r'">)(.*?)(</article>)'
match = re.search(pattern, text, re.S)
if not match:
    parser.error('Cannot find the expected Street Code card in index.html.')
labels = {'skate': 'скейтбординг', 'bmx': 'BMX', 'scooter': 'трюковые самокаты'}
block = match[2]
block = re.sub(r'(<img src=")[^"]+"', lambda m: m[1] + 'assets/' + name + '"', block, count=1)
block = re.sub(r'alt="[^"]*"', lambda _: 'alt="' + html.escape('Roman Chashin — Street Code: ' + labels[args.sport], quote=True) + '"', block, count=1)
block = re.sub(r'<figcaption class="slot-status">.*?</figcaption>', '', block, flags=re.S)
text = text[:match.start()] + match[1] + block + match[3] + text[match.end():]
page.write_text(text, encoding='utf-8')
print('Updated ' + args.sport + ': assets/' + name)
print('The image is shown in full (object-fit: contain), without extra lettering.')
print('Refresh the site. To regenerate the standalone HTML and ZIP, run: python3 package.py')
