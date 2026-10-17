from pathlib import Path
import re,json
root=Path('/home/user/chashin-site')
p=root/'index.html';s=p.read_text()
s=s.replace('<title>Roman Chashin art style — «След»: low-poly искусство и культурный код</title>','<title>Roman Chashin art style — ремесло, стрит и PS1 low-poly</title>')
s=re.sub(r'<meta name="description" content="[^"]+">','<meta name="description" content="Roman Chashin art style: ремесло × стрит × PS1 low-poly. Авторские постеры «След», новая серия про скейтбординг, BMX и трюковые самокаты. Контакты дизайнера.">',s)
s=s.replace('СЛЕД. — Roman Chashin art style','Roman Chashin — ремесло × стрит × PS1')
s=s.replace('Форма меняется. Код остаётся. Три главы о ремесле, памяти и цифровом будущем.','Память рук. Свобода улицы. Геометрия PS1. Авторский визуальный язык Roman Chashin.')
s=s.replace('Прошлое. Настоящее. Будущее. Культурный код в эстетике low-poly.','Ремесло, уличная культура и эстетика PlayStation 1. Постеры, визуальные серии и коллаборации.')
s=s.replace('<body>','<body>\n<div class="scroll-progress" aria-hidden="true"></div>')
s=re.sub(r'<nav aria-label="Главная навигация">.*?</nav>','<nav aria-label="Главная навигация"><a href="#works"><small>01</small> След</a><a href="#street"><small>02</small> Стрит</a><a href="#style"><small>03</small> Стиль</a><a href="#contact"><small>04</small> Контакты</a></nav>',s)
s=s.replace('<a class="header-contact" href="https://www.behance.net/Roman_chashin/projects" target="_blank" rel="noopener noreferrer">Behance','<a class="header-contact" href="https://t.me/Spike_Spige_L" target="_blank" rel="noopener noreferrer" aria-label="Написать Roman Chashin в Telegram">Написать')
hero='''  <section class="hero style-hero" aria-labelledby="hero-title">
    <div class="eyebrow hero-top"><span><i class="live-dot" aria-hidden="true"></i> НЕЗАВИСИМЫЙ ВИЗУАЛЬНЫЙ ЯЗЫК</span><span>ROMAN CHASHIN / DESIGN & ART DIRECTION</span></div>
    <div class="hero-heading">
      <div class="hero-title-wrap"><span class="hero-kicker">HANDCRAFTED MEMORY. STREET ENERGY.</span><h1 id="hero-title"><span class="title-line">РЕМЕСЛО.</span><span class="title-line">СТРИТ.</span><span class="title-line title-accent">PS1<span class="title-cross">↗</span></span></h1></div>
      <div class="hero-intro"><div class="cube-scene" aria-hidden="true"><div class="wire-cube"><span class="cube-face front">LOW<br>POLY</span><span class="cube-face back"></span><span class="cube-face left"></span><span class="cube-face right">CHASHIN</span><span class="cube-face top"></span><span class="cube-face bottom"></span></div><span class="cube-caption">OBJECT_001 / MEMORY MESH</span></div><h2>Память рук.<br>Свобода улицы.<br>Честная геометрия.</h2><p>Я соединяю эстетику ремесла,<br>стрит-культуру и low-poly эпохи<br>PlayStation 1. Это мой язык.</p><a class="text-link" href="#works">Войти в мой мир <span aria-hidden="true">↓</span></a></div>
    </div>
    <div class="hero-foot eyebrow"><span>ROMAN CHASHIN ART STYLE</span><span>CLAY × CONCRETE × POLYGONS</span><a href="#contact">ОБСУДИТЬ ПРОЕКТ ↗</a></div>
  </section>
  <div class="series-intro section-pad"><div><span class="eyebrow">01 / СЕРИЯ «СЛЕД» — PASS IT ON</span><h2>Память в новой форме.</h2></div><p>Прошлое. Настоящее. Будущее.<br>Три поколения — один культурный код.</p></div>
'''
s=re.sub(r'  <section class="hero".*?(?=  <section id="works")',lambda _:hero,s,flags=re.S)
item='<span>РЕМЕСЛО</span><b>×</b><span>СТРИТ</span><b>×</b><span>PS1 LOW-POLY</span><b>↗</b><span>ROMAN CHASHIN ART STYLE</span><b>✳</b>'
s=re.sub(r'  <div class="ticker".*?</div>',lambda _:f'  <div class="ticker" aria-hidden="true"><div class="ticker-track"><div class="ticker-group">{item}</div><div class="ticker-group">{item}</div></div></div>',s,count=1)
s=s.replace('01 / ИДЕЯ ПРОЕКТА','В ОСНОВЕ / ПАМЯТЬ МАТЕРИАЛА')
s=s.replace('  <section id="style"',Path('/home/user/qa/street-section.html').read_text()+'  <section id="style"',1)
s=s.replace('02 / ВИЗУАЛЬНЫЙ КОД','03 / ВИЗУАЛЬНЫЙ КОД')
s=s.replace('<h2>Тёплая память.<br>Цифровая форма.</h2><p>Не фильтр. Не эффект.<br>Система визуальных решений.</p>','<h2>Руки. Улица.<br>Полигоны.</h2><p>Три источника.<br>Один авторский почерк.</p>')
s=s.replace('<h3>Честный полигон</h3><p>Выраженные грани, Gouraud shading и эстетика PS1. Геометрия становится самостоятельным художественным языком.</p>','<h3>Эпоха PS1</h3><p>Видимые грани, Gouraud shading, дизеринг и низкое разрешение текстур. Не ретро-фильтр, а честный язык раннего 3D.</p>')
s=s.replace('<h3>Контраст материй</h3><p>Терракота, лён и дерево встречаются с неоновым цианом и янтарным светом. Прошлое и будущее в одной палитре.</p>','<h3>Память ремесла</h3><p>Глина, лён, дерево, тканый орнамент. Материалы хранят след рук — я переношу эту тактильность в цифровую форму.</p>')
s=s.replace('<h3>Живой артефакт</h3><p>Тканый орнамент, фактура глины, пиксельный дизеринг. Несовершенство поверхности как доказательство памяти.</p>','<h3>Энергия стрита</h3><p>Бетон, потёртая дека, металл, теги. Город не декорация, а мастерская. Трюк и рисунок — два способа оставить свой след.</p>')
s=s.replace('>DIGITAL CRAFT</span>','>STREET CULTURE</span>')
s=s.replace('03 / АВТОР','04 / АВТОР').replace('04 / ДЕТАЛИ','05 / ДЕТАЛИ')
s=s.replace('Роман Чашин — дизайнер, работающий с графикой, интерфейсами и иллюстрацией. В серии «След» авторская концепция соединяет культурные символы, ретро-3D и современный выставочный плакат.','Я Роман Чашин — графический дизайнер и иллюстратор. Продвигаю визуальный язык на стыке ремесла, стрита и PS1 low-poly: тёплая ручная фактура, независимый дух улицы и выразительная геометрия ранних игр.')
s=s.replace('Roman Chashin art style в этом проекте — взаимодействие ремесленной фактуры и цифровой геометрии. В центре не технология, а человек, который передаёт смысл дальше.','Roman Chashin art style — не стерильная цифровая картинка. Мне интересны потёртости, видимые грани и след человеческого жеста. От культурной памяти в серии «След» до скейтбординга, BMX и трюковых самокатов в Street Code.')
s=s.replace('Roman Chashin is a graphic designer and illustrator. “Pass It On” is a three-part art poster concept exploring cultural memory through low-poly geometry, retro PlayStation aesthetics and digital craft.','Roman Chashin is a graphic designer and illustrator combining traditional craft, street culture and retro PlayStation 1 low-poly aesthetics. Explore “Pass It On” and the upcoming “Street Code” series on skateboarding, BMX and freestyle scooters.')
s=s.replace('На этой странице так обозначен визуальный подход Романа Чашина к серии «След»: низкополигональная геометрия, эстетика ранних 3D-игр, традиционный орнамент и контраст тёплых материалов с цифровым светом.','Это авторский визуальный подход Романа Чашина: тактильность ремесла, энергия уличной культуры и low-poly графика эпохи PlayStation 1. Традиционный орнамент, бетон, теги, пиксельные фактуры и видимые полигоны образуют единый язык.')
s=s.replace('свяжитесь с Roman Chashin через <a href="https://www.behance.net/Roman_chashin" target="_blank" rel="noopener noreferrer">Behance</a>','свяжитесь с Roman Chashin через <a href="https://t.me/Spike_Spige_L" target="_blank" rel="noopener noreferrer">Telegram</a>')
s=re.sub(r'  <section class="contact-section.*?</section>',lambda _:Path('/home/user/qa/contact-section.html').read_text().rstrip(),s,flags=re.S)
s=s.replace('КОНЦЕПЦИЯ И АРТ-ДИРЕКШН СЕРИИ «СЛЕД»','РЕМЕСЛО × СТРИТ × PS1 LOW-POLY')
s=s.replace('<button id="share-button"','<div class="footer-social"><a href="https://vk.ru/you.should.befriendly" target="_blank" rel="noopener noreferrer">VK ↗</a><a href="https://t.me/Spike_Spige_L" target="_blank" rel="noopener noreferrer">TELEGRAM ↗</a></div><button id="share-button"')
s=s.replace('<dialog id="art-dialog"','<button class="motion-toggle" id="motion-toggle" type="button" aria-pressed="false" hidden><span class="motion-icon" aria-hidden="true">Ⅱ</span> <span class="motion-label">Анимация</span></button>\n<dialog id="art-dialog"')
pattern=r'(<script type="application/ld\+json" id="structured-data">)(.*?)(</script>)'
m=re.search(pattern,s,re.S);data=json.loads(m[2])
for x in data['@graph']:
 if x['@type']=='Person':
  x['sameAs']+=['https://vk.ru/you.should.befriendly','https://t.me/Spike_Spige_L']
  x['description']='Роман Чашин — дизайнер и иллюстратор. Авторский визуальный язык: ремесло, стрит-культура и PS1 low-poly.'
 if x['@type'] in ['WebSite','CollectionPage']:x['name']='Roman Chashin art style — ремесло, стрит и PS1 low-poly'
 if x['@type']=='CollectionPage':
  x['description']='Авторский визуальный язык Романа Чашина: ремесло, уличная культура и эстетика PlayStation 1. Серии След и Street Code.'
  x['about']=[{'@id':'#roman-chashin'},{'@id':'#series'},{'@id':'#street'}]
