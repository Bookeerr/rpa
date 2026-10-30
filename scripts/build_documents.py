"""Genera PDF de informe y PPT/PDF de exposicion desde contenido versionado."""
from pathlib import Path
from html import escape
import re
import pymupdf
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/entrega'
DIAGRAMS=ROOT/'docs/diagramas'
RELEASE_DATE='2026-10-20'


def image_fit(path,width,height):
    with PILImage.open(path) as im: w,h=im.size
    scale=min(width/w,height/h)
    return Image(str(path),width=w*scale,height=h*scale)


def report():
    styles=getSampleStyleSheet()
    styles['BodyText'].fontSize=10
    styles['BodyText'].leading=14
    story=[]
    text=(ROOT/'docs/INFORME_TECNICO_EP2.md').read_text(encoding='utf-8')
    for block in text.split('\n\n'):
        if not block.strip(): continue
        if block.startswith('# '): style=styles['Title']; block=block[2:]
        elif block.startswith('## '): style=styles['Heading2']; block=block[3:]
        else: style=styles['BodyText']
        story += [Paragraph(escape(block.replace('`','')).replace('\n','<br/>'),style),Spacer(1,6)]
    figures=[('00_flujo_resumen','Vista resumida para exposicion'),('01a_captura_validacion','Figura 1a. Captura y validacion'),('01b_integracion_cierre','Figura 1b. Integracion y cierre'),
                       ('02_arquitectura','Figura 2. Arquitectura y despliegue'),('03_modelo_datos','Figura 3. Modelo SQL real'),
                       ('04_secuencia_auditoria_http','Figura 4. Auditoria e integracion HTTP'),('05_mejora_proceso','Figura 5. Mejora del proceso'),
                       ('06_demo_nativa','Figura 6. Demo sintetica ejecutada en Rocketbot')]
    def footer(c,doc):
        c.setFont('Helvetica',8);c.setFillColor(HexColor('#475569'))
        c.drawString(45,25,'TestFire EP2 | EVIDENCIA Y ALCANCE DECLARADO | '+RELEASE_DATE)
        c.drawRightString(A4[0]-45,25,str(doc.page))
    body_path=OUT/'_informe_cuerpo_temporal.pdf'
    if story and isinstance(story[-1],Spacer):story.pop()
    SimpleDocTemplate(str(body_path),pagesize=A4,
        rightMargin=45,leftMargin=45,topMargin=40,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
    document=pymupdf.open(body_path)
    for name,title in figures:
        with pymupdf.open(DIAGRAMS/(name+'.pdf')) as source:
            original=source[0]
            spans=[span for block in original.get_text('dict')['blocks'] if 'lines' in block
                   for line in block['lines'] for span in line['spans'] if span['text'].strip()]
            # El export ya usa el viewBox natural. Conservar pagina completa:
            # algunas sombras/recuadros SVG aparecen como imagenes, no paths.
            bounds=original.rect
            scale=max(0.5,10/min(s['size'] for s in spans))
            width=max(A4[0],bounds.width*scale+80)
            height=max(A4[1],bounds.height*scale+145)
            page=document.new_page(width=width,height=height)
            page.insert_text((40,35),title,fontsize=16,fontname='hebo',color=(0.09,0.2,0.31))
            target=pymupdf.Rect(40,55,40+bounds.width*scale,55+bounds.height*scale)
            page.show_pdf_page(target,source,0,clip=bounds)
            caption=('Demo sintetica historica; la corrida web se documenta en el cuerpo del informe.' if name=='06_demo_nativa' else
                     'Esquema derivado del SQL entregado; despliegue pendiente.' if name=='03_modelo_datos' else
                     'Diseno del alcance ampliado: MySQL y segunda PC pendientes.')
            page.insert_text((40,height-62),caption,fontsize=10)
            page.insert_text((40,height-44),'Fuente editable: docs/diagramas/'+name+'.mmd',fontsize=10)
            page.insert_text((40,height-24),f'TestFire EP2 | EP2 | {RELEASE_DATE} | {len(document)}',fontsize=9)
    for filename,title,caption in [
        ('recorder_dom_tabla.png','Evidencia: captura del recorder DOM','Sesion real de captura del grabador propio EP2. Export de cuatro eventos en recorder/dom_recording.json; aceptacion de esta alternativa pendiente del docente.'),
        ('studio_web.png','Evidencia: ejecucion nativa en Studio','MAIN_TESTFIRE_EP2 con subrobots, controles e integraciones. UUID y respuestas originales en docs/evidencias/web_nativa_resumen.json y studio_web_responses.json.')]:
        path=ROOT/'docs/evidencias'/filename
        if path.exists():
            page=document.new_page(width=842,height=650)
            page.insert_text((35,35),title,fontsize=18,fontname='hebo')
            page.insert_textbox(pymupdf.Rect(35,50,807,100),caption,fontsize=11)
            page.insert_image(pymupdf.Rect(35,110,807,610),filename=str(path),keep_proportion=True)
            page.insert_text((35,630),'TestFire EP2 | Evidencia guardada | '+RELEASE_DATE,fontsize=9)
    document.save(OUT/'Informe_Tecnico_EP2.pdf',garbage=4,deflate=True)
    document.close();body_path.unlink()


import json
WEB=json.loads((ROOT/'docs/evidencias/web_nativa_resumen.json').read_text(encoding='utf8'))
SLIDES=[
 ('TestFire EP2','Consulta y conciliacion con Rocketbot', ['20 octubre 2026 | ATY1102','Login real, XPath, Excel externo y API persistente','Alcance comprobado y limites declarados'],None),
 ('Del problema al proceso','1 minuto', ['EP1: consulta automatizada y exportacion','EP2: controles visibles e integraciones','Fuente externa y acuse HTTP trazable'],'00_flujo_resumen'),
 ('Rocketbot y recorder','2 minutos', ['MAIN invoca WEB_LOGIN y EXTRACT_TRANSACTIONS','For de filas/pares, IF, While limitado y Try Catch','Grabador DOM propio: 4 eventos reales y replay','Aceptacion de la alternativa: pendiente docente'],None),
 ('DOM y validacion','2 minutos', ['XPath y cinco cabeceras verificadas en TestFire','Fecha real: YYYY-MM-DD HH:MM','Regex + strptime + Decimal; raw conservado','Vista: 100 recientes; no historial completo'],None),
 ('Excel externo y conciliacion','2 minutos', ['Maestro: snapshot previo, versionado y con hash','Cinco estados; duplicados conservados por ocurrencia','El sitio compartido cambia entre capturas','MySQL pendiente por indicacion del usuario'],None),
 ('HTTP con proposito','1 minuto', ['GET salud, POST resumen, GET confirmacion','200 / 201 / 200 repetido / 200 verificados','UUID estable: payload distinto produce 409','API compartida con SQLite; MySQL pendiente'],None),
 ('Segunda PC verificada','1 minuto', ['DESKTOP-OFQ9QLA: ejecucion real desde el cliente','96 validos / 4 rechazados / 103,525 segundos','Resumen en el host y GET HTTP 200 comprobados','Excel del cliente informado; no inspeccionado aqui'],None),
 ('Resultados del host','Corrida 18/10/2026 | 1 minuto', [f"{WEB['valid_rows']} validos / {WEB['rejected_rows']} rechazados / 5 hojas Excel",'58 pruebas Python aprobadas',f"Duracion registrada: {WEB['duration_ms']/1000:.3f} segundos",'PARCIAL global: SQL pendiente; flujo web completo'],None),
 ('Mejora y defensa','1 minuto', ['SCAMPER: combinar fuentes y eliminar recaptura','Sin porcentaje de ahorro: falta referencia manual','Pendientes: MySQL y aceptacion del recorder','Completar aporte personal y ensayar 11 minutos'],None),
]


def slides():
    prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
    pdf=canvas.Canvas(str(OUT/'Presentacion_EP2.pdf'),pagesize=(960,540))
    for index,(title,subtitle,bullets,diagram) in enumerate(SLIDES,1):
        slide=prs.slides.add_slide(prs.slide_layouts[6]);bg=slide.background.fill;bg.solid();bg.fore_color.rgb=RGBColor.from_string('F6F8FC')
        def box(txt,x,y,w,h,size=24,color='16324F',bold=False):
            shape=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
            tf=shape.text_frame;tf.word_wrap=True
            p=tf.paragraphs[0];p.text=txt;p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color)
            return shape
        box(title,0.6,0.45,12,0.7,32,bold=True);box(subtitle,0.65,1.2,12,0.5,16,color='52637A')
        pdf.setFillColor(HexColor('#F6F8FC'));pdf.rect(0,0,960,540,fill=1,stroke=0)
        pdf.setFillColor(HexColor('#16324F'));pdf.setFont('Helvetica-Bold',28);pdf.drawString(45,475,title)
        pdf.setFont('Helvetica',14);pdf.setFillColor(HexColor('#52637A'));pdf.drawString(47,440,subtitle)
        for i,bullet in enumerate(bullets):
            box(bullet,0.8,2.0+i*0.85,7 if diagram=='02_arquitectura' else 11.8,0.8,21)
            pdf.setFillColor(HexColor('#16324F'));pdf.setFont('Helvetica',17)
            pdf.drawString(58,375-i*58,bullet.replace('→',' / '))
        if diagram:
            img=DIAGRAMS/(diagram+'.png')
            with PILImage.open(img) as im: w,h=im.size
            if diagram=='00_flujo_resumen': x,y,aw,ah=0.8,4.5,11.8,2.2
            else:x,y,aw,ah=8.0,1.8,4.6,5.0
            scale=min(aw/w,ah/h);slide.shapes.add_picture(str(img),Inches(x),Inches(y),width=Inches(w*scale),height=Inches(h*scale))
            if diagram=='00_flujo_resumen': pdf.drawImage(str(img),58,65,width=840,height=145,preserveAspectRatio=True,anchor='c')
            # PDF de arquitectura separada evita texto sobrepuesto.
        box(f'{index:02}  |  EP2 | Evidencias verificadas y limites declarados | {RELEASE_DATE}',0.65,7.05,12,0.3,10,color='52637A')
        slide.notes_slide.notes_text_frame.text='Guion: docs/GUION_PRESENTACION.md. Tiempo previsto, no ensayo medido. '+ ' '.join(bullets)
        pdf.setFont('Helvetica',9);pdf.drawString(45,20,f'{index:02} | EP2 | Evidencia y limites | {RELEASE_DATE}');pdf.showPage()
    prs.save(OUT/'Presentacion_EP2.pptx');pdf.save()


def main():
    OUT.mkdir(parents=True,exist_ok=True);report();slides()
    print('Informe PDF y presentacion PPTX/PDF generados en docs/entrega')


if __name__=='__main__':main()
