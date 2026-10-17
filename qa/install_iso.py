from pathlib import Path
import re,json
root=Path('/home/user/chashin-site');brand=root/'assets/brand'
TOP='M16 47 76 12 116 35 86 52 66 40 46 52 76 69 56 81 16 58Z'
LEFT='M16 58 56 81 56 117 16 94Z'
FRONT='M56 81 76 69 76 105 56 117Z'
RIGHT='M86 52 116 35 116 71 86 88Z'
PP=[TOP,LEFT,FRONT,RIGHT]
def shapes(color=None):
 return ''.join(f'<path d="{p}" fill="{color or ("#FF6B3D" if i==0 else "#B32B04")}"/>' for i,p in enumerate(PP))
def svg(color=None,view='0 0 132 132'):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}"><title>CHASHIN — Изометрическая скоба</title>'+shapes(color)+'</svg>'
(brand/'mark-iso.svg').write_text(svg())
for n,c in [('mark-ink','#23241f'),('mark-black','#000000'),('mark-bone','#eae9e2'),('mark-orange',None)]: (brand/(n+'.svg')).write_text(svg(c))
(brand/'mark-micro.svg').write_text(svg(view='10 6 112 118'))
for n in ['logo-lockup','logo-lockup-inverse']:
 p=brand/(n+'.svg');s=p.read_text();s=re.sub(r'(<g fill="[^"]+">)(?:<path d="[^"]+"/>){2}',lambda m:m[1]+'<g transform="translate(0 8) scale(1.5)">'+shapes()+'</g>',s,count=1);p.write_text(s)
