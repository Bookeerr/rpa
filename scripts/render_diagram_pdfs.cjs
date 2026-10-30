// Export vectorial al tamano natural del SVG, sin recortar diagramas verticales.
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer');
const fs=require('fs'),path=require('path');
const folder=path.resolve(__dirname,'../docs/diagramas');
(async()=>{const browser=await puppeteer.launch({headless:true});try{
 const page=await browser.newPage();
 for(const name of fs.readdirSync(folder).filter(n=>n.endsWith('.svg'))){
  let svg=fs.readFileSync(path.join(folder,name),'utf8');
  const bounds=svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
  const width=Math.ceil(bounds[2]),height=Math.ceil(bounds[3]);
  svg=svg.replace(/<svg\b[^>]*>/,root=>root.replace(/\s(?:width|height|style)="[^"]*"/g,'').replace(/>$/,` width="${width}" height="${height}" style="background:white;display:block">`));
  await page.setViewport({width,height});
  await page.setContent('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:white}</style></head><body>'+svg+'</body></html>');
  await page.evaluate(()=>document.fonts.ready);
  await page.pdf({path:path.join(folder,name.replace(/\.svg$/,'.pdf')),width:width+'px',height:height+'px',
                 printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});
  console.log('PDF vectorial:',name);
 }
}finally{await browser.close()}})().catch(e=>{console.error(e.message);process.exit(1)});
