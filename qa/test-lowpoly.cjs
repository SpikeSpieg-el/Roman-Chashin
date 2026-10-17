const {chromium}=require('playwright');const assert=require('node:assert/strict');const fs=require('fs');const vm=require('vm');
(async()=>{
 const source=fs.readFileSync('/home/user/uploads/слой.html','utf8');const raw=source.split('<script>')[1].split("document.querySelectorAll('[data-mark]')")[0];
 const original=vm.runInNewContext(raw+'\nJSON.stringify(ordered.flatMap(c=>facesFor(c).map(f=>pts(f.p))))');
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:1000}});const errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto('http://127.0.0.1:3000',{waitUntil:'networkidle'});
 const actual=await p.locator('.lp-solid polygon').evaluateAll(a=>a.map(e=>e.getAttribute('points')));assert.deepEqual(actual,JSON.parse(original),'Exact reference coordinates/order');
 assert.equal(await p.locator('.lp-solid .ch-vox').count(),10);assert.equal(await p.locator('.lp-solid polygon').count(),30);
 assert.deepEqual(await p.locator('.lp-solid polygon').evaluateAll(a=>[...new Set(a.map(e=>e.getAttribute('fill')))]),['#FF7A44','#E04A15','#BC340C']);
 await p.locator('#identity').evaluate(e=>e.scrollIntoView({block:'start',behavior:'instant'}));await p.locator('#logo-replay').click();assert.equal(await p.locator('.lp-solid .ch-vox').evaluateAll(a=>a.reduce((s,e)=>s+e.getAnimations().length,0)),10);
 await p.waitForTimeout(1500);await p.screenshot({path:'/home/user/qa/lowpoly-case.png'});
 await p.locator('[data-logo-mode="grid"]').click();assert.equal(await p.locator('.lp-stage').getAttribute('data-mode'),'grid');assert.ok(await p.locator('.ch-wire-line').evaluateAll(a=>a.some(e=>e.getAnimations().length>0)));
 await p.waitForTimeout(1500);await p.locator('.identity-workbench').screenshot({path:'/home/user/qa/lowpoly-wire.png'});
 await p.locator('[data-logo-mode="mark"]').click();await p.locator('#motion-toggle').click();assert.equal(await p.locator('#logo-replay').isDisabled(),true);assert.equal(await p.locator('.lp-solid .ch-vox').evaluateAll(a=>a.reduce((s,e)=>s+e.getAnimations().length,0)),0);
 await p.locator('#motion-toggle').click();assert.equal(await p.locator('#logo-replay').isDisabled(),false);
 for(const w of [320,390,768,1440]){await p.setViewportSize({width:w,height:900});assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'Overflow at '+w)}
 await p.setViewportSize({width:390,height:844});await p.locator('#identity').evaluate(e=>e.scrollIntoView({block:'start',behavior:'instant'}));await p.waitForTimeout(900);await p.screenshot({path:'/home/user/qa/lowpoly-mobile.png'});
 assert.equal(await p.locator('.artwork').count(),3);assert.equal(await p.locator('.street-card').count(),3);
 const reduced=await b.newPage({reducedMotion:'reduce'});await reduced.goto('http://127.0.0.1:3000');assert.equal(await reduced.locator('#logo-replay').isDisabled(),true);
 const nojs=await b.newPage({javaScriptEnabled:false});await nojs.goto('http://127.0.0.1:3000');assert.equal(await nojs.locator('.lp-solid').isVisible(),true);assert.equal(await nojs.locator('.identity-controls').isVisible(),false);
 const offline=await b.newPage();await offline.goto('file:///home/user/Roman-Chashin.html');await offline.locator('[data-logo-mode="grid"]').click();assert.equal(await offline.locator('.lp-stage').getAttribute('data-mode'),'grid');
 assert.deepEqual(errors,[]);await b.close();console.log('PASS: exact source geometry/palette/order, 10 animated modules, 30 quads, animated wireframe, replay, global pause cancels motion, reduced-motion, no-JS, 4 breakpoints, exhibition preserved, offline interaction.');
})().catch(e=>{console.error(e);process.exit(1)});
