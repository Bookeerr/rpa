/* Grabador DOM propio EP2. Captura eventos reales; no contiene credenciales.
   Se instala antes de navegar y requiere el enlace ep2Record de su lanzador. */
(() => {
  const xpath = e => e.id ? `//*[@id="${e.id}"]` : e.name ? `//${e.tagName.toLowerCase()}[@name="${e.name}"]` :
    e.tagName === 'A' ? `//a[@href="${e.getAttribute('href')}"]` : null;
  document.addEventListener('change', e => {
    if(!e.isTrusted || !['uid','passw'].includes(e.target.name))return;
    window.ep2Record({action:'input',selector:xpath(e.target),variable:e.target.name==='uid'?'usuario':'clave',trusted:e.isTrusted,url:location.origin+location.pathname});
  },true);
  document.addEventListener('click', e => {
    if(!e.isTrusted)return;
    const t=e.target.closest('a,input[type=submit],button');if(!t||!xpath(t))return;
    window.ep2Record({action:'click',selector:xpath(t),trusted:e.isTrusted,url:location.origin+location.pathname});
  },true);
})();
