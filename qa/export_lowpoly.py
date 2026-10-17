from pathlib import Path
import shutil,cairosvg
from PIL import Image
root=Path('/home/user/chashin-site');brand=root/'assets/brand';kit=Path('/home/user/chashin-brand')
for old in ['source-reference.svg','brand-geometry.py']:
 p=kit/old
 if p.exists():p.unlink()
for f in brand.glob('*.svg'):shutil.copy2(f,kit/f.name)
for name in ['mark-iso','mark-ink','logo-lockup']:
 cairosvg.svg2pdf(url=str(brand/(name+'.svg')),write_to=str(kit/(name+'.pdf')))
cairosvg.svg2png(url=str(brand/'mark-iso.svg'),write_to=str(kit/'mark-transparent.png'),output_width=1024)
cairosvg.svg2png(url=str(root/'assets/favicon.svg'),write_to=str(kit/'favicon-64.png'),output_width=64,output_height=64)
Image.open(kit/'favicon-64.png').save(root/'assets/favicon.ico',sizes=[(16,16),(32,32),(64,64)])
for name in ['favicon.svg','favicon.ico']:shutil.copy2(root/'assets'/name,kit/name)
docs='''## Логотип CHASHIN — low-poly геометрия

Геометрия и палитра взяты из загруженного HTML-референса по выбору пользователя. На сайте используется CHASHIN; название исходного шаблона, чужие контакты и фиктивные реквизиты не перенесены.

10 модулей на плане 4 × 4u, высота 1.2u, изометрические оси 30°. Каждый модуль представлен верхним и двумя боковыми четырёхугольниками. Всего 30 полигонов в исходной SVG-сборке, включая перекрытые поверхности. При разбиении каждой грани пополам — 60 треугольников до оптимизации. Цвета: #FF7A44 / #E04A15 / #BC340C.

Визуальная связь с PS1 и low-poly — простая геометрия, крупные плоскости и плоский цвет, а не утверждение об использовании оригинального игрового движка.

В `#identity` работают «Знак / Построение» и «Повтор». Анимации адаптированы из референса: сборка с шагом 70 мс, длительностью 720 мс и прорисовка каркаса через stroke-dashoffset. Запуск при появлении блока, переключении режима и нажатии повтора. Знак рядом с PS1 собирается на старте и при наведении мыши.

Общая кнопка движения и prefers-reduced-motion отключают анимации, включая уже запущенные. Без JavaScript готовый знак и тексты уже есть в HTML. Выставка, Street Code и контакты сохранены.

`brand-geometry.py` в исходниках сайта — генератор SVG (Python 3, стандартная библиотека). Формула: x'=(x-y)·cos(30°)·100, y'=((x+y)/2-z)·100. Генератор обновляет файлы SVG и favicon; встроенные SVG-демонстрации в index.html — статический снимок, при изменении конструкции их необходимо обновлять отдельно.

Не переносились CDN, внешние шрифты, фотографии и неверные размерные подписи из шаблона. Вектор масштабируется без потери резкости, но на 16 px части могут сближаться; рекомендуемый размер для ясного чтения — 24–32 px и больше. Проверка товарного знака не проводилась.
'''
p=root/'README.md';s=p.read_text().split('## Логотип CHASHIN')[0]+docs;p.write_text(s)
(kit/'README.md').write_text('''# CHASHIN — LOW-POLY GEOMETRY

Геометрия из предоставленного пользователем HTML-референса, выбранная для бренда CHASHIN.

## Файлы

- mark-iso.svg — основной трёхтоновый знак, прозрачный фон.
- mark-orange.svg — совместимое имя той же версии.
- mark-micro.svg — компактное кадрирование, без изменения формы.
- mark-ink.svg / mark-black.svg / mark-bone.svg — одноцветный силуэт.
- logo-lockup.svg / logo-lockup-inverse.svg — знак и CHASHIN в контурах.
- wordmark.svg — надпись CHASHIN отдельно.
- mark-iso.pdf / mark-ink.pdf / logo-lockup.pdf — векторные PDF.
- mark-transparent.png — прозрачный экспорт шириной 1024 px.
- favicon.svg / favicon.ico / favicon-64.png — иконки на тёмном фоне.

Все SVG векторные, без растров и внешних шрифтов. Надпись подготовлена из Onest Bold, лицензия — OFL-Onest.txt. Монохром сохраняет силуэт, но не разделение граней. Не менять проекцию, пропорции модулей и внутренний вырез.

'''+docs)
p=Path('/home/user/qa/package_brand.py');s=p.read_text().replace('CHASHIN — Изометрическая скоба','CHASHIN — Low-poly геометрия').replace('ЧЕТЫРЕ ГРАНИ','30 ПОЛИГОНОВ');p.write_text(s)
