#!/usr/bin/env python3
"""CHASHIN: exact modular geometry and projection adapted from the supplied HTML.
Static SVG assets are generated ahead of time; no browser dependency is required.
"""
from pathlib import Path
from math import cos, pi, hypot
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BRAND = ROOT / 'assets/brand'
U, H, COS = 100, 1.2, cos(pi / 6)
CELLS = [(0, y) for y in range(4)]
for x in range(1, 4):
    CELLS.extend([(x, 0), (x, 3)])
ORDERED = sorted(CELLS, key=lambda c: c[0] + c[1])
PALETTE = ['#FF7A44', '#E04A15', '#BC340C']

def project(x, y, z):
    return ((x - y) * COS * U, ((x + y) * .5 - z) * U)

def faces(cell):
    x, y = cell
    return [
        [project(x,y,H), project(x+1,y,H), project(x+1,y+1,H), project(x,y+1,H)],
        [project(x,y+1,H), project(x+1,y+1,H), project(x+1,y+1,0), project(x,y+1,0)],
        [project(x+1,y,H), project(x+1,y+1,H), project(x+1,y+1,0), project(x+1,y,0)]
    ]

POINTS = [p for cell in CELLS for face in faces(cell) for p in face]
MINX, MAXX = min(p[0] for p in POINTS), max(p[0] for p in POINTS)
MINY, MAXY = min(p[1] for p in POINTS), max(p[1] for p in POINTS)
WIDTH, HEIGHT = MAXX-MINX, MAXY-MINY

def pts(points): return ' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
def viewbox(pad=24): return f'{MINX-pad:.2f} {MINY-pad:.2f} {WIDTH+2*pad:.2f} {HEIGHT+2*pad:.2f}'
def bodies(color=None):
    result = []
    for i, cell in enumerate(ORDERED):
        content = ''
        for j, face in enumerate(faces(cell)):
            fill = color or PALETTE[j]
            content += f'<polygon points="{pts(face)}" fill="{fill}" stroke="{fill}" stroke-width="0.8"/>'
        result.append(f'<g class="ch-vox" data-module="{i}">{content}</g>')
    return ''.join(result)

def svg(color=None,pad=24):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox(pad)}" shape-rendering="geometricPrecision"><title>CHASHIN — low-poly geometry</title>{bodies(color)}</svg>'

def wire():
    grid = ''
    for k in range(-1,6):
        for a,b in [(project(k,-1,0),project(k,5,0)), (project(-1,k,0),project(5,k,0))]:
            length=hypot(b[0]-a[0],b[1]-a[1])
            grid += f'<line class="ch-wire-line ch-grid-line" x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" data-length="{length:.2f}"/>'
    lines = ''
    for cell in ORDERED:
        for face in faces(cell):
            length=sum(hypot(face[(i+1)%4][0]-face[i][0],face[(i+1)%4][1]-face[i][1]) for i in range(4))
            lines += f'<polygon class="ch-wire-line" points="{pts(face)}" data-length="{length:.2f}"/>'
    return '<g class="ch-grid">'+grid+'</g><g class="ch-wire">'+lines+'</g>'

def icon():
    scale=512*.75/max(WIDTH,HEIGHT)
    tx=256-(MINX+MAXX)/2*scale;ty=256-(MINY+MAXY)/2*scale
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>CHASHIN</title><rect width="512" height="512" rx="112" fill="#14120F"/><g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.6f})">{bodies()}</g></svg>'

if __name__ == '__main__':
    BRAND.mkdir(exist_ok=True)
    for name,color,pad in [('mark-iso',None,24),('mark-orange',None,24),('mark-micro',None,4),('mark-ink','#23241f',24),('mark-black','#000000',24),('mark-bone','#eae9e2',24)]:
        (BRAND/(name+'.svg')).write_text(svg(color,pad))
    (ROOT/'assets/favicon.svg').write_text(icon())
    # Keep the outlined CHASHIN typography, replacing only the symbol group.
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    for name,ink in [('logo-lockup','#23241f'),('logo-lockup-inverse','#eae9e2')]:
        old=ET.parse(BRAND/(name+'.svg')).getroot()
        group=old.find('{http://www.w3.org/2000/svg}g')
        text=''.join(ET.tostring(node,encoding='unicode') for node in list(group) if node.tag.endswith('path'))
        scale=188/WIDTH; tx=16-MINX*scale;ty=32-MINY*scale
        new=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 813 216"><title>Roman Chashin — логотип</title><g fill="{ink}"><g transform="translate({tx:.3f} {ty:.3f}) scale({scale:.6f})">{bodies()}</g>{text}</g></svg>'
        (BRAND/(name+'.svg')).write_text(new)
    print('CHASHIN: 10 modules, 30 quads, three source colours, exact 30-degree projection.')
