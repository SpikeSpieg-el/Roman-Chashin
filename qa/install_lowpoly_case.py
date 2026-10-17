from pathlib import Path
import runpy,re,json
root=Path('/home/user/chashin-site');g=runpy.run_path(str(root/'brand-geometry.py'))
body=g['bodies']();wire=g['wire']();v=g['viewbox'](70)
solid=f'<svg class="lp-solid-svg" xmlns="http://www.w3.org/2000/svg" viewBox="{v}" role="img" aria-label="CHASHIN: знак из десяти изометрических модулей">{body}</svg>'
draft=f'<svg class="lp-draft-svg" xmlns="http://www.w3.org/2000/svg" viewBox="{v}" role="img" aria-label="Каркас знака CHASHIN: сетка и тридцать полигонов">{wire}</svg>'
module='<svg class="meaning-symbol lp-plan" viewBox="0 0 112 112" aria-hidden="true">'
for y in range(4):
 for x in range(4):
  fill='#FF7A44' if (x,y) in g['CELLS'] else 'none'
  module+=f'<rect x="{x*27+3}" y="{y*27+3}" width="23" height="23" fill="{fill}" stroke="#8e9481" stroke-width=".7"/>'
module+='</svg>'
mesh=f'<svg class="meaning-symbol lp-mesh" viewBox="{g["viewbox"](10)}" aria-hidden="true"><g fill="none" stroke="#23241f" stroke-width="3">'+''.join(f'<polygon points="{g["pts"](f)}"/>' for c in g['ORDERED'] for f in g['faces'](c))+'</g></svg>'
section=Path('/home/user/qa/lowpoly-case-template.html').read_text().replace('{{SOLID}}',solid).replace('{{DRAFT}}',draft).replace('{{MODULE}}',module).replace('{{MESH}}',mesh)
p=root/'index.html';s=p.read_text();s=re.sub(r'  <section id="identity".*?(?=  <section class="statement)',lambda _:section,s,flags=re.S)
hero=f'<svg class="ch-live-logo" xmlns="http://www.w3.org/2000/svg" viewBox="{g["viewbox"](24)}" aria-hidden="true">{body}</svg>'
s=re.sub(r'(<a class="hero-logo-link"[^>]*>).*?(</a>)',lambda m:m[1]+hero+m[2],s,count=1,flags=re.S)
pattern=r'(<script type="application/ld\+json" id="structured-data">)(.*?)(</script>)';d=json.loads(re.search(pattern,s,re.S)[2])
for x in d['@graph']:
 if x.get('@id','').endswith('#identity'):
  x['name']='CHASHIN — low-poly геометрия личного знака'
  x['description']='Десять модулей, тридцать четырёхугольных граней, изометрическая проекция 30 градусов и три плоские заливки. Разбор связи логотипа с эстетикой low-poly и PS1.'
s=re.sub(pattern,lambda m:m[1]+'\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n  '+m[3],s,flags=re.S)
p.write_text(s)
# Remove the previous one-off logo controller; the new controller follows it.
p=root/'script.js';js=p.read_text().split('// An actual vector breakdown:',1)[0]
js=js.replace("document.body.classList.toggle('motion-on', enabled);", "document.body.classList.toggle('motion-on', enabled);\n    document.dispatchEvent(new CustomEvent('chashin:motion', { detail: { enabled } }));")
p.write_text(js)
print('Integrated reference geometry and low-poly case into the complete exhibition landing.')
