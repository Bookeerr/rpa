const {test}=require('node:test'),assert=require('node:assert/strict');
const {verifyRun}=require('../scripts/studio_verification.cjs');
const executionId='a7989182-00cc-450e-93d0-e7fd55f9a212';
function run(){return {executionId,robot:'MAIN_TESTFIRE_EP2',responses:[{status:200,body:{status:'True',message:'WEB_ROCKETBOT_FIN'}}],summary:{execution_id:executionId,ended_at:'2026-10-18T12:00:00Z',status:'PARCIAL',http_ok:true,web_excel_api_complete:true}}}
test('acepta cierre confirmado de la misma corrida',()=>assert.equal(verifyRun(run()).execution_id,executionId));
test('rechaza marcador final cuyo comando fallo',()=>{const r=run();r.responses[0].body.status='False';assert.throws(()=>verifyRun(r),/fallaron/)});
test('rechaza timeout sin cierre',()=>{const r=run();r.responses[0].body.message='paso intermedio';assert.throws(()=>verifyRun(r),/sin cierre/)});
test('rechaza resumen de una corrida anterior',()=>{const r=run();r.summary.execution_id='otra';assert.throws(()=>verifyRun(r),/no corresponde/)});
test('rechaza integraciones incompletas aunque el comando final exista',()=>{const r=run();r.summary.web_excel_api_complete=false;assert.throws(()=>verifyRun(r),/incompletas/)});
test('rechaza ejecucion abierta y HTTP sin confirmacion',()=>{const r=run();r.summary.ended_at=null;assert.throws(()=>verifyRun(r),/incompleta/);r.summary.ended_at='fecha';r.summary.http_ok=false;assert.throws(()=>verifyRun(r),/confirmacion/)});
