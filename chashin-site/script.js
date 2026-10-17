'use strict';
const artworks = [
  { src: 'assets/roots.webp', original: 'assets/roots-original.jpg', title: 'След I. Исток и Ремесло', alt: 'Низкополигональные руки мастера с глиняным сосудом и вышитой лентой' },
  { src: 'assets/synthesis.webp', original: 'assets/synthesis-original.jpg', title: 'След II. Момент передачи и Синтез', alt: 'Передача глиняного артефакта, превращающегося в светящуюся полигональную сетку' },
  { src: 'assets/future.webp', original: 'assets/future-original.jpg', title: 'След III. Капсула в будущее', alt: 'Молодая фигура со светящейся капсулой культурной памяти' }
];
const dialog = document.querySelector('#art-dialog');
let selected = 0;
let trigger;
function showArt(index) {
  selected = (index + artworks.length) % artworks.length;
  const artwork = artworks[selected];
  const image = document.querySelector('#dialog-image');
  image.src = artwork.src;
  image.alt = artwork.alt;
  document.querySelector('#dialog-title').textContent = artwork.title;
  document.querySelector('#dialog-count').textContent = `0${selected + 1} / 03`;
  document.querySelector('#original-link').href = artwork.original;
}
document.querySelectorAll('[data-art]').forEach(link => {
  link.addEventListener('click', event => {
    if (!dialog.showModal || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    trigger = link;
    showArt(Number(link.dataset.art));
    dialog.showModal();
    document.body.classList.add('modal-open');
  });
});
document.querySelector('#dialog-close').addEventListener('click', () => dialog.close());
document.querySelector('#art-prev').addEventListener('click', () => showArt(selected - 1));
document.querySelector('#art-next').addEventListener('click', () => showArt(selected + 1));
dialog.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  if (trigger) trigger.focus({ preventScroll: true });
});
dialog.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft') { event.preventDefault(); showArt(selected - 1); }
  if (event.key === 'ArrowRight') { event.preventDefault(); showArt(selected + 1); }
});
let touchStart = 0;
const dialogImage = document.querySelector('#dialog-image');
dialogImage.addEventListener('touchstart', event => { touchStart = event.changedTouches[0].screenX; }, { passive: true });
dialogImage.addEventListener('touchend', event => {
  const delta = event.changedTouches[0].screenX - touchStart;
  if (Math.abs(delta) > 55) showArt(selected + (delta < 0 ? 1 : -1));
}, { passive: true });
let shareTimer;
document.querySelector('#share-button').addEventListener('click', async () => {
  const canonical = document.querySelector('link[rel="canonical"]');
  const url = canonical ? canonical.href : location.href.split('#')[0];
  const status = document.querySelector('#share-status');
  try {
    if (!navigator.clipboard) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText(url);
    status.textContent = 'Ссылка скопирована';
  } catch {
    status.textContent = 'Скопируйте адрес из строки браузера';
  }
  clearTimeout(shareTimer);
  shareTimer = setTimeout(() => { status.textContent = ''; }, 4000);
});

