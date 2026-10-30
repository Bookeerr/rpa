// Obtiene plantillas mediante formularios reales de Studio 2025.07.01.
// El JSON resultante es evidencia de formato, NO un export importable.
const puppeteer=require(process.env.PUPPETEER_MODULE),fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const db=Buffer.from(path.join(root,'rocketbot/MAIN_TESTFIRE_EP2/robot.db')).toString('base64');
(async()=>{const browser=await puppeteer.launch({headless:true});try{
 const page=await browser.newPage();
 await page.goto('http://localhost:5000/editor/#/edit/MAIN_TESTFIRE_EP2/db/'+db,{waitUntil:'networkidle2'});
 await page.waitForFunction(()=>window.$nuxt?.$store?.state?.allCommands);
 await new Promise(r=>setTimeout(r,3000));
 const templates={};
 for(const father of ['for','evaluateIf','trycatch','execRocketBotDB','openbrowser','waitforobject','evaluatewhile','gettable_extend','sendkey_web','click_web','killdriver','getscreenshot']){
  await page.evaluate(father=>{
   function find(c){if(c.$data.CURRENT_BOT!==undefined)return c;for(const ch of c.$children){const r=find(ch);if(r)return r}}
   const e=find(window.$nuxt);e.createCommandModal(Object.values(e.$store.state.allCommands).find(c=>c.father===father&&c.visible));
  },father);
  await new Promise(r=>setTimeout(r,400));
  console.log('Captura formulario',father);
  templates[father]=await page.evaluate(()=>{
   function find(c,p){if(p(c))return c;for(const ch of c.$children){const r=find(ch,p);if(r)return r}}
   const e=find(window.$nuxt,c=>c.$data.CURRENT_BOT!==undefined);
   const modal=find(e.$refs.editCreateModalRef,c=>typeof c.ok==='function');
   const command=e.generateCommandObjectToCreateOrEditIt(modal.ok());
   return command;
  });
  await page.evaluate(()=>window.$nuxt.$bvModal.hide('editCreateModal'));
 }
 fs.writeFileSync(path.join(root,'docs/evidencias/studio_command_templates.json'),JSON.stringify(templates,null,2));
 console.log('Plantillas guardadas:',Object.keys(templates).join(', '));
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