data['@graph'].append({'@type':'CreativeWorkSeries','@id':'#street','name':'Street Code / Ремесло движения','creator':{'@id':'#roman-chashin'},'description':'Концепция новой серии про скейтбординг, BMX и трюковые самокаты в эстетике ремесла, стрита и PS1 low-poly. Изображения будут добавлены.'})
s=re.sub(pattern,lambda m:m[1]+'\n'+json.dumps(data,ensure_ascii=False,indent=2)+'\n  '+m[3],s,flags=re.S)
p.write_text(s)
# Original neutral layout slots: no generated sports artworks.
for key,number,label,color in [('skate','01','SKATE','#bda18a'),('bmx','02','BMX','#9baab0'),('scooter','03','SCOOTER','#b4b8a0')]:
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="900" viewBox="0 0 720 900"><rect width="720" height="900" fill="#282b28"/><defs><pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="#eae9e2" stroke-opacity=".07"/></pattern></defs><rect width="720" height="900" fill="url(#grid)"/><g fill="none" stroke="{color}" stroke-width="1" opacity=".5"><path d="M60 180H660V720H60Z" stroke-dasharray="4 12"/><path d="M60 180 660 720M660 180 60 720"/><circle cx="360" cy="450" r="175"/><path d="M360 230V670M140 450H580"/></g><text x="360" y="507" text-anchor="middle" fill="{color}" font-family="Arial,sans-serif" font-weight="700" font-size="170" letter-spacing="-10">{number}</text><rect x="208" y="554" width="304" height="34" fill="#282b28"/><text x="360" y="576" text-anchor="middle" fill="{color}" font-family="monospace" font-size="15" letter-spacing="4">{label} / PLACEHOLDER</text><g fill="none" stroke="{color}" stroke-width="3"><path d="M40 90V40H90M630 40H680V90M40 810V860H90M630 860H680V810"/></g><text x="48" y="825" fill="{color}" font-family="monospace" font-size="13" letter-spacing="3">STREET CODE — ROMAN CHASHIN</text></svg>'''
 (root/'assets'/f'street-{key}.svg').write_text(svg)
print('Content, contact links, SEO, sports placeholders updated.')
