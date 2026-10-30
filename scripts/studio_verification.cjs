// Verifica el resultado persistido, no solo la presencia de un comando final.
function verifyRun({responses,executionId,summary,robot}) {
  const marker=robot==='MAIN_TESTFIRE_EP2'?'WEB_ROCKETBOT_FIN':'DEMO_ROCKETBOT_FIN';
  if(!responses.length || responses.some(r=>r.status!==200 || String(r.body?.status).toLowerCase()!=='true'))
    throw Error('Uno o mas comandos nativos fallaron');
  if(!responses.some(r=>r.body?.message?.includes(marker)))throw Error('Tiempo agotado o ejecucion sin cierre');
  if(!executionId || summary?.execution_id!==executionId)throw Error('Resumen no corresponde a la ejecucion iniciada');
  if(!summary.ended_at || !['OK','PARCIAL'].includes(summary.status))throw Error('Ejecucion incompleta o con error');
  if(robot==='MAIN_TESTFIRE_EP2' && summary.web_excel_api_complete!==true)throw Error('Integraciones web/Excel/API incompletas');
  if(summary.http_ok!==true)throw Error('HTTP sin confirmacion');
  return {execution_id:executionId,status:summary.status,valid_rows:summary.valid_rows,rejected_rows:summary.rejected_rows};
}
module.exports={verifyRun};
