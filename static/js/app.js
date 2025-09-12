(function(){
  const themeBtn = document.querySelector('[data-toggle="theme"]');
  const root = document.documentElement;
  function setTheme(t){root.setAttribute('data-theme', t);localStorage.setItem('theme',t);themeBtn && (themeBtn.textContent = t==='dark' ? '🌙' : '☀️');}
  setTheme(localStorage.getItem('theme') || 'light');
  themeBtn && themeBtn.addEventListener('click', ()=> setTheme(root.getAttribute('data-theme')==='dark'?'light':'dark'));
})();
