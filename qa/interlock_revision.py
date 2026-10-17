from pathlib import Path
import re,json
root=Path('/home/user/chashin-site');brand=root/'assets/brand'
AA=[(48,20),(96,20),(96,60),(72,60),(56,76),(56,116),(72,132),(128,132),(128,180),(48,180),(16,148),(16,52)]
BB=[(112,20),(152,20),(184,52),(184,148),(152,180),(144,180),(144,116),(88,116),(72,100),(72,92),(88,76),(112,76)]
OO=[(48,20),(152,20),(184,52),(184,148),(152,180),(48,180),(16,148),(16,52)]
CC=[(96,20),(112,20),(112,76),(88,76),(72,92),(72,100),(88,116),(144,116),(144,180),(128,180),(128,132),(72,132),(56,116),(56,76),(72,60),(96,60)]
MA=[(48,20),(92,20),(92,56),(68,56),(52,72),(52,120),(68,136),(124,136),(124,180),(48,180),(16,148),(16,52)]
def path(pts):return 'M'+' '.join(f'{x} {y}' for x,y in pts)+'Z'
A,B,O,C,M=map(path,[AA,BB,OO,CC,MA])
def area(p):return abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2)
assert area(AA)+area(BB)+area(CC)==area(OO)
def symbol(color,micro=False):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><title>CHASHIN — Зацеп</title><g fill="{color}"><path d="{M if micro else A}"/><path d="{B}"/></g></svg>'
for n,c in [('mark-ink','#23241f'),('mark-black','#000000'),('mark-bone','#eae9e2'),('mark-orange','#fa542b')]: (brand/(n+'.svg')).write_text(symbol(c))
(brand/'mark-micro.svg').write_text(symbol('#23241f',True))
for n in ['logo-lockup','logo-lockup-inverse']:
 p=brand/(n+'.svg');s=p.read_text();s=re.sub(r'(<g fill="[^"]+">)(?:<path d="[^"]+"/>){3}',lambda m:m[1]+f'<path d="{A}"/><path d="{B}"/>',s,count=1);p.write_text(s)
