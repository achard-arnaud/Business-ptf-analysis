#!/usr/bin/env python3
"""Chromium-free PDF fallback, same v0.3 executive content and color tokens.
Usage: python render_fallback.py payload.json output.pdf
No research, scoring or business logic. Raises on overflow.
"""
import json, sys, html, re
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

font='/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf';bold='/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf'
if not Path(font).exists():
 font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('CX',font));pdfmetrics.registerFont(TTFont('CXB',bold));pdfmetrics.registerFontFamily('CX',normal='CX',bold='CXB')
P=json.load(open(sys.argv[1]));out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True)
W,H=landscape(A4); navy=HexColor('#13213A');teal=HexColor('#0C7185');blue=HexColor('#1F4E8C');muted=HexColor('#5B6B82');border=HexColor('#CBD6E4');gold=HexColor('#C98A00')
c=canvas.Canvas(str(out),pagesize=(W,H)); fig={k:v['value'] for k,v in P['figures'].items()}
def text(s):
 s=re.sub(r'\{([a-z0-9_]+)\}',lambda m:fig[m[1]],str(s));return html.escape(s).replace('**','<b>',1).replace('**','</b>',1)
def para(s,x,top,w,size=10,color=navy,bold=False,leading=None):
 sty=ParagraphStyle('x',fontName='CXB' if bold else 'CX',fontSize=size,leading=leading or size*1.17,textColor=color,spaceAfter=0)
 q=Paragraph(text(s),sty); _,h=q.wrap(w,1000);q.drawOn(c,x,top-h);return h
def rect(x,y,w,h,fill=None,stroke=border,r=8):
 c.setStrokeColor(stroke);c.setFillColor(fill or HexColor('#FFFFFF'));c.roundRect(x,y,w,h,r,fill=1,stroke=1)
def card(x,y,w,h,title,lines,take=None,dark=False,fs=10):
 rect(x,y,w,h,navy if dark else None,navy if dark else border)
 ink=HexColor('#FFFFFF') if dark else navy; top=y+h-12
 th=para(title.upper(),x+12,top,w-24,11,HexColor('#8AE0EA') if dark else teal,True);top-=th+8
 available=top-(y+12)-(30 if take else 0)
 for line in lines:
  hh=para(line,x+12,top,w-24,fs,ink);top-=hh+5
 if top < y+12+(30 if take else 0):raise RuntimeError(f'overflow card {title}: {top-(y+12)}')
 if take:
  c.setStrokeColor(teal);c.line(x+12,y+35,x+w-12,y+35)
  hh=para('À RETENIR  '+take,x+12,y+31,w-24,9.2,ink)
  if hh>27:raise RuntimeError(f'overflow take {title}: {hh}')
def header(n,subtitle):
 c.setFillColor(navy);c.rect(0,H-70,W,70,fill=1,stroke=0)
 para(P["program"].upper(),28,H-10,500,10,HexColor('#8AE0EA'),True)
 para(P["entity"],28,H-28,275,20,HexColor('#FFFFFF'),True)
 para(subtitle,310,H-32,W-365,11,HexColor('#FFFFFF'))
 para(f'{n} / 3',W-55,H-12,35,9,HexColor('#8AE0EA'),True)
def footer(n,body,sources):
 rect(28,18,W-56,25,teal,teal,6)
 para(body,37,39,W-74,9.3,HexColor('#FFFFFF'))
 para(sources,28,14,W-68,7.5,muted)
 para(f'{n}/3',W-48,14,25,8,muted)
# PAGE 1
header(1,'Profil et décisions de valeur — lecture prudente des finances')
y=295;h=224;gap=9;w=(W-56-2*gap)/3
sig=[f'{a} : {b}' for a,b in P['page1']['signaletique']['rows']]
card(28,y,w,h,'Signalétique',sig,'2024 et 2025 sont deux exercices distincts.',fs=8.4)
card(28+w+gap,y,w,h,'Thèse',[P['page1']['thesis']['paras'][0],P['page1']['thesis']['paras'][1]],P['page1']['thesis']['take'],True,10.5)
card(28+2*(w+gap),y,w,h,'Drivers de valeur',[f'{i}. {d["label"]} — {d["text"]}' for i,d in enumerate(P['drivers'],1)],'Priorité économique à mesurer.',fs=9.3)
y=65;h=220
card(28,y,w,h,'Mix produit 2024',[f'{a} : {v} %' for a,v in P['page1']['breakdown']['series']]+['Canaux : ventilation non comparable au mix produit.'],'Mix produit et canaux sont deux découpages distincts.',fs=9.7)
card(28+w+gap,y,w,h,'Direction & données',[f'{r["who"]} — {r["what"]}' for r in P['page1']['board']['rows']],'Mandats COO/DSI et équipe IA à confirmer.',fs=9.2)
s=P['page1']['swot'];card(28+2*(w+gap),y,w,h,'SWOT → décision',['Forces : '+', '.join(s['s'][:2]),'Faiblesses : '+', '.join(s['w'][:2]),'Opportunités : '+', '.join(s['o'][:2]),'Menaces : '+', '.join(s['t'][:2])],'W-O provisoire : intégration et pouvoir de prix à mesurer.',fs=8.8)
footer(1,P['page1']['footer']['body'],P['page1']['sources']);c.showPage()
# PAGE 2
header(2,'Chaîne de valeur — enjeux par maillon, effets non quantifiés')
y=337;h=182;gap=7;w=(W-56-3*gap)/4
for i,a in enumerate(P['page2']['support']):
 card(28+i*(w+gap),y,w,h,a['name'],[a['desc'],'Bénéfice recherché : '+a['benefit']],None,fs=9.4)
y=130;h=197;w=(W-56-4*gap)/5
for i,a in enumerate(P['page2']['primary']):
 card(28+i*(w+gap),y,w,h,a['name'],[a['desc'],'Bénéfice recherché : '+a['benefit']],None,fs=9.2)
card(28,55,W-56,65,'Lecture économique',[P['page2']['metrics']['take']],None,fs=10)
footer(2,P['page2']['footer']['body'],P['page2']['sources']);c.showPage()
# PAGE 3
header(3,'Diagnostic public — pilotes, prérequis et questions d’investissement')
y=174;h=345;gap=9;left=260;right=W-56-left-gap
q=P['page3']['quadrant'];card(28,y,left,h,'Centralité × différenciation',[f'{z["row"]} / {z["col"]} : {z["label"]}' for z in q['cells']],'Différenciation et prix à prouver par comparaison.',fs=9.3)
ths=P['themes'];card(28+left+gap,y,right,h,'Priorités IA proposées',[f'{t["n"]}. {t["name"]} — {t["change"]}. Bénéfice : {t["benefit"]}. Approche : {t["feature"]}.' for t in ths],P['page3']['themes_take'],fs=9.7)
y=55;h=109;w=(W-56-2*gap)/3
card(28,y,w,h,'Transformation',['Cartographier ERP, qualité des données, owners et séries par site.'],None,fs=9.7)
D=P['page3']['ai_diag'];card(28+w+gap,y,w,h,'Maturité IA : '+D['level'],D['facts'],None,fs=9.4)
card(28+2*(w+gap),y,w,h,'Décision à prendre',['Comparer chaque pilote à la pratique actuelle sans IA.','GO si baseline, owner, données et contrôle validés.'],None,fs=9.5)
footer(3,P['page3']['footer']['body'],P['page3']['sources']);c.save()
print(out)
