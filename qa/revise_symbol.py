from pathlib import Path
import re,json,shutil
root=Path('/home/user/chashin-site');out=root/'assets/brand'
# Two crossing ribbons; the lower ribbon is interrupted by real negative space.
UP='M20 140 140 20H164L180 36V60L60 180H36L20 164Z'
NW='M20 36 36 20H60L94 54 54 94 20 60Z'
SE='M106 146 146 106 180 140V164L164 180H140Z'
MNW='M20 36 36 20H60L90 50 50 90 20 60Z'
MSE='M110 150 150 110 180 140V164L164 180H140Z'
paths=[UP,NW,SE]
def shape(color, micro=False):
 pp=[UP,MNW,MSE] if micro else paths
 return '<g fill="'+color+'">'+''.join('<path d="'+p+'"/>' for p in pp)+'</g>'
def svg(color,micro=False):return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><title>CHASHIN — Переплетение</title>'+shape(color,micro)+'</svg>'
for name,c in [('mark-ink','#23241f'),('mark-black','#000000'),('mark-bone','#eae9e2'),('mark-orange','#fa542b')]: (out/f'{name}.svg').write_text(svg(c))
(out/'mark-micro.svg').write_text(svg('#23241f',True))
# Preserve outlined wordmark, replace just the first two paths of old lockup.
for name,c in [('logo-lockup','#23241f'),('logo-lockup-inverse','#eae9e2')]:
 p=out/f'{name}.svg';s=p.read_text();s=re.sub(r'(<g fill="[^"]+">)<path d="[^"]+"/><path d="[^"]+"/>',lambda m:m[1]+''.join('<path d="'+d+'"/>' for d in paths),s,count=1);p.write_text(s)