(root/'assets/favicon.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><title>CHASHIN</title><rect width="200" height="200" rx="24" fill="#fa542b"/><g fill="#23241f"><path d="{M}"/><path d="{B}"/></g></svg>')
p=root/'index.html';s=p.read_text()
diagram=f'''<svg class="identity-diagram" viewBox="-20 -20 240 240" role="img" aria-labelledby="identity-svg-title"><title id="identity-svg-title">Зацеп: две сцепленные массы с фигурным вырезом между ними</title><path class="identity-stock" d="{O}" fill="#23241f"/><g class="identity-interlock" fill="#23241f"><path class="interlock-left" d="{A}"/><path class="interlock-right" d="{B}"/></g><path class="identity-cut" d="{C}" fill="#fa542b"/></svg>'''
s=re.sub(r'<svg class="identity-diagram".*?</svg>',lambda _:diagram,s,count=1,flags=re.S)
s=s.replace('ПЕРЕПЛЕТЕНИЕ','ЗАЦЕП').replace('Переплетение','Зацеп').replace('CH—02','CH—03').replace('3 КОНТУРА · 1 ЦВЕТ','2 КОНТУРА · 1 ЦВЕТ')
s=s.replace('Две ленты. Одно переплетение. Никаких букв.','Две сцепленные массы. Форму определяет вырез.')
s=s.replace('>Сетка</button>','>Вычитание</button>').replace('>Сборка</button>','>Сцепление</button>')
s=s.replace('Не инициал и не пиктограмма. Две гранёные ленты пересекаются: одна проходит сверху, другая продолжается под ней.','Плотный силуэт с вырезанным каналом. Он делит цельную форму на две части: выступ правой входит в полость левой.')
s=s.replace('Зацеп — принцип ремесла. Встреча траекторий — энергия улицы. Крупные плоскости и срезанные углы — логика low-poly. Вместе они дают самостоятельный символ, который дополняет типографику, а не изображает букву.','Главный элемент здесь — не линия, а пустота. Канал меняет направление, огибает выступ и выходит за пределы формы. Детали не наложены крест-накрест: они сцеплены, как элементы вырезанного замка.')
s=s.replace('<dt>Ритм</dt><dd>2 ленты</dd>','<dt>Конструкция</dt><dd>2 массы</dd>').replace('<dt>Пауза</dt><dd>8,5 ед.</dd>','<dt>Базовый зазор</dt><dd>16 ед.</dd>').replace('<dt>Пропорции</dt><dd>1 : 1</dd>','<dt>Габарит</dt><dd>168 × 160</dd>')
meaning=f'''    <div class="identity-meaning-grid">
      <article><span class="eyebrow">01 / МАССА</span><svg class="meaning-symbol" viewBox="0 0 200 200" aria-hidden="true"><path d="{O}" fill="#23241f"/></svg><h3>Сначала — цельный блок</h3><p>Тяжёлая форма со срезанными углами. Не буква, не крест и не спортивная пиктограмма. Нейтральная заготовка с характером.</p></article>
      <article><span class="eyebrow">02 / ВЫЧИТАНИЕ</span><svg class="meaning-symbol" viewBox="0 0 200 200" aria-hidden="true"><path d="{O}" fill="#a8aa9e"/><path d="{C}" fill="#fa542b"/></svg><h3>Пустота рисует знак</h3><p>Из блока вычитается фигурный канал. Его повороты создают полость и встречный выступ. Оранжевым показано то, что убирается.</p></article>
      <article><span class="eyebrow">03 / СОЕДИНЕНИЕ</span><svg class="meaning-symbol" viewBox="-10 -5 220 210" aria-hidden="true"><path d="{A}" fill="#23241f" transform="translate(-5 0)"/><path d="{B}" fill="#fa542b" transform="translate(5 0)"/></svg><h3>Детали держат друг друга</h3><p>Внешний силуэт собирает их обратно. Внутри остаётся воздух: сцепление видно, но части не сливаются в бесформенное пятно.</p></article>
    </div>
'''
s=re.sub(r'    <div class="identity-meaning-grid">.*?(?=    <div class="identity-process")',lambda _:meaning,s,flags=re.S)
s=s.replace('Две диагональные ленты. Разрывы нижней создают эффект переплетения: всего три контура.','Общий блок минус фигурный канал. На выходе — два самостоятельных замкнутых контура.')
s=s.replace('Равные диагонали держат квадратный силуэт. Срезанные углы смягчают тяжёлую массу.','Верхний и нижний разрезы смещены. Асимметрия внутри делает статичный силуэт напряжённым.')
s=s.replace('Оставлять вокруг минимум 20 единиц свободного поля — ⅛ ширины самого знака.','Оставлять вокруг не меньше 16 координатных единиц свободного поля.')
s=s.replace('Собственная айдентика: две переплетённые ленты, три векторных контура. Ремесло, стрит и low-poly. Идея, геометрия, негативное пространство и применение.','Собственная айдентика: цельная масса, фигурное вычитание и две сцепленные детали. Чистый вектор, негативное пространство, конструкция и применение.')
s=s.replace('width="15" height="16"','width="16" height="16"').replace('width="22" height="24"','width="24" height="24"').replace('width="30" height="32"','width="32" height="32"').replace('width="44" height="48"','width="48" height="48"')
p.write_text(s)
p=root/'script.js';s=p.read_text().replace('Две ленты. Одно переплетение. Никаких букв.','Две сцепленные массы. Форму определяет вырез.').replace('Квадратный силуэт. Диагонали 45°. Габарит 160 × 160.','Оранжевое — вычитаемый канал. Остальное образует две детали.').replace('Оранжевая лента сверху. Два тёмных фрагмента продолжаются под ней.','Детали разнесены: выступ правой повторяет полость левой.');p.write_text(s)
Path('/home/user/qa/interlock-paths.json').write_text(json.dumps({'left':A,'right':B,'stock':O,'cut':C}))
print('Boolean identity verified: area(stock) = area(left) + area(right) + area(cut). New mark installed.')
