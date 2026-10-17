#!/usr/bin/env python3
"""Add production URL metadata and generate a sitemap for a static deployment."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urljoin
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description='Configure the public HTTPS URL of the Roman Chashin landing page.')
parser.add_argument('--url', required=True, help='Full production URL, including a subdirectory if used')
args = parser.parse_args()
parts = urlsplit(args.url)
if (parts.scheme != 'https' or not parts.hostname or '.' not in parts.hostname
        or parts.query or parts.fragment or parts.username or parts.password):
    parser.error('Use a real public HTTPS URL without query parameters, credentials or a fragment.')
url = args.url.rstrip('/') + '/'
page = ROOT / 'index.html'
html = page.read_text(encoding='utf-8')
block = '<!-- PUBLICATION_META -->\n  <link rel="canonical" href="' + escape(url, {'"': '&quot;'}) + '">\n  <meta property="og:url" content="' + escape(url, {'"': '&quot;'}) + '">\n  <!-- /PUBLICATION_META -->'
html = re.sub(r'<!-- PUBLICATION_META -->(?:.*?<!-- /PUBLICATION_META -->)?', lambda _: block, html, count=1, flags=re.S)
for name in ['og:image', 'twitter:image']:
    key = 'property' if name.startswith('og:') else 'name'
    html = re.sub(r'(<meta ' + key + r'="' + name + r'" content=")[^"]*(">)', lambda m: m[1] + urljoin(url, 'assets/og-cover.jpg') + m[2], html)
schema_re = r'(<script type="application/ld\+json" id="structured-data">)(.*?)(</script>)'
match = re.search(schema_re, html, re.S)
data = json.loads(match[2])
def resolve(value):
    if isinstance(value, dict):
        for key, item in list(value.items()):
            if key == '@id' and isinstance(item, str) and '#' in item:
                value[key] = url + '#' + item.rsplit('#', 1)[-1]
            elif key == 'image' and isinstance(item, str):
                value[key] = urljoin(url, 'assets/' + item.split('assets/', 1)[-1]) if 'assets/' in item else item
            else:
                resolve(item)
    elif isinstance(value, list):
        for item in value:
            resolve(item)
resolve(data)
for item in data['@graph']:
    if item['@type'] in ['WebSite', 'CollectionPage']:
        item['url'] = url
html = re.sub(schema_re, lambda m: m[1] + '\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n  ' + m[3], html, count=1, flags=re.S)
page.write_text(html, encoding='utf-8')
images = [('assets/roots.webp', 'След I. Исток и Ремесло'), ('assets/synthesis.webp', 'След II. Момент передачи и Синтез'), ('assets/future.webp', 'След III. Капсула в будущее')]
for key, title in [('skate', 'Street Code — Скейтбординг'), ('bmx', 'Street Code — BMX'), ('scooter', 'Street Code — Трюковые самокаты')]:
    card = re.search(r'<article class="street-card" data-sport="' + key + r'">(.*?)</article>', html, re.S)
    image = re.search(r'<img src="([^"]+)"', card[1]) if card else None
    if image and not image[1].endswith('.svg'):
        images.append((image[1], title))
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n  <url>\n    <loc>' + escape(url) + '</loc>\n'
for name, title in images:
    sitemap += '    <image:image><image:loc>' + escape(urljoin(url, name)) + '</image:loc><image:title>' + escape(title) + '</image:title></image:image>\n'
sitemap += '  </url>\n</urlset>\n'
(ROOT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + urljoin(url, 'sitemap.xml') + '\n', encoding='utf-8')
print('Configured: ' + url)
print('Updated index.html, robots.txt and sitemap.xml. Upload the static files to your host.')
if parts.path and parts.path != '/':
    print('Subdirectory deployment: also add the Sitemap directive to robots.txt at the domain root.')
