#!/usr/bin/env python3
"""Render the research note with searchable text and clickable references."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'output/pdf/delegation-blind-spot-research-note.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
ink = colors.HexColor('#172F38')
accent = colors.HexColor('#176C73')
styles = {
    'body': ParagraphStyle('body', fontName='Times-Roman', fontSize=11, leading=15.2,
                           textColor=ink, spaceAfter=10),
    'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=29, leading=32,
                         textColor=ink, spaceAfter=14),
    'h2': ParagraphStyle('h2', fontName='Helvetica', fontSize=17, leading=22,
                         textColor=accent, spaceAfter=14),
    'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=12.5, leading=17,
                         textColor=accent, spaceBefore=6, spaceAfter=8, keepWithNext=True),
    'code': ParagraphStyle('code', fontName='Courier', fontSize=9.2, leading=13,
                           textColor=ink, backColor=colors.HexColor('#EDF4F2'),
                           borderPadding=9, spaceBefore=7, spaceAfter=12),
    'caption': ParagraphStyle('caption', fontName='Helvetica', fontSize=8.4, leading=11.5,
                              textColor=colors.HexColor('#53646C'), spaceAfter=10),
}


def markup(text):
    text = escape(text)
    return re.sub(r'https://[^\s<]+', lambda m: '<link href="'+m[0]+'" color="#176C73">'+m[0]+'</link>', text)


def footer(canvas, doc):
    width, height = doc.pagesize
    canvas.saveState()
    canvas.setFillColor(accent)
    canvas.rect(48, height-34, 20, 3, fill=1, stroke=0)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(76, height-34, 'SHIVAM GUPTA / THE DELEGATION BLIND SPOT')
    canvas.setStrokeColor(colors.HexColor('#CAD9DA'))
    canvas.line(48, 42, width-48, 42)
    canvas.setFillColor(ink)
    canvas.drawString(48, 28, 'RESEARCH NOTE 0.1 | Exploratory, not peer reviewed')
    canvas.drawRightString(width-48, 28, str(doc.page))
    canvas.restoreState()


story = []
source = (ROOT/'paper/research-note.md').read_text()
for block in re.split(r'\n\s*\n', source.strip()):
    if block == '<!-- pagebreak -->':
        story.append(PageBreak())
    elif block.startswith('!['):
        relative = re.search(r'\]\((.+)\)', block).group(1)
        path = (ROOT/'paper'/relative).resolve()
        width,height = ImageReader(str(path)).getSize()
        story.append(Image(str(path), width=490, height=490*height/width))
        story.append(Spacer(1,6))
    elif block.startswith('    '):
        story.append(Paragraph('<br/>'.join(escape(x.strip()) for x in block.splitlines()), styles['code']))
    else:
        for prefix, style in [('### ', 'h3'), ('## ', 'h2'), ('# ', 'h1')]:
            if block.startswith(prefix):
                # The title and subtitle are on consecutive lines.
                for line in block.splitlines():
                    matched = next((p,s) for p,s in [('### ','h3'),('## ','h2'),('# ','h1')] if line.startswith(p))
                    story.append(Paragraph(markup(line[len(matched[0]):]), styles[matched[1]]))
                break
        else:
            style = 'caption' if block.startswith('Figure ') or block.startswith('Shivam Gupta |') else 'body'
            story.append(Paragraph(markup(' '.join(block.splitlines())), styles[style]))

doc = SimpleDocTemplate(str(OUT), pagesize=(612,792), leftMargin=54, rightMargin=54,
                        topMargin=54, bottomMargin=56, title='The Delegation Blind Spot',
                        author='Shivam Gupta', subject='Exploratory research note on delegated product learning')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
