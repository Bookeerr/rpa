const puppeteer=require(process.env.PUPPETEER_MODULE);
const fs=require('fs');const path=require('path');
const {verifyRun}=require('./studio_verification.cjs');
const root=path.resolve(__dirname,'..');
const db=Buffer.from(path.join(root,'rocketbot/MAIN_TESTFIRE_EP2/robot.db')).toString('base64');
const robot=process.env.STUDIO_ROBOT||'MAIN_TESTFIRE_EP2';
const evidence=process.env.STUDIO_EVIDENCE||(robot==='MAIN_TESTFIRE_EP2'?'studio_web':'studio_demo');
if(!/^[a-zA-Z0-9_-]+$/.test(evidence))throw Error('Nombre de evidencia invalido');
(async()=>{
 const browser=await puppeteer.launch({headless:true});
 try{
  const page=await browser.newPage();await page.setViewport({width:1440,height:1000});
  const responses=[];
  let executionId;const pending=new Set(),secrets=new Set();
  const redact=v=>typeof v==='string'?[...secrets].reduce((s,key)=>s.split(key).join('[REDACTADO]'),v):Array.isArray(v)?v.map(redact):v&&typeof v==='object'?Object.fromEntries(Object.entries(v).map(([k,x])=>[k,redact(x)])):v;
  page.on('response',r=>{if(new URL(r.url()).pathname==='/execute'){
   const task=(async()=>{const body=await r.json();for(const v of body.vars||[]){
     if(v.name==='execution_id' && /^[0-9a-f-]{36}$/i.test(v.data))executionId=v.data;
     if(['usuario','clave'].includes(v.name)&&v.data)secrets.add(String(v.data));
   }delete body.vars;delete body.img;responses.push({url:r.url(),status:r.status(),body:redact(body)});if(responses.length%100===0)console.log('Comandos respondidos:',responses.length)})();
   pending.add(task);task.finally(()=>pending.delete(task)).catch(()=>{});
  }});
  await page.goto('http://localhost:5000/editor/#/edit/'+robot+'/db/'+db,{waitUntil:'networkidle2'});
  await page.waitForFunction(()=>[...document.querySelectorAll('button')].some(e=>['Run','Ejecutar'].includes(e.innerText.trim())&&!e.disabled),{timeout:45000});
  await page.evaluate(()=>{const e=[...document.querySelectorAll('button')].find(e=>['Run','Ejecutar'].includes(e.innerText.trim())&&!e.disabled);if(!e)throw Error('Run no encontrado');e.click()});
  const deadline=Date.now()+900000;
  while(Date.now()<deadline){
   const complete=robot==='MAIN_TESTFIRE_EP2'?responses.some(r=>r.body?.message?.includes('WEB_ROCKETBOT_FIN')):
      responses.some(r=>r.body?.message?.includes('DEMO_ROCKETBOT_FIN'));
   if(complete)break;
   await new Promise(r=>setTimeout(r,500));
  }
  await Promise.allSettled([...pending]);
  console.log('Respuestas:',responses.length,'Fallos:',responses.filter(r=>String(r.body?.status).toLowerCase()==='false').map(r=>r.body));
  fs.writeFileSync(path.join(root,'docs/evidencias/'+evidence+'_responses.json'),JSON.stringify(responses,null,2));
  await page.screenshot({path:path.join(root,'docs/evidencias/'+evidence+'.png'),fullPage:false});
  const summary=executionId?JSON.parse(fs.readFileSync(path.join(root,'output',executionId,'execution.json'),'utf8')):null;
  const result=verifyRun({responses,executionId,summary,robot});
  fs.writeFileSync(path.join(root,'docs/evidencias/'+evidence+'_verified.json'),JSON.stringify(result,null,2));
  console.log('Ejecucion verificada:',JSON.stringify(result));
 }finally{await browser.close()}
})().catch(e=>{console.error(e.message);process.exit(1)});
