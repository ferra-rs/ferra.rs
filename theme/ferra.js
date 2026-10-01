(function () {
  var sb = document.querySelector('.sidebar');
  if (!sb) return;

  /* Back link to main site */
  var back = document.createElement('a');
  back.href = '/';
  back.className = 'ferra-back-link';
  back.innerHTML = '&#8592; ferra.rs';
  back.style.cssText = [
    'display:block',
    'padding:14px 20px 10px',
    'font:600 12px/1 var(--mono,monospace)',
    'letter-spacing:0.06em',
    'color:rgba(216,205,184,0.5)',
    'text-decoration:none',
    'border-bottom:1px solid rgba(255,255,255,0.08)',
    'margin-bottom:8px',
    'transition:color .15s',
  ].join(';');
  back.addEventListener('mouseenter', function () { back.style.color = '#f6c016'; });
  back.addEventListener('mouseleave', function () { back.style.color = 'rgba(216,205,184,0.5)'; });

  sb.insertBefore(back, sb.firstChild);
})();

(function () {
  /* Notice: this published guide describes Ferra 0.7. */
  var host = document.getElementById('mdbook-content') || document.querySelector('.content');
  if (!host) return;
  var note = document.createElement('div');
  note.className = 'ferra-outdated-note';
  note.setAttribute('role', 'note');
  note.textContent = 'This guide describes Ferra 0.7 and is out of date; the 0.9 guide is published with the release.';
  note.style.cssText = [
    'margin:0 0 20px',
    'padding:10px 14px',
    'border-left:3px solid #f6c016',
    'background:rgba(246,192,22,0.12)',
    'font:600 13px/1.5 var(--mono,monospace)',
  ].join(';');
  host.insertBefore(note, host.firstChild);
})();
