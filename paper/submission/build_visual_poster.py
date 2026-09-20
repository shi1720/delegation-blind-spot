#!/usr/bin/env python3
"""Build an anonymous vector A0 research poster from recorded study results."""
from pathlib import Path
import csv
import math
import tempfile
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A0
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/pdf/chi-visual-poster.pdf'
FONT=Path('/System/Library/Fonts/Supplemental')
if (FONT/'Arial.ttf').exists():
    pdfmetrics.registerFont(TTFont('Body',str(FONT/'Arial.ttf')))
    pdfmetrics.registerFont(TTFont('Strong',str(FONT/'Arial Bold.ttf')))
else:
    import matplotlib
    FONT=Path(matplotlib.get_data_path())/'fonts/ttf'
    pdfmetrics.registerFont(TTFont('Body',str(FONT/'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('Strong',str(FONT/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Strong',italic='Body',boldItalic='Strong')
W,H=A0
M=104; CW=W-2*M
NAVY=HexColor('#102D3A'); INK=HexColor('#17343F'); MUTED=HexColor('#49636C')
TEAL=HexColor('#087F83'); GOLD=HexColor('#C98421'); ORANGE=HexColor('#B85F38')
PAPER=HexColor('#F7F8F5'); LINE=HexColor('#CFDCD9'); LIGHT=HexColor('#E6F2EF')
BLUE=HexColor('#EAF0F6'); WARM=HexColor('#F8EFE0')


def build():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    fd=tempfile.NamedTemporaryFile(suffix='.pdf',delete=False); raw=Path(fd.name); fd.close()
    c=canvas.Canvas(str(raw),pagesize=A0,pageCompression=1)
    def rect(x,t,w,h,fill,stroke=None,r=0):
        c.setFillColor(fill)
        c.setStrokeColor(stroke or fill)
        if r:c.roundRect(x,H-t-h,w,h,r,fill=1,stroke=bool(stroke))
        else:c.rect(x,H-t-h,w,h,fill=1,stroke=bool(stroke))
    def line(x1,t1,x2,t2,col=LINE,width=2):
        c.setStrokeColor(col);c.setLineWidth(width);c.line(x1,H-t1,x2,H-t2)
    def text(s,x,t,size=32,color=INK,bold=False):
        c.setFillColor(color);c.setFont('Strong' if bold else 'Body',size)
        c.drawString(x,H-t-size*.82,s)
    def para(s,x,t,w,size=32,color=INK,bold=False,leading=None,maxheight=None):
        p=Paragraph(s,ParagraphStyle('p',fontName='Strong' if bold else 'Body',fontSize=size,
                    leading=leading or size*1.29,textColor=color,spaceAfter=0))
        _,h=p.wrap(w,H)
        if maxheight is not None and h>maxheight+0.1:raise ValueError(f'Overflow {h}>{maxheight}: {s[:90]}')
        p.drawOn(c,x,H-t-h)
        return h
    def tag(s,x,t,col=TEAL):text(s,x,t,25,col,True)
    def arrow(x,t,length=65):
        line(x,t,x+length,t,TEAL,5)
        line(x+length-16,t-13,x+length,t,TEAL,5);line(x+length-16,t+13,x+length,t,TEAL,5)
    rect(0,0,W,H,PAPER)
    rect(0,0,W,605,NAVY)
    tag('AGENT-MEDIATED INTERFACES  /  COMPUTATIONAL RESEARCH',M,78,HexColor('#8BCECA'))
    text('The Delegation',M,146,118,white,True)
    text('Blind Spot',M,277,118,white,True)
    para('Successful execution is not the same as evidence<br/>for the next product decision.',M,440,CW-100,46,white,leading=57,maxheight=130)
    # Restrained top-right motif: identical observed actions, distinct latent priorities.
    sx=W-610
    for top,label in [(162,'QUIET'),(262,'LOCATION')]:
        rect(sx,top,210,65,HexColor('#264550'),r=12)
        text(label,sx+23,top+19,28,white,True)
        line(sx+225,top+32,sx+305,244,HexColor('#8BCECA'),3)
    rect(sx+310,210,190,69,HexColor('#8BCECA'),r=12)
    text('SAME HOTEL',sx+327,234,23,NAVY,True)

    tag('01  THE AUDIT',M,658)
    text('Does this log support this future decision?',M,703,50,INK,True)
    gap=86; boxw=(CW-2*gap)/3; boxTop=791; boxh=254
    stages=[('OBSERVE','An agent chooses.', 'A logged action can fit several<br/>different customer priorities.',BLUE),
            ('AUDIT','Keep alternatives visible.', 'Combine a calibrated channel,<br/>a value contrast and uncertainty.',LIGHT),
            ('DECIDE','Resolve or abstain.', 'Recommend only when every<br/>compatible mixture agrees.',WARM)]
    for i,(label,head,body,bg) in enumerate(stages):
        x=M+i*(boxw+gap)
        rect(x,boxTop,boxw,boxh,bg,r=18)
        tag(label,x+31,boxTop+27)
        text(head,x+31,boxTop+83,34,INK,True)
        para(body,x+31,boxTop+143,boxw-60,30,maxheight=95)
        if i<2:arrow(x+boxw+12,boxTop+126,60)
    para('Example: two optimal hotel bookings can look identical. They need not support the same investment in soundproofing or transport links.',M,1080,CW,31,MUTED,maxheight=83)

    tag('02  THREE DISTINCT PIECES OF EVIDENCE',M,1190)
    gap=30; rw=(CW-2*gap)/3; rt=1250; rh=631
    cards=[
       ('PRIMARY / PROSPECTIVELY FROZEN','0 / 36','comparisons resolved',
        '4,800 API requests',
        'GPT-5.4 Mini and Nano on shared synthetic tasks. They choose a utility maximizer in 73.19% and 55.69% of field tasks, respectively.',
        'Conservative intervals remain unresolved. This does not prove structural information loss.',BLUE,TEAL),
       ('FOLLOW-UP / EXPLORATORY','3 / 9','resolved per model',
        '2,400 additional calls',
        'Report the largest supplied preference weight. Each model repeats only 12 distinct prompts. Every report is correct.',
        'Matched observation counts, not matched costs. Known input extraction, not human preference discovery.',LIGHT,TEAL),
       ('PARSER / EXPLORATORY REANALYSIS','7 / 9','comparisons resolved',
        '720 shared field records',
        'Read the supplied weights directly. A known identity channel removes report-calibration uncertainty. No new API calls.',
        'Zero incorrect resolutions in this sample. The profile is synthetic, not validated against a customer.',WARM,ORANGE)]
    for i,(label,stat,desc,count,body,caution,bg,col) in enumerate(cards):
        x=M+i*(rw+gap)
        rect(x,rt,rw,rh,white,LINE,r=18)
        rect(x,rt,rw,12,col,r=4)
        tag(label,x+30,rt+36,col)
        text(stat,x+30,rt+93,100,col,True)
        text(desc,x+30,rt+213,34,INK,True)
        text(count,x+30,rt+280,31,INK,True)
        para(body,x+30,rt+335,rw-60,30,maxheight=170)
        rect(x+20,rt+510,rw-40,111,bg,r=12)
        para(caution,x+36,rt+526,rw-72,24,INK,maxheight=94)
    para('Coverage is marginal, not across all decisions: primary and model-report intervals use 96%; the parser uses a known channel and 96% field intervals. Follow-ups are not corrected for selection after the primary results.',M,1913,CW,28,MUTED,maxheight=85)

    top=2050; gap=42; half=(CW-gap)/2; height=741
    rect(M,top,half,height,white,LINE,r=18)
    rect(M+half+gap,top,half,height,white,LINE,r=18)
    lx=M+34; rx=M+half+gap+34
    tag('03  WHAT THE MATHEMATICS SAYS',lx,top+30)
    text('A contrast, not a full profile.',lx,top+79,41,INK,True)
    para('p = proportions of declared intent classes<br/>A = calibrated class-to-log channel<br/>q = observed log distribution<br/>d = independently specified product-value contrast',lx,top+153,half-68,30,leading=44,maxheight=180)
    rect(lx,top+360,half-68,90,LIGHT,r=12)
    text('q = Ap',lx+25,top+383,42,TEAL,True)
    text('Target: d\u1d40p',lx+340,top+383,42,TEAL,True)
    para('<b>Global identification:</b> for known A, the contrast is identified from every feasible q exactly when d lies in the row space of A.',lx,top+482,half-68,31,maxheight=132)
    para('With uncertain A and q, a joint-mass linear program returns attainable bounds and endpoint witness mixtures. A range crossing zero supports abstention.',lx,top+624,half-68,28,MUTED,maxheight=96)

    tag('04  STRUCTURAL LOSS ≠ FINITE PRECISION',rx,top+30)
    text('Identified can still mean imprecise.',rx,top+79,39,INK,True)
    para('Controlled channel: A(η) = (1 − η)11\u1d40/4 + ηI<br/>Exact width is zero whenever η &gt; 0.',rx,top+147,half-68,29,maxheight=87)
    # Vector scientific plot. Categorical x positions are explicitly labelled.
    rows=list(csv.DictReader((ROOT/'results/precision-sweep-v3/summary.csv').open()))
    vals=[r for r in rows if r['cohort']=='positive' and r['method']=='joint' and int(r['calibration_per_class'])==2560]
    vals.sort(key=lambda r:float(r['eta']))
    px=rx+100; py=top+302; pw=half-190; ph=247
    for value in [0,.05,.1]:
        yy=py+ph-ph*value/.1
        line(px,yy,px+pw,yy,LINE,1.5)
        text(f'{value:.2f}',rx+8,yy-12,25,MUTED)
    positions=[px+i*pw/5 for i in range(6)]
    finite=[float(r['width_median']) for r in vals]
    exact=[float(r['structural_width']) for r in vals]
    def plot(series,col,shape):
        for i in range(5):line(positions[i],py+ph-series[i]/.1*ph,positions[i+1],py+ph-series[i+1]/.1*ph,col,4)
        for xx,v in zip(positions,series):
            yy=H-(py+ph-v/.1*ph);c.setFillColor(col)
            if shape=='circle':c.circle(xx,yy,7,stroke=0,fill=1)
            else:c.rect(xx-7,yy-7,14,14,stroke=0,fill=1)
    plot(finite,TEAL,'circle');plot(exact,ORANGE,'square')
    for xx,r in zip(positions,vals):text(r['eta'],xx-16,py+ph+17,25,MUTED)
    text('Channel strength η (categorical spacing)',px,py+ph+58,25,MUTED)
    line(rx+3,top+265,rx+39,top+265,TEAL,4);text('Finite-sample median width',rx+52,top+251,25,INK)
    line(rx+505,top+265,rx+541,top+265,ORANGE,4);text('Exact width',rx+554,top+251,25,INK)
    para('Joint intervals; positive mixture; d = (.06, .02, -.04, -.02). 2,560 calibration samples per class; 5,120 field samples. 200 repetitions per point; widths condition on feasibility.',rx,top+635,half-68,24,MUTED,maxheight=100)

    y=2850
    tag('05  THE INTERFACE QUESTION',M,y)
    text('Keep the source of a claim visible.',M,y+48,46,INK,True)
    tags=[('OBSERVED','Booking'),('SUPPLIED','Quiet-room constraint'),('INFERRED','Boutique preference'),('OUTCOME','Not yet measured')]
    wg=(CW-3*26)/4
    for i,(a,b) in enumerate(tags):
        x=M+i*(wg+26)
        rect(x,y+122,wg,113,NAVY,r=13)
        tag(a,x+22,y+141,HexColor('#8BCECA'))
        text(b,x+22,y+186,27,white,True)
    para('<b>Discuss:</b> Which fields justify their privacy and elicitation cost? When should teams collect a direct outcome instead? Do witness mixtures help analysts interpret uncertainty?',M,y+269,CW,31,INK,maxheight=85)
    line(M,3255,W-M,3255,LINE,2)
    para('<b>Scope:</b> one synthetic task family, two related model snapshots, zero human participants. Controlled sweep: 14,400 multinomial datasets, not additional model calls. No measured customer or commercial outcomes.',M,3280,CW,25,MUTED,maxheight=72)
    c.showPage();c.save()
    reader=PdfReader(str(raw));writer=PdfWriter();writer.append_pages_from_reader(reader)
    writer.metadata=None
    if '/Metadata' in writer._root_object:del writer._root_object['/Metadata']
    with OUT.open('wb') as f:writer.write(f)
    raw.unlink()
    print(OUT)

if __name__=='__main__':build()
