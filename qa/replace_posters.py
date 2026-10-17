from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import re,shutil,base64,mimetypes,zipfile
root=Path('/home/user/chashin-site')
for i,name in enumerate(['roots','synthesis','future'],1):
 src=Path('/home/user/uploads')/f'{i}.jpg'
 shutil.copy2(src,root/'assets'/f'{name}-original.jpg')
 im=Image.open(src).convert('RGB')
 im.save(root/'assets'/f'{name}.webp',quality=94,method=6)
 im.thumbnail((600,800),Image.Resampling.LANCZOS)
 im.save(root/'assets'/f'{name}-600.webp',quality=91,method=6)
p=root/'index.html'; html=p.read_text()
html,n=re.subn(r'        <span class="image-top">.*?</span></span>\n','',html)
assert n==3,n
html=html.replace('href="assets/roots.webp" target="_blank"','href="assets/roots-original.jpg" target="_blank"')
html=html.replace('у портала','среди полигональной архитектуры')
p.write_text(html)
p=root/'style.css';css=p.read_text()
css=re.sub(r'\.artwork-image:after\{[^}]*\}','.artwork-image:after{content:none}',css)
css=css.replace('height:100%;width:100%;object-fit:cover;display:block;transition:transform .65s cubic-bezier(.2,.7,.3,1)','height:auto;width:100%;object-fit:contain;display:block')
css=css.replace('.artwork-image:hover img{transform:scale(1.045)}','.artwork-image:hover img{transform:none}')
css=css.replace('aspect-ratio:3/4','aspect-ratio:896/1200')
css+='\n/* Preserve the supplied posters: no crop, dark overlay, or added lettering. */\n.artwork-image{background:transparent;cursor:zoom-in}\n'
p.write_text(css)
p=root/'script.js';js=p.read_text()
for name in ['roots','synthesis','future']:
 js=js.replace(f"src: 'assets/{name}.webp',",f"src: 'assets/{name}.webp', original: 'assets/{name}-original.jpg',")
js=js.replace("document.querySelector('#original-link').href = artwork.src;","document.querySelector('#original-link').href = artwork.original;")
p.write_text(js)
canvas=Image.new('RGB',(1200,630),'#eae9e1');d=ImageDraw.Draw(canvas)
f=ImageFont.truetype(str(root/'assets/fonts/onest-bold.ttf'),124);small=ImageFont.truetype(str(root/'assets/fonts/onest-regular.ttf'),24)
d.text((45,40),'СЛЕД.',font=f,fill='#20211d');d.text((48,205),'ROMAN CHASHIN ART STYLE',font=small,fill='#20211d');d.text((48,545),'ПРОШЛОЕ → НАСТОЯЩЕЕ → БУДУЩЕЕ',font=small,fill='#20211d')
for i,n in enumerate(['roots','synthesis','future']):
 im=Image.open(root/'assets'/f'{n}.webp').resize((210,281),Image.Resampling.LANCZOS);canvas.paste(im,(505+i*225,173))
canvas.save(root/'assets/og-cover.jpg',quality=94)
p=root/'README.md';readme=p.read_text();readme=readme.replace('Тексты и визуальные материалы подготовлены для этой посадочной страницы по брифу.','Тексты подготовлены для этой посадочной страницы по брифу. Три постера предоставлены пользователем: 1.jpg — Roots, 2.jpg — The Synthesis, 3.jpg — The Future Vessel. В assets сохранены неизменённые JPG-оригиналы и оптимизированные WebP-копии. Изображения показаны целиком, без наложения дополнительного текста, затемнения или обрезки.')
p.write_text(readme)
def uri(rel):
 f=root/rel;return 'data:'+(mimetypes.guess_type(str(f))[0] or 'application/octet-stream')+';base64,'+base64.b64encode(f.read_bytes()).decode()
html=(root/'index.html').read_text()
html=re.sub(r'\s+srcset="[^"]*"','',html);html=re.sub(r'\s+sizes="[^"]*"','',html);html=re.sub(r'\s*<link rel="preload"[^>]+>','',html)
css=(root/'style.css').read_text()
for name in ['assets/fonts/onest-regular.ttf','assets/fonts/onest-bold.ttf']:css=css.replace(name,uri(name))
html=html.replace('<link rel="stylesheet" href="style.css">','<style>'+css+'</style>');html=html.replace('<script src="script.js" defer></script>','');html=html.replace('</body>','<script>'+(root/'script.js').read_text()+'</script>\n</body>')
for name in ['assets/roots.webp','assets/synthesis.webp','assets/future.webp','assets/roots-original.jpg','assets/synthesis-original.jpg','assets/future-original.jpg','assets/og-cover.jpg','assets/favicon.svg']:html=html.replace(name,uri(name))
Path('/home/user/Roman-Chashin.html').write_text(html)
with zipfile.ZipFile('/home/user/Roman-Chashin-site.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(root.rglob('*')):
  if f.is_file():z.write(f,Path('chashin-site')/f.relative_to(root))
print('Replaced all 3 posters; updated original links, cover, standalone and ZIP.')
print('Overlay elements remaining:',len(re.findall('class="image-(?:top|bottom)"',(root/'index.html').read_text())))
for i,name in enumerate(['roots','synthesis','future'],1):
 assert (root/'assets'/f'{name}-original.jpg').read_bytes()==(Path('/home/user/uploads')/f'{i}.jpg').read_bytes()
print('Original JPGs verified byte-for-byte.')