(root/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="6 2 120 126"><title>CHASHIN</title><rect x="6" y="2" width="120" height="126" rx="12" fill="#141414"/>'+shapes()+'</svg>')
# Preserve the exact supplied geometry and palette as a source reference.
(brand/'reference-original.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300"><rect width="300" height="300" fill="#141414" rx="16"/><g transform="translate(84 63)">'+shapes().replace(f'd="{FRONT}" fill="#B32B04"',f'd="{FRONT}" fill="#E23B0B"')+'</g><text x="150" y="260" text-anchor="middle" fill="#777" font-family="monospace" font-size="11" letter-spacing="2">05 / RAW ISO STAPLE</text></svg>')
p=root/'index.html';s=p.read_text()
s=s.replace('CHASHIN / «ЗАЦЕП»','CHASHIN / RAW ISO STAPLE').replace('CH—03 / АБСТРАКТНЫЙ ЗНАК','CH—05 / ИЗОМЕТРИЧЕСКАЯ СКОБА').replace('2 КОНТУРА · 1 ЦВЕТ','4 ГРАНИ · 2 ТОНА')
diagram=f'''<svg class="identity-diagram" viewBox="-16 -16 164 164" role="img" aria-labelledby="identity-svg-title"><title id="identity-svg-title">Изометрическая скоба: светлая верхняя грань и тёмные боковые грани</title><g class="iso-sides" fill="#B32B04"><path d="{LEFT}"/><path d="{FRONT}"/><path d="{RIGHT}"/></g><path class="iso-top" d="{TOP}" fill="#FF6B3D"/><g class="iso-construction" fill="none" stroke="#828879" stroke-width=".6" stroke-dasharray="2 2"><path d="M16 47 76 12 116 35M16 47V94M116 35V71M56 81V117M56 117 76 105M46 52 66 40 86 52"/></g></svg>'''
s=re.sub(r'<svg class="identity-diagram".*?</svg>',lambda _:diagram,s,count=1,flags=re.S)
s=s.replace('Две сцепленные массы. Форму определяет вырез.','Светлая плоскость. Тёмная толщина. Два тона.')
s=s.replace('>Вычитание</button>','>Контур</button>').replace('>Сцепление</button>','>Грани</button>')
s=s.replace('<h3>«Зацеп»</h3>','<h3>Изометрическая<br>скоба</h3>')
s=s.replace('Плотный силуэт с вырезанным каналом. Он делит цельную форму на две части: выступ правой входит в полость левой.','С-образный брусок, повёрнутый в изометрии. Светлая верхняя плоскость задаёт форму, тёмные боковые грани показывают толщину.')
s=s.replace('Главный элемент здесь — не линия, а пустота. Канал меняет направление, огибает выступ и выходит за пределы формы. Детали не наложены крест-накрест: они сцеплены, как элементы вырезанного замка.','Вырез делает силуэт открытым. Изометрия даёт ощущение предмета — как небольшая деталь из раннего 3D. Ремесленная простота и геометрия PS1 без градиентов, текстур и декоративных эффектов.')
s=s.replace('<dt>Конструкция</dt><dd>2 массы</dd>','<dt>Конструкция</dt><dd>4 грани</dd>').replace('<dt>Базовый зазор</dt><dd>16 ед.</dd>','<dt>Палитра</dt><dd>2 тона</dd>').replace('<dt>Скосы</dt><dd>45°</dd>','<dt>Проекция</dt><dd>Изометрия</dd>').replace('<dt>Габарит</dt><dd>168 × 160</dd>','<dt>Габарит</dt><dd>100 × 105</dd>')
s=s.replace('href="assets/brand/mark-ink.svg" download="CHASHIN-mark.svg"','href="assets/brand/mark-iso.svg" download="CHASHIN-mark.svg"')
meaning=f'''    <div class="identity-meaning-grid">
      <article><span class="eyebrow">01 / ФОРМА</span><svg class="meaning-symbol" viewBox="0 0 132 132" aria-hidden="true"><path d="{TOP}" fill="#FF6B3D"/></svg><h3>Верхняя плоскость</h3><p>С-образная скоба с открытым вырезом. Геометрия взята из выбранного эскиза: без добавленных перемычек и новых символов.</p></article>
      <article><span class="eyebrow">02 / ТОЛЩИНА</span><svg class="meaning-symbol" viewBox="0 0 132 132" aria-hidden="true"><path d="{LEFT}" fill="#B32B04"/><path d="{FRONT}" fill="#B32B04"/><path d="{RIGHT}" fill="#B32B04"/></svg><h3>Предмет, а не линия</h3><p>Три боковые грани образуют толщину бруска. Один тёмный оттенок удерживает их вместе, не дробя знак на лишние цвета.</p></article>
      <article><span class="eyebrow">03 / ДВА ТОНА</span><div class="meaning-symbol iso-swatches" aria-hidden="true"><i></i><i></i></div><h3>Объём без градиента</h3><p>Светлый оранжевый #FF6B3D и тёмный #B32B04. Разница тона объясняет объём, а не украшает поверхность.</p></article>
    </div>
'''
s=re.sub(r'    <div class="identity-meaning-grid">.*?(?=    <div class="identity-process")',lambda _:meaning,s,flags=re.S)
s=s.replace('Три эстетики без буквального инициала. Задача — найти самостоятельный принцип формы.','Взять выбранную С-образную скобу. Сохранить её предметный характер и открытый вырез.')
s=s.replace('Общий блок минус фигурный канал. На выходе — два самостоятельных замкнутых контура.','Четыре замкнутых полигона. Верхняя плоскость и три боковые грани; исходная геометрия сохранена.')
s=s.replace('Верхний и нижний разрезы смещены. Асимметрия внутри делает статичный силуэт напряжённым.','Убрать третий оттенок из эскиза. Оставить светлый верх и единую тёмную толщину.')
s=s.replace('Основной знак для крупных носителей. Микроверсия — с увеличенным зазором.','Для малых размеров — плотнее кадрирование. 16 px — предельный размер, 24–32 px читаются увереннее.')
s=s.replace('Оставлять вокруг не меньше 16 координатных единиц свободного поля. Не растягивать, не скруглять углы и не закрывать промежутки. Основная версия — от 48 px по высоте; ниже — микроверсия.','Не менять угол проекции и пропорции, не закрывать вырез. Для небольших иконок использовать компактное поле SVG. На 16 px мелкие грани сближаются; для уверенной читаемости предпочтительнее 24–32 px и выше.')
s=s.replace('знак Зацеп','изометрическая скоба').replace('ГОРИЗОНТАЛЬНАЯ КОМПОЗИЦИЯ / ОДИН ЦВЕТ','ГОРИЗОНТАЛЬНАЯ КОМПОЗИЦИЯ / ДВА ТОНА')
s=s.replace('class="brand-monogram" src="assets/brand/mark-micro.svg"','class="brand-monogram" src="assets/brand/mark-iso.svg"')
s=s.replace('src="assets/brand/mark-orange.svg"','src="assets/brand/mark-iso.svg"')
s=s.replace('<div class="identity-sticker"><img src="assets/brand/mark-ink.svg"','<div class="identity-sticker"><img src="assets/brand/mark-iso.svg"')
s=s.replace('CHASHIN — Зацеп: концепция абстрактного знака и разбор логотипа','CHASHIN — Изометрическая скоба: конструкция и применение логотипа')
s=s.replace('Собственная айдентика: цельная масса, фигурное вычитание и две сцепленные детали. Чистый вектор, негативное пространство, конструкция и применение.','Изометрическая С-образная скоба. Четыре векторные грани и два тона оранжевого. Форма, толщина, конструкция и применение.')
s=s.replace('"image": "assets/brand/mark-ink.svg"','"image": "assets/brand/mark-iso.svg"')
p.write_text(s)
p=root/'script.js';s=p.read_text().replace('Две сцепленные массы. Форму определяет вырез.','Светлая плоскость. Тёмная толщина. Два тона.').replace('Оранжевое — вычитаемый канал. Остальное образует две детали.','Контуры четырёх граней. Геометрия исходного эскиза.').replace('Детали разнесены: выступ правой повторяет полость левой.','Верхняя плоскость отделена от боковых граней.');p.write_text(s)
Path('/home/user/qa/iso-paths.json').write_text(json.dumps(PP))
print('Installed exact supplied geometry; production logo has two orange tones.')
