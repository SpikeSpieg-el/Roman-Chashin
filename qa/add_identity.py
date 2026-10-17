from pathlib import Path
import json,re
root=Path('/home/user/chashin-site')
paths=json.loads(Path('/home/user/qa/brand-paths.json').read_text())
section=Path('/home/user/qa/identity-section.html').read_text().replace('{{ARM}}',paths['arm']).replace('{{SPINE}}',paths['spine'])
section=section.replace('class="identity-controls" role=', 'class="identity-controls" hidden role=')
section=section.replace('id="identity-mode-caption"','id="identity-mode-caption" aria-live="polite"')
Path('/home/user/qa/identity-section-rendered.html').write_text(section)
p=root/'index.html';s=p.read_text()
s=s.replace('<span class="brand-symbol" aria-hidden="true">↗</span>', '<img class="brand-monogram" src="assets/brand/mark-micro.svg" width="38" height="41" alt="">')
s=s.replace('<span class="brand-dot">✳</span>','')
s=s.replace('<a href="#style"><small>03</small> Стиль</a>','<a href="#identity"><small>03</small> Знак</a>')
s=s.replace('<span class="title-cross">↗</span>','<a class="hero-logo-link" href="#identity" aria-label="Разбор логотипа CHASHIN"><img src="assets/brand/mark-orange.svg" width="66" height="72" alt=""></a>')
s=s.replace('ОБСУДИТЬ ПРОЕКТ ↗</a></div>','РАЗБОР ЛОГОТИПА ↓</a></div>',1)
s=s.replace('<a href="#contact">РАЗБОР ЛОГОТИПА','<a href="#identity">РАЗБОР ЛОГОТИПА')
s=s.replace('  <section class="statement', section+'  <section class="statement',1)
s=s.replace('04 / АВТОР','05 / АВТОР').replace('05 / ДЕТАЛИ','06 / ДЕТАЛИ').replace('06 / НА СВЯЗИ','07 / НА СВЯЗИ')
s=s.replace('<div class="footer-word" aria-hidden="true">CHASHIN<span>✳</span></div>','<div class="footer-word" aria-hidden="true">CHASHIN<img class="footer-monogram" src="assets/brand/mark-bone.svg" width="32" height="35" alt=""></div>')
s=s.replace('Постер, визуальная серия, айдентика<br>или коллаборация','Логотип, визуальная серия, айдентика<br>или коллаборация')
s=s.replace('Авторские постеры «След», новая серия про скейтбординг, BMX и трюковые самокаты. Контакты дизайнера.','Авторские постеры, серия Street Code и разбор логотипа CHASHIN. Контакты дизайнера.')
pattern=r'(<script type="application/ld\+json" id="structured-data">)(.*?)(</script>)'
m=re.search(pattern,s,re.S);data=json.loads(m[2])
for node in data['@graph']:
 if node['@type']=='CollectionPage':
  node['hasPart']=[{'@id':'#identity'}]
 if node['@type']=='Person':
  node['image']='assets/brand/logo-lockup.svg'
  # The logo identifies the brand, not a claimed portrait of the person.
  del node['image']
data['@graph'].append({'@type':'CreativeWork','@id':'#identity','name':'CHASHIN — Стык: концепция монограммы и разбор логотипа','description':'Собственная айдентика: монограмма Ч из двух векторных контуров. Идея, модульная геометрия, негативное пространство, микроверсия и применение.','image':'assets/brand/mark-ink.svg','inLanguage':'ru','about':{'@id':'#roman-chashin'}})
s=re.sub(pattern,lambda m:m[1]+'\n'+json.dumps(data,ensure_ascii=False,indent=2)+'\n  '+m[3],s,flags=re.S)
p.write_text(s)
print('Inserted identity case, replaced arrow logo, updated favicon references and SEO.')
