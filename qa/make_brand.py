from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import json
root=Path('/home/user/chashin-site');out=root/'assets/brand'
A='M24 40 40 24H64V80L88 104H136V144H72L24 96Z'
B='M128 24H160L176 40V176L160 192H128V152H144V96H128Z'
MICROA='M24 40 40 24H64V80L88 104H132V144H72L24 96Z'
MICROB='M128 24H160L176 40V176L160 192H128V156H144V92H128Z'
def symbol(color='#23241f',micro=False):
 a,b=(MICROA,MICROB) if micro else (A,B)
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 216"><title>CHASHIN — монограмма Ч, Стык</title><g fill="{color}"><path d="{a}"/><path d="{b}"/></g></svg>'
for name,color in [('mark-ink','#23241f'),('mark-bone','#eae9e2'),('mark-orange','#fa542b')]:
 (out/f'{name}.svg').write_text(symbol(color))
(out/'mark-micro.svg').write_text(symbol(micro=True))
font=TTFont(root/'assets/fonts/onest-bold.ttf');glyphs=font.getGlyphSet();cmap=font.getBestCmap();upem=font['head'].unitsPerEm

def lettering(text,x,y,size,tracking=0):
 scale=size/upem;parts=[]
 for char in text:
  name=cmap[ord(char)];g=glyphs[name];pen=SVGPathPen(glyphs)
  tr=TransformPen(pen,(scale,0,0,-scale,x,y));g.draw(tr)
  if pen.getCommands():parts.append('<path d="'+pen.getCommands()+'"/>')
  x+=g.width*scale+tracking
 return ''.join(parts),x
word,end=lettering('CHASHIN',232,150,124,-3)
sub,_=lettering('ROMAN / ART & DESIGN',237,188,15,2)
width=round(end+22)
lockup=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 216"><title>Roman Chashin — фирменный логотип</title><g fill="#23241f"><path d="{A}"/><path d="{B}"/>{word}{sub}</g></svg>'
(out/'logo-lockup.svg').write_text(lockup)
(out/'logo-lockup-inverse.svg').write_text(lockup.replace('#23241f','#eae9e2'))
word,ww=lettering('CHASHIN',0,110,145,-3)
(out/'wordmark.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {round(ww)} 124"><title>CHASHIN</title><g fill="#23241f">{word}</g></svg>')
# Micro-sized browser icon with intentional oversize and no arrow.
favicon=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="16 16 168 184"><title>CHASHIN</title><rect x="16" y="16" width="168" height="184" rx="24" fill="#fa542b"/><g fill="#23241f"><path d="{MICROA}"/><path d="{MICROB}"/></g></svg>'
(root/'assets/favicon.svg').write_text(favicon)
Path('/home/user/qa/brand-paths.json').write_text(json.dumps({'arm':A,'spine':B,'microArm':MICROA,'microSpine':MICROB}))
print('Vector symbol and outlined wordmarks created. Lockup width:',width)