// Progressive motion: content stays readable with JavaScript disabled.
(() => {
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const toggle = document.querySelector('#motion-toggle');
  let preference = null;
  try { preference = localStorage.getItem('chashin-motion'); } catch {}
  let enabled = !media.matches && preference !== 'off';
  const animations = new Set();
  function applyMotion() {
    if (media.matches) enabled = false;
    toggle.disabled = media.matches;
    toggle.title = media.matches ? 'Уменьшение движения включено в настройках устройства' : 'Включить или выключить декоративные анимации';
    document.body.classList.toggle('motion-on', enabled);
    document.dispatchEvent(new CustomEvent('chashin:motion', { detail: { enabled } }));
    toggle.hidden = false;
    toggle.setAttribute('aria-pressed', String(enabled));
    toggle.setAttribute('aria-label', enabled ? 'Выключить анимацию' : 'Включить анимацию');
    toggle.querySelector('.motion-icon').textContent = enabled ? 'Ⅱ' : '▷';
    toggle.querySelector('.motion-label').textContent = enabled ? 'Анимация вкл.' : 'Анимация выкл.';
    if (!enabled) {
      animations.forEach(animation => animation.cancel());
      animations.clear();
      document.querySelectorAll('.artwork-image').forEach(card => {
        card.style.removeProperty('--tilt-x'); card.style.removeProperty('--tilt-y');
      });
    }
  }
  toggle.addEventListener('click', () => {
    enabled = !enabled;
    preference = enabled ? 'on' : 'off';
    try { localStorage.setItem('chashin-motion', enabled ? 'on' : 'off'); } catch {}
    applyMotion();
  });
  media.addEventListener('change', event => { enabled = !event.matches && preference !== 'off'; applyMotion(); });
  applyMotion();
  function reveal(element, delay = 0) {
    if (!enabled || !element.animate || media.matches) return;
    const animation = element.animate([
      { opacity: 0, transform: 'translate3d(0, 22px, 0)' },
      { opacity: 1, transform: 'translate3d(0, 0, 0)' }
    ], { duration: 760, delay, easing: 'cubic-bezier(.16,1,.3,1)', fill: 'backwards' });
    animations.add(animation);
    animation.finished.then(() => animations.delete(animation)).catch(() => {});
  }
  document.querySelectorAll('.title-line').forEach((line, i) => reveal(line, 70 + i * 95));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const siblings = Array.from(entry.target.parentElement.children);
        const stagger = entry.target.matches('.artwork,.street-card,.social-card,.code-grid article') ? Math.min(siblings.indexOf(entry.target), 3) * 65 : 0;
        reveal(entry.target, stagger);
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.series-intro,.artwork,.concept-content,.street-heading,.street-card,.style-heading,.code-grid article,.statement>p,.author-layout,.contact-heading,.social-card,.identity-heading,.identity-workbench,.identity-meaning-grid>article,.identity-applications').forEach(element => observer.observe(element));
  }
  document.querySelectorAll('.artwork-image').forEach(card => {
    let frame = 0;
    card.addEventListener('pointermove', event => {
      if (!enabled || media.matches || !finePointer.matches) return;
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        card.style.setProperty('--tilt-x', `${-y * 3}deg`);
        card.style.setProperty('--tilt-y', `${x * 3}deg`);
      });
    });
    card.addEventListener('pointerleave', () => {
      cancelAnimationFrame(frame);
      card.style.setProperty('--tilt-x', '0deg');
      card.style.setProperty('--tilt-y', '0deg');
    });
  });
  const progress = document.querySelector('.scroll-progress');
  let scrollFrame = 0;
  function updateProgress() {
    const range = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${range > 0 ? Math.max(0, Math.min(1, scrollY / range)) : 0})`;
    scrollFrame = 0;
  }
  addEventListener('scroll', () => { if (!scrollFrame) scrollFrame = requestAnimationFrame(updateProgress); }, { passive: true });
  addEventListener('resize', updateProgress, { passive: true });
  updateProgress();
})();


// An actual vector breakdown: adapted from the supplied modular-geometry HTML.
// Geometry is pre-rendered in the document: animation is progressive enhancement.
(() => {
  const stage = document.querySelector('.lp-stage');
  const controls = document.querySelector('.identity-controls');
  const replay = document.querySelector('#logo-replay');
  const hero = document.querySelector('.ch-live-logo');
  if (!stage || !controls || !replay) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const active = new Map();
  let entered = false;
  const enabled = () => document.body.classList.contains('motion-on') && !reduced.matches;
  const caption = document.querySelector('#identity-mode-caption');
  const captions = {
    mark: '10 модулей собираются в единый силуэт.',
    grid: 'Каркас: 30 четырёхугольников на изометрической сетке.'
  };
  controls.hidden = false;
  replay.hidden = false;
  function cancel(root) {
    (active.get(root) || []).forEach(animation => animation.cancel());
    active.delete(root);
  }
  function animateModules(root) {
    if (!root) return;
    cancel(root);
    if (!enabled() || !root.animate) return;
    const animations = [];
    root.querySelectorAll('.ch-vox').forEach((block, i) => {
      // Same falling-block assembly, stagger and easing as the reference.
      const animation = block.animate([
        { opacity: 0, transform: 'translateY(-26px)' },
        { opacity: 1, transform: 'translateY(0)' }
      ], { duration: 720, delay: i * 70, easing: 'cubic-bezier(.2,.8,.25,1)', fill: 'backwards' });
      animations.push(animation);
    });
    active.set(root, animations);
  }
  function animateDraft() {
    cancel(stage);
    if (!enabled() || !stage.animate) return;
    const animations = [];
    stage.querySelectorAll('.ch-wire-line').forEach((line, i) => {
      const length = Number(line.dataset.length);
      const isGrid = line.classList.contains('ch-grid-line');
      const delay = isGrid ? i * 22 : 200 + ((i - 14) % 12) * 42;
      const animation = line.animate([
        { strokeDasharray: `${length}`, strokeDashoffset: `${length}` },
        { strokeDasharray: `${length}`, strokeDashoffset: '0' }
      ], { duration: isGrid ? 950 : 900, delay, easing: 'cubic-bezier(.35,0,.15,1)', fill: 'backwards' });
      animations.push(animation);
    });
    active.set(stage, animations);
  }
  function play() {
    cancel(stage);
    cancel(stage.querySelector('.lp-solid'));
    if (stage.dataset.mode === 'grid') animateDraft();
    else animateModules(stage.querySelector('.lp-solid'));
  }
  function setMode(mode) {
    stage.dataset.mode = mode;
    controls.querySelectorAll('button').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.logoMode === mode));
    });
    stage.querySelector('.lp-solid').setAttribute('aria-hidden', String(mode !== 'mark'));
    stage.querySelector('.lp-draft').setAttribute('aria-hidden', String(mode !== 'grid'));
    caption.textContent = captions[mode];
    play();
  }
  controls.querySelectorAll('[data-logo-mode]').forEach(button => {
    button.addEventListener('click', () => setMode(button.dataset.logoMode));
  });
  replay.addEventListener('click', play);
  function syncMotion() {
    replay.disabled = !enabled();
    replay.title = enabled() ? 'Повторить анимацию текущего режима' : 'Анимация выключена настройкой страницы или устройства';
    if (!enabled()) [...active.keys()].forEach(cancel);
  }
  document.addEventListener('chashin:motion', syncMotion);
  reduced.addEventListener('change', syncMotion);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) [...active.keys()].forEach(cancel);
  });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting || entered) return;
        entered = true;
        play();
        observer.disconnect();
      });
    }, { threshold: .3 });
    observer.observe(stage);
  }
  syncMotion();
  animateModules(hero);
  if (hero) {
    let last = 0;
    hero.parentElement.addEventListener('pointerenter', () => {
      if (!matchMedia('(hover: hover) and (pointer: fine)').matches || performance.now() - last < 1600) return;
      last = performance.now();
      animateModules(hero);
    });
  }
})();
