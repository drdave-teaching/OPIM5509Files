# -*- coding: utf-8 -*-
"""ConvNet Size & Trainable Parameters practice worksheets (M3.1), PEDW-style.
Two levels (Simple/Advanced) x two versions (STUDENT blank / KEY filled) = 4 PDFs.
Students fill Output shape + Trainable params for each layer using the two formulas.
Architectures TF-verified: Simple total 32,988; Advanced total 319,521."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2550, 3300
GOLD=(242,183,5); GOLDD=(140,105,8); GOLDT=(154,120,10)
INK=(28,30,36); GREY=(120,124,134); PAPER=(255,255,255); CARD=(255,251,238)
BOXLINE=(185,183,175); BLANKBG=(252,252,250); DARKCODE=(30,32,40); CODEINK=(230,232,238)
GOLDCODE=(245,200,90)
AB=r"C:\Windows\Fonts\arialbd.ttf"; AR=r"C:\Windows\Fonts\arial.ttf"
CON=r"C:\Windows\Fonts\consola.ttf"; CONB=r"C:\Windows\Fonts\consolab.ttf"
F=lambda p,s: ImageFont.truetype(p,s)
OUT=os.path.dirname(os.path.abspath(__file__))

SIMPLE = {
 'level':'Simple', 'sub':'One black-and-white image through a small ConvNet — the lecture example.',
 'input':'(28, 28, 1)',
 'code':[
   "model = models.Sequential()",
   "model.add(layers.Conv2D(3, (5, 5), activation='relu',",
   "                        input_shape=(28, 28, 1)))",
   "model.add(layers.MaxPooling2D((2, 2)))",
   "model.add(layers.Conv2D(5, (3, 3), activation='relu'))",
   "model.add(layers.MaxPooling2D((2, 2)))",
   "model.add(layers.Flatten())",
   "model.add(layers.Dense(256, activation='relu'))",
   "model.add(layers.Dense(2, activation='softmax'))",
 ],
 'rows':[
   ("Conv2D: F=3, (5x5)", "(24, 24, 3)", "78",     "28-(5-1)=24;  ((5x5x1)+1)x3"),
   ("MaxPool 2x2",         "(12, 12, 3)", "0",      "24/2=12;  nothing learned"),
   ("Conv2D: F=5, (3x3)", "(10, 10, 5)", "140",    "12-(3-1)=10;  ((3x3x3)+1)x5   L=3 in!"),
   ("MaxPool 2x2",         "(5, 5, 5)",   "0",      "10/2=5"),
   ("Flatten",             "(125,)",      "0",      "5x5x5 = 125"),
   ("Dense(256)",          "(256,)",      "32,256", "(125+1)x256"),
   ("Dense(2, softmax)",   "(2,)",        "514",    "(256+1)x2"),
 ],
 'total':"32,988",
}
ADV = {
 'level':'Advanced', 'sub':'A color image through a deeper ConvNet — no number repeats, so lean on the formulas.',
 'input':'(64, 64, 3)',
 'code':[
   "model = models.Sequential()",
   "model.add(layers.Conv2D(16, (5, 5), activation='relu',",
   "                        input_shape=(64, 64, 3)))",
   "model.add(layers.MaxPooling2D((2, 2)))",
   "model.add(layers.Conv2D(32, (3, 3), activation='relu'))",
   "model.add(layers.MaxPooling2D((2, 2)))",
   "model.add(layers.Conv2D(64, (3, 3), activation='relu'))",
   "model.add(layers.MaxPooling2D((2, 2)))",
   "model.add(layers.Flatten())",
   "model.add(layers.Dense(128, activation='relu'))",
   "model.add(layers.Dense(1, activation='sigmoid'))",
 ],
 'rows':[
   ("Conv2D: F=16, (5x5)", "(60, 60, 16)", "1,216",   "64-(5-1)=60;  ((5x5x3)+1)x16   L=3 (RGB)"),
   ("MaxPool 2x2",          "(30, 30, 16)", "0",       "60/2=30"),
   ("Conv2D: F=32, (3x3)", "(28, 28, 32)", "4,640",   "30-(3-1)=28;  ((3x3x16)+1)x32   L=16 in"),
   ("MaxPool 2x2",          "(14, 14, 32)", "0",       "28/2=14"),
   ("Conv2D: F=64, (3x3)", "(12, 12, 64)", "18,496",  "14-(3-1)=12;  ((3x3x32)+1)x64   L=32 in"),
   ("MaxPool 2x2",          "(6, 6, 64)",   "0",       "12/2=6"),
   ("Flatten",              "(2304,)",      "0",       "6x6x64 = 2304"),
   ("Dense(128)",           "(128,)",       "295,040", "(2304+1)x128"),
   ("Dense(1, sigmoid)",    "(1,)",         "129",     "(128+1)x1"),
 ],
 'total':"319,521",
}

def build(data, filled):
    im=Image.new('RGB',(W,H),PAPER); dr=ImageDraw.Draw(im,'RGBA')
    # header
    dr.rectangle([150,120,410,136],fill=GOLD)
    dr.text((150,165),"OPIM 5509  ·  MODULE 3.1  ·  CONVOLUTIONAL NEURAL NETWORKS",font=F(AB,40),fill=GOLDT)
    dr.text((144,228),"ConvNet Size & Parameters",font=F(AB,104),fill=INK)
    tag=("%s  ·  %s"%(data['level'],'ANSWER KEY' if filled else 'STUDENT — fill in the blanks'))
    dr.text((150,360),tag,font=F(AB,46),fill=(GOLDD if filled else GREY))
    dr.text((150,424),data['sub'],font=F(AR,38),fill=GREY)

    y=500
    # formula reference card
    ch=430
    dr.rounded_rectangle([150,y,2400,y+ch],28,fill=CARD,outline=GOLD,width=5)
    dr.text((195,y+28),"THE ONLY TWO FORMULAS (stride 1, no padding)",font=F(AB,40),fill=GOLDD)
    fl=[
      "Conv2D:   params = ((M x N x L) + B) x F        new size = old size - (M - 1)",
      "MaxPool:  params = 0                            new size = old size / pool",
      "Flatten:  params = 0                            size = rows x cols x channels",
      "Dense:    params = (inputs + 1) x nodes         size = nodes",
    ]
    yy=y+96
    for line in fl:
        dr.text((195,yy),line,font=F(CONB,34),fill=INK); yy+=52
    yy+=8
    dr.text((195,yy),"M, N = kernel size    L = channels coming IN (inherited, never chosen)",font=F(AR,32),fill=GOLDT); yy+=44
    dr.text((195,yy),"B = bias = 1          F = filters = feature maps coming OUT (you choose)",font=F(AR,32),fill=GOLDT)

    y=y+ch+45
    # code card (given)
    codeh=70+len(data['code'])*46+30
    dr.rounded_rectangle([150,y,2400,y+codeh],28,fill=DARKCODE)
    dr.text((195,y+26),"THE CODE  (given)",font=F(AB,34),fill=GOLDCODE)
    yy=y+86
    for ln in data['code']:
        dr.text((195,yy),ln,font=F(CON,34),fill=CODEINK); yy+=46

    y=y+codeh+45
    # table
    cols=[(150,760,'Layer'),(910,1330,'Output shape'),(1330,1660,'Params'),(1660,2400,'The math')]
    rowh=118; headh=70
    # header row
    dr.rectangle([150,y,2400,y+headh],fill=(245,238,214),outline=INK,width=4)
    for x0,x1,lab in cols:
        dr.text(((x0+x1)//2,y+headh//2),lab,font=F(AB,36),fill=INK,anchor='mm')
    y+=headh
    for (lname,shape,params,math) in data['rows']:
        dr.rectangle([150,y,2400,y+rowh],outline=INK,width=3)
        for x0,x1,_ in cols: dr.line([x1,y,x1,y+rowh],fill=INK,width=3)
        dr.text((175,y+rowh//2),lname,font=F(AB,34),fill=INK,anchor='lm')
        def cell(x0,x1,txt,mono=True,gold=False):
            cx=(x0+x1)//2
            if filled and txt:
                dr.text((cx,y+rowh//2),txt,font=F(CONB if mono else AB,36),
                        fill=(GOLDD if gold else INK),anchor='mm')
            else:
                dr.rounded_rectangle([x0+22,y+24,x1-22,y+rowh-24],12,fill=BLANKBG,outline=BOXLINE,width=3)
        cell(910,1330,shape)
        cell(1330,1660,params,gold=(params not in ('0','')))
        # math column: KEY shows it; STUDENT gets a blank work area
        if filled:
            dr.text((1685,y+rowh//2),math,font=F(CON,28),fill=GREY,anchor='lm')
        else:
            dr.rounded_rectangle([1682,y+24,2378,y+rowh-24],12,fill=BLANKBG,outline=BOXLINE,width=3)
        y+=rowh
    # total row
    dr.rectangle([150,y,2400,y+rowh],fill=(245,238,214),outline=INK,width=4)
    dr.line([1330,y,1330,y+rowh],fill=INK,width=3); dr.line([1660,y,1660,y+rowh],fill=INK,width=3)
    dr.text((175,y+rowh//2),"TOTAL trainable parameters",font=F(AB,38),fill=INK,anchor='lm')
    if filled:
        dr.text((1495,y+rowh//2),data['total'],font=F(CONB,40),fill=GOLDD,anchor='mm')
    else:
        dr.rounded_rectangle([1352,y+24,1638,y+rowh-24],12,fill=BLANKBG,outline=BOXLINE,width=3)
    y+=rowh

    # footer
    dr.rectangle([0,H-36,W,H],fill=GOLD); dr.rectangle([0,H-46,W,H-36],fill=GOLDD)
    dr.text((150,H-118),"OPIM 5509 · Introduction to Deep Learning · Dr. Dave Wanik",font=F(AR,32),fill=GREY)
    tip=("Answer key — every shape and count worked out." if filled
         else "Fill Output shape + Params for each layer, then total. Check against model.summary().")
    dr.text((150,H-172),tip,font=F(AR,32),fill=GOLDT)
    return im

for data in (SIMPLE,ADV):
    for filled in (False,True):
        im=build(data,filled)
        fn=os.path.join(OUT,"ConvNetParams_%s_%s.pdf"%(data['level'],'KEY' if filled else 'STUDENT'))
        im.save(fn,"PDF",resolution=300.0)
        print("wrote",os.path.basename(fn))
print("done")
