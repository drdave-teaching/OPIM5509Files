# -*- coding: utf-8 -*-
"""PEDW ADVANCED worksheet - one hidden layer, real weight matrices.
Mirrors 3_BackProp_and_ReLU.ipynb 'Our First Deep Neural Network':
x=[1,0,0] (D13: hot, dry, calm -> PLAYED, y=1), W01 3x4, hidden 1x4 w/ ReLU,
W12 4x1, alpha=0.1, seed(1) weights rounded to 2dp so hand math checks exactly.
3 pages x 2 versions (KEY filled / STUDENT blanks)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2550, 3300
GOLD = (242, 183, 5); GOLDD = (140, 105, 8); GOLDT = (154, 120, 10)
DARK = (24, 26, 32); INK = (28, 30, 36); GREY = (120, 124, 134)
PAPER = (255, 255, 255); CARD = (255, 251, 238)
BOXLINE = (185, 183, 175); SOFT = (250, 216, 120); BLANKBG = (252, 252, 250)

AB = r"C:\Windows\Fonts\arialbd.ttf"; AR = r"C:\Windows\Fonts\arial.ttf"
CO = r"C:\Windows\Fonts\consola.ttf"
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
        dr.text((x+45, y+30), title.upper(), font=F(AB, 38), fill=GOLDD)

def mat(dr, x, y, rows, col_labels=None, row_labels=None, cw=200, chh=92, name=None, hot=None):
    """rows = list of list of strings ('' = blank cell). hot = set of (r,c) to tint gold."""
    if name:
        h = len(rows)*chh
        dr.text((x, y + h/2), name, font=F(AB, 44), fill=INK, anchor='rm')
    x0 = x + 28
    if col_labels:
        for j, lab in enumerate(col_labels):
            dr.text((x0 + j*cw + cw/2, y - 26), lab, font=F(AR, 30), fill=GREY, anchor='mm')
    for i, row in enumerate(rows):
        if row_labels:
            dr.text((x0 - 18, y + i*chh + chh/2), row_labels[i], font=F(AR, 30), fill=GREY, anchor='rm')
        for j, c in enumerate(row):
            cx, cy = x0 + j*cw, y + i*chh
            tint = hot and (i, j) in hot
            dr.rectangle([cx, cy, cx+cw, cy+chh],
                         fill=(255, 244, 205) if tint else (BLANKBG if c == '' else (255, 255, 255)),
                         outline=INK, width=4)
            if c != '':
                dr.text((cx+cw/2, cy+chh/2), c, font=F(AB, 42), fill=INK, anchor='mm')
    return x0 + len(rows[0])*cw, y + len(rows)*chh

def blank_line(dr, x, y, w, h=80):
    dr.rounded_rectangle([x, y, x+w, y+h], 14, fill=BLANKBG, outline=BOXLINE, width=4)

def step_badge(dr, x, y, txt, wpx=None):
    wpx = wpx or (90 + int(dr.textlength(txt, font=F(AB, 40))))
    dr.rounded_rectangle([x, y, x+wpx, y+78], 18, fill=DARK)
    dr.text((x+wpx/2, y+39), txt, font=F(AB, 40), fill=SOFT, anchor='mm')
    return x + wpx

# ---------- ground truth (seed(1) weights rounded to 2dp; all math exact from there)
W01 = [['-0.17', '0.44', '-1.00', '-0.40'],
       ['-0.71', '-0.82', '-0.63', '-0.31'],
       ['-0.21', '0.08', '-0.16', '0.37']]
W12 = [['-0.59'], ['0.76'], ['-0.95'], ['0.34']]
NODES = ['node1', 'node2', 'node3', 'node4']
INPUTS = ['Temp', 'Humidity', 'Wind']

# ============================================================ PAGE 1: SETUP
def page1(filled):
    im, dr = page()
    dr.rectangle([150, 120, 400, 136], fill=GOLD)
    dr.text((150, 162), "OPIM 5509  ·  MODULE 2.1  ·  DENSE NEURAL NETWORKS", font=F(AB, 44), fill=GOLDT)
    dr.text((144, 226), "P·E·D·W  Advanced", font=F(AB, 108), fill=INK)
    dr.text((150, 362), "One hidden layer, real weight matrices - same four moves" + ("  -  the ANSWER KEY" if filled else "  -  YOUR TURN"), font=F(AR, 46), fill=GREY)

    # setup card
    y = 480
    card(dr, 150, y, 2250, 1080, "the setup - day D13 of the golf logbook")
    dr.text((195, y+100), "D13 said:  hot, dry, calm  ...and they PLAYED!  (so this time the target is 1)", font=F(AB, 44), fill=INK)
    vy = y + 250
    mat(dr, 640, vy, [['1', '0', '0']], col_labels=INPUTS, name='layer_0  =', cw=180, chh=92)
    dr.text((1900, vy+46), 'target  y =', font=F(AB, 44), fill=INK, anchor='rm')
    mat(dr, 1900, vy, [['1']], col_labels=['Play?'], cw=180, chh=92)
    my = vy + 210
    dr.text((195, my-56), "The weight matrices (random start, seed(1), rounded to 2 decimals - your hand math will check exactly):", font=F(AR, 36), fill=GREY)
    dr.text((530, my+40+142), 'weights_0_1  =', font=F(AB, 44), fill=INK, anchor='rm')
    ex, eyy = mat(dr, 700, my+40, W01, col_labels=NODES, row_labels=INPUTS, cw=195, chh=95)
    mat(dr, 2000, my+40, W12, row_labels=NODES, name='weights_1_2  =', cw=195, chh=95)
    dr.rounded_rectangle([195, eyy+75, 800, eyy+180], 20, fill=DARK)
    dr.text((497, eyy+127), "\u03b1 = 0.1", font=F(AB, 50), fill=SOFT, anchor='mm')
    dr.text((830, eyy+127), "(learning rate)   ·   3\u00d74 = 12 weights into the hidden layer, 4 more to the output: 16 total", font=F(AR, 34), fill=GREY, anchor='lm')

    # relu card
    y2 = y + 1150
    card(dr, 150, y2, 2250, 560, "two tiny handcrafted functions - this is ALL the magic")
    dr.rounded_rectangle([195, y2+105, 1240, y2+330], 20, fill=DARK)
    for k, ln in enumerate(["def relu(x):", "    return (x > 0) * x", "", "def relu2deriv(output):", "    return output > 0"]):
        dr.text((235, y2+130 + k*40), ln, font=F(CO, 34), fill=(230, 232, 238))
    dr.text((1300, y2+120), "relu: a negative number gets recoded to 0.", font=F(AB, 36), fill=INK)
    dr.text((1300, y2+175), "(positive numbers pass straight through)", font=F(AR, 33), fill=GREY)
    dr.text((1300, y2+250), "relu2deriv: THE MASK. 1 if the node fired,", font=F(AB, 36), fill=INK)
    dr.text((1300, y2+305), "0 if it slept. Sleeping nodes learn nothing.", font=F(AR, 33), fill=GREY)
    dr.text((195, y2+400), "Forward:  layer_1 = relu( layer_0 \u00b7 W01 )    then    prediction = layer_1 \u00b7 W12    (no relu at the output!)", font=F(AR, 38), fill=INK)
    dr.text((195, y2+470), "Backward: the delta flows back through the SAME weights - and relu2deriv silences the nodes that never fired.", font=F(AR, 38), fill=INK)

    # plan strip
    y3 = y2 + 620
    dr.rounded_rectangle([150, y3, 2400, y3+250], 24, fill=DARK)
    dr.text((195, y3+35), "THE FLIGHT PLAN (same P·E·D·W, just with matrices)", font=F(AB, 40), fill=SOFT)
    dr.text((195, y3+105), "p.2  FORWARD:  layer_1 before relu \u2192 relu \u2192 prediction        then E and D", font=F(AR, 40), fill=(210, 212, 220))
    dr.text((195, y3+165), "p.3  BACKWARD: update weights_1_2, build layer_1_delta (the mask!), update weights_0_1", font=F(AR, 40), fill=(210, 212, 220))
    footerbar(dr, 1)
    return im

# ============================================================ PAGE 2: FORWARD
def page2(filled):
    im, dr = page()
    dr.rectangle([150, 110, 400, 126], fill=GOLD)
    dr.text((150, 150), "FORWARD PASS  +  E  +  D" + ("   ·   ANSWER KEY" if filled else "   ·   YOUR TURN"), font=F(AB, 44), fill=GOLDT)

    # F1: layer_1 before relu
    y = 250
    card(dr, 150, y, 2250, 800)
    step_badge(dr, 195, y+35, "P - step 1:  layer_1 (before relu)  =  layer_0 \u00b7 W01")
    dr.text((195, y+135), "One dot product per hidden node - walk the columns of W01 with x = [1, 0, 0]:", font=F(AR, 36), fill=GREY)
    exprs = [("node1", "(1\u00d7-0.17) + (0\u00d7-0.71) + (0\u00d7-0.21)", "-0.17"),
             ("node2", "(1\u00d7 0.44) + (0\u00d7-0.82) + (0\u00d7 0.08)", "0.44"),
             ("node3", "(1\u00d7-1.00) + (0\u00d7-0.63) + (0\u00d7-0.16)", "-1.00"),
             ("node4", "(1\u00d7-0.40) + (0\u00d7-0.31) + (0\u00d7 0.37)", "-0.40")]
    for i, (nd, ex, ans) in enumerate(exprs):
        yy = y + 205 + i*100
        dr.text((225, yy+12), nd + ":", font=F(AB, 38), fill=INK)
        dr.text((430, yy+12), ex + "  =", font=F(AR, 40), fill=INK)
        if filled:
            dr.text((1560, yy+8), ans, font=F(AB, 46), fill=INK)
        else:
            blank_line(dr, 1560, yy-4, 280)
    mat(dr, 950, y + 640, [([c for c in ('-0.17', '0.44', '-1.00', '-0.40')] if filled else ['', '', '', ''])],
        col_labels=NODES, name='layer_1 (pre-relu) =', cw=195, chh=95)

    # F2: relu
    y2 = y + 860
    card(dr, 150, y2, 2250, 420)
    step_badge(dr, 195, y2+35, "P - step 2:  layer_1  =  relu( layer_1 )")
    dr.text((195, y2+135), "Negative? Recode to 0. Positive? Pass through.", font=F(AR, 36), fill=GREY)
    mat(dr, 950, y2 + 230, [(['0', '0.44', '0', '0'] if filled else ['', '', '', ''])],
        col_labels=NODES, name='layer_1 =', cw=195, chh=95, hot={(0, 1)} if filled else None)
    if filled:
        dr.text((1800, y2+272), "\u2190 only node2 fired!", font=F(AB, 36), fill=GOLDT, anchor='lm')

    # F3: prediction + E + D
    y3 = y2 + 480
    card(dr, 150, y3, 2250, 660)
    step_badge(dr, 195, y3+35, "P - step 3:  prediction  =  layer_1 \u00b7 W12        then  E  and  D")
    rows = [("P", "(0\u00d7-0.59) + (0.44\u00d70.76) + (0\u00d7-0.95) + (0\u00d70.34)  =", "0.3344"),
            ("E", "(1 - 0.3344)\u00b2  =", "0.443"),
            ("D", "0.3344 - 1  =", "-0.6656")]
    skel = {"P": "(0\u00d7-0.59) + ( ____ \u00d70.76) + (0\u00d7-0.95) + (0\u00d70.34)  =",
            "E": "(1 - ______ )\u00b2  =", "D": "______ - 1  ="}
    for i, (letter, ex, ans) in enumerate(rows):
        yy = y3 + 160 + i*115
        dr.rounded_rectangle([195, yy, 270, yy+80], 16, fill=GOLD)
        dr.text((232, yy+40), letter, font=F(AB, 44), fill=DARK, anchor='mm')
        body = ex if filled else skel[letter]
        dr.text((310, yy+16), body, font=F(AR, 42), fill=INK)
        bw = dr.textlength(body, font=F(AR, 42))
        if filled:
            dr.text((310+bw+45, yy+10), ans, font=F(AB, 48), fill=INK)
        else:
            blank_line(dr, 310+bw+45, yy-2, 320)
    dr.text((195, y3+540), ("D is NEGATIVE: we UNDERestimated (they played and we said 0.33). The messenger weights must get BIGGER."
                            if filled else "Is D positive or negative? Did we over- or under-estimate? Which direction must the messenger weights move?"),
            font=F(AB, 36), fill=GOLDT)
    footerbar(dr, 2)
    return im

# ============================================================ PAGE 3: BACKWARD
def page3(filled):
    im, dr = page()
    dr.rectangle([150, 110, 400, 126], fill=GOLD)
    dr.text((150, 150), "BACKWARD PASS - THE W IN P·E·D·W" + ("   ·   ANSWER KEY" if filled else "   ·   YOUR TURN"), font=F(AB, 44), fill=GOLDT)

    # W-a: update W12
    y = 250
    card(dr, 150, y, 2250, 780)
    step_badge(dr, 195, y+35, "W (part a):  weight_delta_1_2 = layer_1 \u00d7 D      then update W12")
    dr.text((195, y+135), "Each hidden node's activation times the delta. Keep 4 decimals.", font=F(AR, 36), fill=GREY)
    upds = [("node1", "0 \u00d7 -0.6656", "0", "-0.59 - 0.1\u00d70", "-0.59"),
            ("node2", "0.44 \u00d7 -0.6656", "-0.2929", "0.76 - 0.1\u00d7(-0.2929)", "0.7893"),
            ("node3", "0 \u00d7 -0.6656", "0", "-0.95 - 0.1\u00d70", "-0.95"),
            ("node4", "0 \u00d7 -0.6656", "0", "0.34 - 0.1\u00d70", "0.34")]
    dr.text((520, y+205), "weight_delta_1_2", font=F(AB, 34), fill=GOLDD)
    dr.text((1500, y+205), "new W12", font=F(AB, 34), fill=GOLDD)
    for i, (nd, ex, wd, upd, ans) in enumerate(upds):
        yy = y + 265 + i*105
        dr.text((225, yy+12), nd + ":", font=F(AB, 36), fill=INK)
        dr.text((450, yy+12), ex + " =", font=F(AR, 38), fill=INK)
        if filled: dr.text((940, yy+8), wd, font=F(AB, 42), fill=INK)
        else: blank_line(dr, 940, yy-2, 250, 74)
        dr.text((1280, yy+12), upd + " =", font=F(AR, 38), fill=INK)
        if filled: dr.text((1960, yy+8), ans, font=F(AB, 42), fill=INK if nd == 'node2' else GREY)
        else: blank_line(dr, 1960, yy-2, 250, 74)
    dr.text((195, y+700), ("Only node2's weight moved: 0.76 \u2192 0.7893. It UNDERdelivered, so its volume gets turned UP."
                           if filled else "How many of the four weights actually move? Why those?"), font=F(AB, 36), fill=GOLDT)

    # W-b: layer_1_delta + mask
    y2 = y + 840
    card(dr, 150, y2, 2250, 620)
    step_badge(dr, 195, y2+35, "W (part b):  layer_1_delta = D \u00d7 W12   ...then APPLY THE MASK")
    dr.text((195, y2+135), "Send the miss backward through the same weights: D \u00d7 each W12 value. Keep 4 decimals.", font=F(AR, 36), fill=GREY)
    pre = ['0.3927', '-0.5059', '0.6323', '-0.2263']
    mat(dr, 1030, y2+245, [(pre if filled else ['', '', '', ''])], col_labels=NODES, name='before the mask =', cw=230, chh=92)
    dr.text((195, y2+400), "\u00d7 relu2deriv(layer_1) = [0, 1, 0, 0]   \u2192", font=F(AB, 38), fill=INK)
    mat(dr, 1280, y2+460, [(['0', '-0.5059', '0', '0'] if filled else ['', '', '', ''])], col_labels=None, name='layer_1_delta =', cw=230, chh=92, hot={(0, 1)} if filled else None)
    if filled:
        dr.text((2230, y2+500), "\u2190 the mask", font=F(AB, 32), fill=GOLDT, anchor='lm')
        dr.text((2230, y2+545), "kills the sleepers", font=F(AB, 32), fill=GOLDT, anchor='lm')

    # W-c: update W01
    y3 = y2 + 680
    card(dr, 150, y3, 2250, 700)
    step_badge(dr, 195, y3+35, "W (part c):  weight_delta_0_1 = layer_0\u1d40 \u00d7 layer_1_delta      then update W01")
    dr.text((195, y3+135), "Outer product: each INPUT row times layer_1_delta. Inputs Humidity and Wind were 0 - whole rows of zeros!", font=F(AR, 36), fill=GREY)
    wd01 = [['0', '-0.5059', '0', '0'], ['0', '0', '0', '0'], ['0', '0', '0', '0']]
    blank3 = [['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    dr.text((420, y3+370), 'wt_delta_0_1 =', font=F(AB, 40), fill=INK, anchor='rm')
    mat(dr, 480, y3+250, (wd01 if filled else blank3), col_labels=NODES, row_labels=None, cw=170, chh=80, hot={(0, 1)} if filled else None)
    dr.text((445, y3+282), 'Temp', font=F(AR, 28), fill=GREY, anchor='rm')
    dr.text((445, y3+362), 'Hum', font=F(AR, 28), fill=GREY, anchor='rm')
    dr.text((445, y3+442), 'Wind', font=F(AR, 28), fill=GREY, anchor='rm')
    new01 = [['-0.17', '0.4906', '-1.00', '-0.40'], ['-0.71', '-0.82', '-0.63', '-0.31'], ['-0.21', '0.08', '-0.16', '0.37']]
    mat(dr, 1760, y3+250, (new01 if filled else blank3), col_labels=NODES, name='new W01 =', cw=140, chh=80, hot={(0, 1)} if filled else None)
    dr.text((195, y3+560), ("Only (Temp \u2192 node2) moves:  0.44 - 0.1\u00d7(-0.5059) = 0.4906.  15 of 16 weights slept through this round!"
                            if filled else "Update rule per cell:  new = old - 0.1 \u00d7 delta.  How many of the 16 weights actually change?"),
            font=F(AB, 36), fill=GOLDT)

    # check strip
    y4 = y3 + 760
    dr.rounded_rectangle([150, y4, 2400, y4+190], 24, fill=DARK)
    if filled:
        dr.text((195, y4+35), "THE MORAL:  information only flows - forward OR backward - through nodes that FIRE.", font=F(AB, 40), fill=SOFT)
        dr.text((195, y4+100), "Temp built node2, node2 built the prediction, so the credit (and the blame) lands on exactly that path.", font=F(AR, 38), fill=(205, 207, 215))
    else:
        dr.text((195, y4+35), "CHECK YOURSELF:   P = 0.3344    D = -0.6656    new W12 node2 = 0.7893    new W01 (Temp\u2192node2) = 0.4906", font=F(AB, 38), fill=SOFT)
        dr.text((195, y4+100), "Everything else stays frozen. If more than 2 of your weights moved, hunt down which zero you dropped.", font=F(AR, 38), fill=(205, 207, 215))
    footerbar(dr, 3)
    return im

for filled, fname in [(True, 'PEDW_Advanced_KEY.pdf'), (False, 'PEDW_Advanced_STUDENT.pdf')]:
    p1, p2, p3 = page1(filled), page2(filled), page3(filled)
    p1.save(os.path.join(OUT, fname), 'PDF', resolution=300, save_all=True, append_images=[p2, p3])
    for i, p in enumerate([p1, p2, p3], 1):
        p.save(os.path.join(OUT, fname.replace('.pdf', '_p%d.png' % i)))
    print('built', fname)
