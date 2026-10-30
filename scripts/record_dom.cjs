// Conduce una sesion de captura. El recorder escucha eventos del navegador;
// los comandos exportados se obtienen de esos eventos, no de esta secuencia.
const puppeteer=require(process.env.PUPPETEER_MODULE),fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const cfg=Object.fromEntries(fs.readFileSync(path.join(root,'.env'),'utf8').split(/\r?\n/).filter(x=>x&&!x.startsWith('#')).map(x=>{const i=x.indexOf('=');return [x.slice(0,i),x.slice(i+1)]}));
(async()=>{const b=await puppeteer.launch({headless:false,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',defaultViewport:{width:1200,height:850}});
 const events=[];try{
 const p=await b.newPage();await p.exposeFunction('ep2Record',event=>events.push({...event,at:new Date().toISOString()}));
 await p.evaluateOnNewDocument(fs.readFileSync(path.join(root,'recorder/dom_recorder.js'),'utf8'));
 await p.goto(cfg.TESTFIRE_URL+'login.jsp',{waitUntil:'networkidle2'});
 await p.type('#uid',cfg.TESTFIRE_USER);await p.type('#passw',cfg.TESTFIRE_PASSWORD);
 await Promise.all([p.waitForNavigation({waitUntil:'networkidle2'}),p.click('input[name=btnSubmit]')]);
 await Promise.all([p.waitForNavigation({waitUntil:'networkidle2'}),p.click('a[href="/bank/transaction.jsp"]')]);
 await p.waitForSelector('#_ctl0__ctl0_Content_Main_MyTransactions');
 await p.screenshot({path:path.join(root,'docs/evidencias/recorder_dom_tabla.png')});
 const evidence={recorder:'Grabador DOM propio EP2; no es Rocketbot Recorder oficial',started_at:events[0]?.at,ended_at:new Date().toISOString(),events};
 if(events.length!==4||events.some(e=>!e.trusted))throw Error('Captura inesperada: '+events.length);
 fs.writeFileSync(path.join(root,'recorder/dom_recording.json'),JSON.stringify(evidence,null,2));
 console.log('Eventos reales capturados:',events.length);
 }finally{await b.close()}
})().catch(e=>{console.error(e.message);process.exit(1)});
