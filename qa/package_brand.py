from pathlib import Path
import re,base64,mimetypes,zipfile,shutil
root=Path('/home/user/chashin-site')
html=(root/'index.html').read_text()
section=re.search(r'  <section id="identity".*?(?=  <section class="statement)',html,re.S)[0]
section=section.replace('04 / СОБСТВЕННАЯ АЙДЕНТИКА','КЕЙС / СОБСТВЕННАЯ АЙДЕНТИКА')
css=(root/'style.css').read_text()
logic=(root/'script.js').read_text().split('// An actual vector breakdown:',1)[1]
logic='// An actual vector breakdown:'+logic
preview='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CHASHIN — Low-poly геометрия / Разбор логотипа</title><style>'''+css+'''</style></head><body><header class="identity-guide-header"><img src="assets/brand/logo-lockup.svg" width="813" height="216" alt="CHASHIN — логотип"><a href="Roman-Chashin.html#identity">На сайт ↗</a></header><main>'''+section+'''</main><footer class="identity-guide-footer"><span>CHASHIN / ЧИСТЫЙ ВЕКТОР / 30 ПОЛИГОНОВ</span><a href="CHASHIN-brand-kit.zip" download>Скачать набор SVG + PDF ↓</a><a href="Roman-Chashin.html#identity">Открыть обновлённый сайт ↗</a></footer><script>if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.body.classList.add('motion-on');\n'''+logic+'''</script></body></html>'''
references=set(re.findall(r'''assets/[a-zA-Z0-9_./-]+\.(?:webp|jpg|jpeg|png|svg|ico|ttf|woff2)''',preview))
for rel in sorted(references,key=len,reverse=True):
 f=root/rel;mime=mimetypes.guess_type(str(f))[0] or 'application/octet-stream'
 preview=preview.replace(rel,'data:'+mime+';base64,'+base64.b64encode(f.read_bytes()).decode())
Path('/home/user/CHASHIN-logo-case.html').write_text(preview)
shutil.copy(root/'assets/brand/mark-iso.svg','/home/user/CHASHIN-logo.svg')
with zipfile.ZipFile('/home/user/CHASHIN-brand-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in Path('/home/user/chashin-brand').iterdir():
  if f.is_file():z.write(f,Path('CHASHIN-brand-kit')/f.name)
print('Packaged logo, brand kit and self-contained case study.')
