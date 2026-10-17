#!/usr/bin/env python3
"""Build a standalone offline HTML and ZIP from the current static site."""
from pathlib import Path
import base64
import mimetypes
import re
import zipfile

root = Path(__file__).resolve().parent
output = root.parent
html = (root / 'index.html').read_text(encoding='utf-8')
html = re.sub(r'\s+srcset="[^"]*"', '', html)
html = re.sub(r'\s+sizes="[^"]*"', '', html)
html = re.sub(r'\s*<link rel="preload"[^>]+>', '', html)
html = html.replace('<link rel="stylesheet" href="style.css">', '<style>' + (root / 'style.css').read_text(encoding='utf-8') + '</style>')
html = html.replace('<script src="script.js" defer></script>', '')
html = html.replace('</body>', '<script>' + (root / 'script.js').read_text(encoding='utf-8') + '</script>\n</body>')
# Embed only referenced assets. All original files stay in the deployable archive.
references = set(re.findall(r'''assets/[a-zA-Z0-9_./-]+\.(?:webp|jpg|jpeg|png|svg|ico|ttf|woff2)''', html))
for rel in sorted(references, key=len, reverse=True):
    file = root / rel
    if not file.is_file():
        raise FileNotFoundError(file)
    mime = mimetypes.guess_type(str(file))[0] or 'application/octet-stream'
    uri = 'data:' + mime + ';base64,' + base64.b64encode(file.read_bytes()).decode()
    html = html.replace(rel, uri)
(output / 'Roman-Chashin.html').write_text(html, encoding='utf-8')
with zipfile.ZipFile(output / 'Roman-Chashin-site.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for file in sorted(root.rglob('*')):
        if file.is_file() and '__pycache__' not in file.parts:
            archive.write(file, Path('chashin-site') / file.relative_to(root))
print('Saved: ' + str(output / 'Roman-Chashin.html'))
print('Saved: ' + str(output / 'Roman-Chashin-site.zip'))
