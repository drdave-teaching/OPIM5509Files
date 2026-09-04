# -*- coding: utf-8 -*-
"""PEDW worksheet pair, v2 per Dave: vectors/matrices drawn as filled cell
rectangles (always given), formulas are what students fill in.
Numbers match 3_BackProp_and_ReLU.ipynb: x=[1,1,0] (D1), y=0, w=[0.52,0.18,-0.12], a=0.1.
Two pages: setup+legend, then 3 rounds. KEY + STUDENT versions."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2550, 3300
GOLD = (242, 183, 5); GOLDD = (140, 105, 8); GOLDT = (154, 120, 10)
DARK = (24, 26, 32); INK = (28, 30, 36); GREY = (120, 124, 134)
PAPER = (255, 255, 255); CARD = (255, 251, 238)
BOXLINE = (185, 183, 175); SOFT = (250, 216, 120)

AB = r"C:\Windows\Fonts\arialbd.ttf"; AR = r"C:\Windows\Fonts\arial.ttf"
F = lambda p, s: ImageFont.truetype(p, s)
OUT = r"C:\Users\dww05002\Documents\DL_Fall2026_GeneralMaterials\M31_review"

def page():
    im = Image.new('RGB', (W, H), PAPER)
    return im, ImageDraw.Draw(im, 'RGBA')

def footerbar(dr, pageno):
    dr.rectangle([0, H-36, W, H], fill=GOLD)
    dr.rectangle([0, H-46, W, H-36], fill=GOLDD)
    dr.text((150, H-115), "OPIM 5509 · Introduction to Deep Learning · Dr. Dave Wanik", font=F(AR, 34), fill=GREY)
    dr.text((2330, H-115), "p. %d" % pageno, font=F(AB, 34), fill=GREY)

def card(dr, x, y, w, h, title=None):
    dr.rounded_rectangle([x, y, x+w, y+h], 28, fill=CARD, outline=GOLD, width=5)
    if title:
        dr.text((x+45, y+32), title.upper(), font=F(AB, 40), fill=GOLDD)

def vec(dr, x, y, cells, labels=None, cw=230, chh=110, filled=True, name=None, namecolor=INK):
    """Draw a vector as a rectangle of cells. cells=list of strings ('' = empty)."""
    if name:
        dr.text((x, y + chh/2), name, font=F(AB, 48), fill=namecolor, anchor='rm')
    x0 = x + 30
    if labels:
        for i, lab in enumerate(labels):
            dr.text((x0 + i*cw + cw/2, y - 28), lab, font=F(AR, 32), fill=GREY, anchor='mm')
    for i, c in enumerate(cells):
        cx = x0 + i*cw
        dr.rectangle([cx, y, cx+cw, y+chh], fill=(252,252,250) if c=='' else (255,255,255),
                     outline=INK, width=5)
        if c != '':
            dr.text((cx+cw/2, y+chh/2), c, font=F(AB, 52), fill=INK, anchor='mm')
    return x0 + len(cells)*cw

def blank_line(dr, x, y, w, h=84):
    dr.rounded_rectangle([x, y, x+w, y+h], 14, fill=(252, 252, 250), outline=BOXLINE, width=4)

# --------------------------------------------------------- page 1
def page1(filled, subtitle):
    im, dr = page()
    dr.rectangle([150, 130, 400, 146], fill=GOLD)
    dr.text((150, 175), "OPIM 5509  ·  MODULE 2.1  ·  DENSE NEURAL NETWORKS", font=F(AB, 44), fill=GOLDT)
    dr.text((144, 240), "The P·E·D·W Worksheet", font=F(AB, 110), fill=INK)
    dr.text((150, 378), subtitle, font=F(AR, 48), fill=GREY)

    # setup card with drawn vectors
    y = 500
    card(dr, 150, y, 2250, 800, "the setup - one row of the golf logbook")
    dr.text((195, y+108), "Day D1 said:  hot, humid, calm  ...and the players stayed home.", font=F(AB, 46), fill=INK)
    dr.text((195, y+172), "Recoded for the network (1 = hot / humid / windy / played,  0 = cool / dry / calm / stayed home):", font=F(AR, 38), fill=GREY)
    vy = y + 300
    vec(dr, 480, vy, ['1', '1', '0'], labels=['Temp', 'Humidity', 'Wind'], name='inputs  x =')
    dr.text((1700, vy+55), 'target  y =', font=F(AB, 48), fill=INK, anchor='rm')
    vec(dr, 1700, vy, ['0'], labels=['Play?'])
    vy2 = vy + 230
    vec(dr, 480, vy2, ['0.52', '0.18', '-0.12'], labels=['w1', 'w2', 'w3'], name='weights  w =')
    dr.rounded_rectangle([1360, vy2, 1900, vy2+110], 20, fill=DARK)
    dr.text((1630, vy2+55), "\u03b1 = 0.1", font=F(AB, 52), fill=SOFT, anchor='mm')
    dr.text((1930, vy2+55), "(learning rate)", font=F(AR, 36), fill=GREY, anchor='lm')
    dr.text((195, y+720), "The starting weights are random guesses. Your job: use P·E·D·W three times and watch them learn.", font=F(AB, 38), fill=GOLDT)

    # legend card
    y2 = y + 860
    card(dr, 150, y2, 2250, 700, "the four moves - say them in order, every time")
    steps = [
        ("P", "PREDICTION", "P  =  x \u00b7 w  =  (x1\u00d7w1) + (x2\u00d7w2) + (x3\u00d7w3)", "the dot product - multiply and add"),
        ("E", "ERROR", "E  =  (y - P)\u00b2", "squared so it is always positive (just for tracking)"),
        ("D", "DELTA", "D  =  P - y", "signed miss: + means we OVERestimated"),
        ("W", "WEIGHT UPDATE", "new weight  =  old weight  -  \u03b1 \u00b7 ( its input \u00d7 D )", "scale by the input, step against the miss"),
    ]
    for i, (letter, nm, formula, note) in enumerate(steps):
        yy = y2 + 115 + i*120
        dr.rounded_rectangle([195, yy, 295, yy+95], 20, fill=DARK)
        dr.text((245, yy+48), letter, font=F(AB, 60), fill=GOLD, anchor='mm')
        dr.text((330, yy), nm, font=F(AB, 36), fill=INK)
        dr.text((330, yy+46), formula, font=F(AR, 42), fill=INK)
        dr.text((1560, yy+46), note, font=F(AR, 34), fill=GREY)
    dr.text((195, y2+615), "Overestimated (D > 0)?  weights SHRINK.   Underestimated (D < 0)?  weights GROW.   Input = 0?  that weight does NOT move!",
            font=F(AB, 36), fill=GOLDT)

    # how to read
    y3 = y2 + 760
    dr.rounded_rectangle([150, y3, 2400, y3+240], 24, fill=DARK)
    if filled:
        dr.text((195, y3+40), "HOW TO USE THIS KEY", font=F(AB, 40), fill=SOFT)
        dr.text((195, y3+105), "Every rectangle and every formula is filled in. Follow one round top to bottom, then try the blank", font=F(AR, 40), fill=(210, 212, 220))
        dr.text((195, y3+160), "version yourself - same numbers, no peeking until you finish a round.", font=F(AR, 40), fill=(210, 212, 220))
    else:
        dr.text((195, y3+40), "HOW TO USE THIS SHEET", font=F(AB, 40), fill=SOFT)
        dr.text((195, y3+105), "The rectangles (vectors) are all filled in for you - you never have to hunt for a number. The formulas", font=F(AR, 40), fill=(210, 212, 220))
        dr.text((195, y3+160), "are yours: fill every gold-edged blank. Each round's answer feeds the next round's rectangle - so you can self-check!", font=F(AR, 40), fill=(210, 212, 220))
    footerbar(dr, 1)
    return im

# --------------------------------------------------------- rounds data
ITERS = [
    dict(n=1, win=('0.52', '0.18', '-0.12'), wout=('0.45', '0.11', '-0.12'),
         P_ex='(1 \u00d7 0.52) + (1 \u00d7 0.18) + (0 \u00d7 -0.12)', P='0.70',
         E_ex='(0 - 0.70)\u00b2', E='0.49', D_ex='0.70 - 0', D='+0.70',
         W_ex=['0.52 - 0.1\u00d7(1\u00d70.70)', '0.18 - 0.1\u00d7(1\u00d70.70)', '-0.12 - 0.1\u00d7(0\u00d70.70)']),
    dict(n=2, win=('0.45', '0.11', '-0.12'), wout=('0.394', '0.054', '-0.12'),
         P_ex='(1 \u00d7 0.45) + (1 \u00d7 0.11) + (0 \u00d7 -0.12)', P='0.56',
         E_ex='(0 - 0.56)\u00b2', E='0.3136', D_ex='0.56 - 0', D='+0.56',
         W_ex=['0.45 - 0.1\u00d7(1\u00d70.56)', '0.11 - 0.1\u00d7(1\u00d70.56)', '-0.12 - 0.1\u00d7(0\u00d70.56)']),
    dict(n=3, win=('0.394', '0.054', '-0.12'), wout=('0.3492', '0.0092', '-0.12'),
         P_ex='(1 \u00d7 0.394) + (1 \u00d7 0.054) + (0 \u00d7 -0.12)', P='0.448',
         E_ex='(0 - 0.448)\u00b2', E='0.2007', D_ex='0.448 - 0', D='+0.448',
         W_ex=['0.394 - 0.1\u00d7(1\u00d70.448)', '0.054 - 0.1\u00d7(1\u00d70.448)', '-0.12 - 0.1\u00d7(0\u00d70.448)']),
]

def round_block(dr, y, it, filled):
    hh = 895
    card(dr, 150, y, 2250, hh)
    dr.rounded_rectangle([195, y+38, 560, y+118], 18, fill=DARK)
    dr.text((375, y+78), "ROUND %d" % it['n'], font=F(AB, 48), fill=SOFT, anchor='mm')
    # given rectangles: x and w-in (ALWAYS filled - Dave's rule)
    vy = y + 190
    vec(dr, 900, vy, ['1', '1', '0'], labels=['Temp', 'Hum', 'Wind'], cw=170, chh=95, name='x =')
    vec(dr, 1810, vy, list(it['win']), labels=['w1', 'w2', 'w3'], cw=185, chh=95, name='w in =')
    # formula rows P, E, D
    fy = y + 330
    rows = [('P', it['P_ex'], it['P'], '( 1 \u00d7 ______ ) + ( 1 \u00d7 ______ ) + ( 0 \u00d7 ______ )'),
            ('E', it['E_ex'], it['E'], '( 0  -  ______ )\u00b2'),
            ('D', it['D_ex'], it['D'], '______  -  0')]
    for i, (letter, ex, ans, skel) in enumerate(rows):
        yy = fy + i*105
        dr.rounded_rectangle([195, yy, 270, yy+80], 16, fill=GOLD)
        dr.text((232, yy+40), letter, font=F(AB, 46), fill=DARK, anchor='mm')
        body = ex if filled else skel
        dr.text((310, yy+16), body + '   =', font=F(AR, 44), fill=INK)
        bw = dr.textlength(body + '   =', font=F(AR, 44))
        if filled:
            dr.text((310 + bw + 45, yy+10), ans, font=F(AB, 50), fill=INK)
        else:
            blank_line(dr, 310 + bw + 45, yy-4, 320)
    # W row
    wy = fy + 3*105 + 15
    dr.rounded_rectangle([195, wy, 270, wy+80], 16, fill=GOLD)
    dr.text((232, wy+40), "W", font=F(AB, 46), fill=DARK, anchor='mm')
    for k in range(3):
        x = 310 + k*700
        lab = ['w1', 'w2', 'w3'][k]
        if filled:
            dr.text((x, wy), lab + ' = ' + it['W_ex'][k], font=F(AR, 34), fill=INK)
        else:
            dr.text((x, wy), lab + ' = ______ - 0.1\u00d7(' + ('1' if k < 2 else '0') + ' \u00d7 ______ )', font=F(AR, 34), fill=INK)
        dr.text((x, wy+52), '\u2193', font=F(AB, 36), fill=GOLDD)
    # weights-out rectangle: filled on KEY, empty cells on STUDENT
    oy = wy + 120
    if filled:
        end = vec(dr, 900, oy, list(it['wout']), cw=185, chh=95, name='w out =')
        if it['n'] == 1:
            dr.text((end+40, oy+48), '\u2190 w3 didn\u2019t move - its input was 0!', font=F(AB, 36), fill=GOLDT, anchor='lm')
        else:
            dr.text((end+40, oy+48), '\u2190 carry these into Round %d' % (it['n']+1) if it['n'] < 3 else '\u2190 final weights!', font=F(AR, 34), fill=GREY, anchor='lm')
    else:
        end = vec(dr, 900, oy, ['', '', ''], cw=185, chh=95, name='w out =')
        dr.text((end+40, oy+48), '\u2190 write them here, then peek at Round %d' % (it['n']+1) + (' to check!' if it['n'] < 3 else ''), font=F(AR, 34), fill=GOLDT, anchor='lm') if it['n'] < 3 else \
        dr.text((end+40, oy+48), '\u2190 check against the strip below!', font=F(AR, 34), fill=GOLDT, anchor='lm')
    return y + hh

def page2(filled):
    im, dr = page()
    dr.rectangle([150, 110, 400, 126], fill=GOLD)
    dr.text((150, 150), "P·E·D·W  ·  THREE ROUNDS ON ROW D1" + ("  ·  ANSWER KEY" if filled else "  ·  YOUR TURN"), font=F(AB, 44), fill=GOLDT)
    y = 225
    for it in ITERS:
        y = round_block(dr, y, it, filled) + 18
    # check strip
    dr.rounded_rectangle([150, y, 2400, y+185], 24, fill=DARK)
    if filled:
        dr.text((195, y+35), "WHAT TO NOTICE:  P marches toward the target:  0.70 \u2192 0.56 \u2192 0.448  (each round is 0.8\u00d7 the last!)", font=F(AB, 40), fill=SOFT)
        dr.text((195, y+100), "We overestimated every round (D > 0), so the active weights kept shrinking - and w3 never moved. Zero in, zero learned.", font=F(AR, 38), fill=(205, 207, 215))
    else:
        dr.text((195, y+35), "CHECK YOURSELF:   P1 = 0.70      P2 = 0.56      P3 = 0.448      final w = [ 0.3492 ,  0.0092 ,  -0.12 ]", font=F(AB, 40), fill=SOFT)
        dr.text((195, y+100), "Stuck? Say the four letters out loud - P... E... D... W - and remember: an input of 0 sends no information.", font=F(AR, 38), fill=(205, 207, 215))
    footerbar(dr, 2)
    print(('KEY' if filled else 'STUDENT') + ' page2 content ends at', y+185)
    return im

for filled, fname, sub in [
    (True, 'PEDW_Worksheet_KEY.pdf', 'Forward + backprop by hand, one row of golf data  -  the ANSWER KEY'),
    (False, 'PEDW_Worksheet_STUDENT.pdf', 'Forward + backprop by hand, one row of golf data  -  YOUR TURN')]:
    p1 = page1(filled, sub); p2 = page2(filled)
    p1.save(os.path.join(OUT, fname), 'PDF', resolution=300, save_all=True, append_images=[p2])
    p1.save(os.path.join(OUT, fname.replace('.pdf', '_p1.png')))
    p2.save(os.path.join(OUT, fname.replace('.pdf', '_p2.png')))
    print('built', fname)