(root/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><title>CHASHIN</title><rect width="200" height="200" rx="30" fill="#fa542b"/>'+shape('#23241f',True)+'</svg>')
p=root/'index.html';s=p.read_text()
# Main interactive drawing, actual construction with 45 degree separation lines.
diagram='''<svg class="identity-diagram" viewBox="-20 -20 240 240" role="img" aria-labelledby="identity-svg-title"><title id="identity-svg-title">Абстрактный знак Переплетение: две гранёные ленты проходят одна над другой</title><defs><pattern id="identity-grid-pattern" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M10 0H0V10" fill="none" stroke="#7d8172" stroke-width=".35"/></pattern></defs><g class="identity-grid-lines" aria-hidden="true"><rect x="-10" y="-10" width="220" height="220" fill="url(#identity-grid-pattern)"/><path d="M20 0V200M180 0V200M0 20H200M0 180H200M10 190 190 10M10 10 190 190" fill="none" stroke="#fa542b" stroke-width=".6" stroke-dasharray="2 2"/></g><g class="identity-under" fill="#23241f"><path class="identity-tail-nw" d="'''+NW+'''"/><path class="identity-tail-se" d="'''+SE+'''"/></g><path class="identity-over" fill="#23241f" d="'''+UP+'''"/><path class="identity-seam" d="M54 94 94 54M106 146 146 106" fill="none" stroke="#fa542b" stroke-width="1.2"/></svg>'''
s=re.sub(r'<svg class="identity-diagram".*?</svg>',lambda _:diagram,s,count=1,flags=re.S)
s=s.replace('CHASHIN / «СТЫК»','CHASHIN / «ПЕРЕПЛЕТЕНИЕ»').replace('CH—01 / МОНОГРАММА «Ч»','CH—02 / АБСТРАКТНЫЙ ЗНАК').replace('2 КОНТУРА · 1 ЦВЕТ','3 КОНТУРА · 1 ЦВЕТ')
s=s.replace('Знак целиком. Две детали — одна буква.','Две ленты. Одно переплетение. Никаких букв.')
s=s.replace('<h3>«Стык»</h3>','<h3>«Переплетение»</h3>')
s=s.replace('Монограмма «Ч» — первая буква фамилии. Не набранная шрифтом, а собранная из двух самостоятельных деталей.','Не инициал и не пиктограмма. Две гранёные ленты пересекаются: одна проходит сверху, другая продолжается под ней.')
s=s.replace('Левая часть задаёт движение, правая держит конструкцию. Между ними — точный зазор. Он превращает обычную букву в соединение: здесь встречаются разные материалы, культуры и времена.','Переплетение — принцип ремесла. Встреча траекторий — энергия улицы. Крупные плоскости и срезанные углы — логика low-poly. Вместе они дают самостоятельный символ, который дополняет типографику, а не изображает букву.')
s=s.replace('<dt>Модуль</dt><dd>1u</dd>','<dt>Ритм</dt><dd>2 ленты</dd>').replace('<dt>Зазор</dt><dd>1u</dd>','<dt>Пауза</dt><dd>8,5 ед.</dd>').replace('<dt>Форма знака</dt><dd>19u × 21u</dd>','<dt>Пропорции</dt><dd>1 : 1</dd>')
meaning='''    <div class="identity-meaning-grid">
      <article><span class="eyebrow">01 / РЕМЕСЛО</span><svg class="meaning-symbol" viewBox="0 0 200 200" aria-hidden="true"><path d="'''+NW+'''" fill="#8c8e80"/><path d="'''+SE+'''" fill="#8c8e80"/><path d="'''+UP+'''" fill="#23241f"/></svg><h3>Над и под</h3><p>Как нити в ткани: одна линия перекрывает другую. Пустые промежутки показывают порядок переплетения без теней и объёма.</p></article>
      <article><span class="eyebrow">02 / СТРИТ</span><svg class="meaning-symbol" viewBox="0 0 200 200" aria-hidden="true"><path d="M35 165 165 35M35 35 70 70M130 130 165 165" fill="none" stroke="#23241f" stroke-width="14"/><path d="M35 165 165 35" fill="none" stroke="#fa542b" stroke-width="4"/><circle cx="35" cy="165" r="10" fill="#fa542b"/><circle cx="165" cy="35" r="10" fill="#fa542b"/></svg><h3>Встреча траекторий</h3><p>Две диагонали передают движение и столкновение направлений. Знак работает как отметка на деке, наклейка или независимый тег.</p></article>
      <article><span class="eyebrow">03 / PS1 LOW-POLY</span><svg class="meaning-symbol" viewBox="0 0 200 200" aria-hidden="true"><path d="'''+UP+'''" fill="none" stroke="#23241f" stroke-width="2"/><path d="M20 140 180 60M140 20 60 180M164 20 180 36M36 180 20 164" fill="none" stroke="#fa542b" stroke-width="2"/></svg><h3>Грань вместо эффекта</h3><p>Срезы под 45°, жёсткий силуэт, минимум деталей. Эстетика раннего 3D выражена геометрией, а не фильтром поверх картинки.</p></article>
    </div>
'''
s=re.sub(r'    <div class="identity-meaning-grid">.*?(?=    <div class="identity-process")',lambda _:meaning,s,flags=re.S)
s=s.replace('Три эстетики, одна фамилия. Задача — соединить их без набора буквальных символов.','Три эстетики без буквального инициала. Задача — найти самостоятельный принцип формы.')
s=s.replace('Буква «Ч», два контура, единый модуль. Стык становится главным отличием.','Две диагональные ленты. Разрывы нижней создают эффект переплетения: всего три контура.')
s=s.replace('Правая стойка шире левой. Это уравновешивает массивную диагональную часть.','Равные диагонали держат квадратный силуэт. Срезанные углы смягчают тяжёлую массу.')
s=s.replace('Оставлять вокруг минимум 3u свободного поля. Не растягивать, не скруглять углы и не закрывать стык.','Оставлять вокруг минимум 20 единиц свободного поля — ⅛ ширины самого знака. Не растягивать, не скруглять углы и не закрывать промежутки.')
s=s.replace('Логотип Roman Chashin: монограмма Ч и надпись CHASHIN, переведённая в векторные контуры','Логотип Roman Chashin: знак Переплетение и надпись CHASHIN в векторных контурах').replace('Одноцветная монограмма CHASHIN на макете наклейки','Абстрактный знак CHASHIN на макете наклейки')
s=s.replace('width="200" height="216"','width="200" height="200"').replace('class="brand-monogram"','class="brand-monogram"').replace('width="38" height="41"','width="38" height="38"')
s=s.replace('class="hero-logo-link" href="#identity"','class="hero-logo-link" href="#identity"').replace('width="66" height="72"','width="120" height="120"')
s=s.replace('CHASHIN — Стык: концепция монограммы и разбор логотипа','CHASHIN — Переплетение: концепция абстрактного знака и разбор логотипа').replace('Собственная айдентика: монограмма Ч из двух векторных контуров. Идея, модульная геометрия, негативное пространство, микроверсия и применение.','Собственная айдентика: две переплетённые ленты, три векторных контура. Ремесло, стрит и low-poly. Идея, геометрия, негативное пространство и применение.')
p.write_text(s)
p=root/'script.js';s=p.read_text().replace('Знак целиком. Две детали — одна буква.','Две ленты. Одно переплетение. Никаких букв.').replace('Модуль 1u. Зазор 1u. Габарит знака 19u × 21u.','Квадратный силуэт. Диагонали 45°. Габарит 160 × 160.').replace('Две самостоятельные детали. Оранжевая — опорная стойка.','Оранжевая лента сверху. Два тёмных фрагмента продолжаются под ней.');p.write_text(s)
Path('/home/user/qa/new-symbol-paths.json').write_text(json.dumps(paths))
print('Abstract interlaced symbol installed across site.')
