# -*- coding: utf-8 -*-
"""Math deck - one layer per slide, one big calculation, running total.
Imports the shared helpers from build_decks.py (which also builds the theory deck)."""
from build_decks import *   # noqa

CHAIN = [
    ('INPUT',          '(None, 28, 28, 1)', None),
    ('Conv2D 3 @ 5x5', '(None, 24, 24, 3)', '78'),
    ('MaxPool 2x2',    '(None, 12, 12, 3)', '0'),
    ('Conv2D 5 @ 3x3', '(None, 10, 10, 5)', '140'),
    ('MaxPool 2x2',    '(None, 5, 5, 5)',   '0'),
    ('Flatten',        '(None, 125)',       '0'),
    ('Dense 256',      '(None, 256)',       '32,256'),
    ('Dense 2',        '(None, 2)',         '514'),
]

def chain_strip(s, upto, y=1.95, small=True):
    n = len(CHAIN)
    bw, gap = 1.42, 0.145
    x = (W - (n*bw + (n-1)*gap)) / 2
    ch = 1.05 if small else 1.5
    for i, (name, shape, parm) in enumerate(CHAIN):
        cur = (i == upto); future = (i > upto); done = (i < upto)
        fill = PAPER if not future else CHIPOFF
        line = GOLD if cur else (GOLDD if done and parm not in (None, '0') else RGBColor(0xC8, 0xC6, 0xBE))
        c = rect(s, x, y, bw, ch, fill, line=line, lw=3.0 if cur else 1.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        c.adjustments[0] = 0.14
        tcol = INK if not future else RGBColor(0xB4, 0xB2, 0xAA)
        text(s, x+0.06, y+0.10, bw-0.12, 0.32, name, size=10.5, color=tcol, bold=True, align=PP_ALIGN.CENTER)
        text(s, x+0.03, y+0.42, bw-0.06, 0.3, shape, size=9.5, color=tcol if future else GREY, align=PP_ALIGN.CENTER)
        if not future and parm is not None:
            bcol = GOLD if parm != '0' else RGBColor(0xE1, 0xDF, 0xD7)
            b = rect(s, x+0.16, y+ch-0.34, bw-0.32, 0.26, bcol, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
            b.adjustments[0] = 0.5
            text(s, x+0.16, y+ch-0.315, bw-0.32, 0.22, parm, size=9.5,
                 color=DARK if parm != '0' else GREY, bold=True, align=PP_ALIGN.CENTER)
        if i < n-1:
            ar = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, IN(x+bw+0.01), IN(y+ch/2), IN(x+bw+gap-0.01), IN(y+ch/2))
            ar.line.color.rgb = GOLDD if i < upto else RGBColor(0xC8, 0xC6, 0xBE)
            ar.line.width = Pt(2.2); ar.shadow.inherit = False
        x += bw + gap

def big2(lines):
    out = []
    for k, ln in enumerate(lines):
        last = (k == len(lines) - 1)
        out.append([(ln, {'size': 30 if last else 20, 'bold': last, 'color': INK if last else GREY})])
    return out

def calc_slide(prs, n, upto, title, size_lines, parm_lines, running, note, trap=None):
    s = blank(prs)
    header(s, 'Module 3.1 - Size & Trainable Parameters', title, tsize=34)
    chain_strip(s, upto)
    ly = 3.35
    card(s, 0.85, ly, 5.75, 2.55, 'output size')
    text(s, 1.2, ly+0.62, 5.1, 1.7, big2(size_lines), spacing=1.15)
    card(s, 6.85, ly, 5.65, 2.55, 'trainable parms')
    text(s, 7.2, ly+0.62, 5.0, 1.7, big2(parm_lines), spacing=1.15)
    rt = rect(s, 0.85, 6.12, 11.65, 0.62, DARK, shape=MSO_SHAPE.ROUNDED_RECTANGLE); rt.adjustments[0] = 0.5
    text(s, 1.25, 6.245, 11, 0.4, [[('RUNNING TOTAL:  ', {'color': LGREY, 'size': 16}),
                                    (running, {'color': SOFT, 'bold': True, 'size': 18})]], size=16)
    if trap:
        tr = rect(s, 6.85, 2.62, 5.65, 0.56, GOLD, shape=MSO_SHAPE.ROUNDED_RECTANGLE); tr.adjustments[0] = 0.5
        text(s, 7.05, 2.72, 5.3, 0.4, trap, size=14, color=DARK, bold=True)
    footer(s, n)
    notes(s, note)
    return s

prs = new_prs()

s = title_slide(prs, 'OPIM 5509  -  Module 3.1', ['Math for a', 'Simple ConvNet'],
                'Rebuild model.summary() by hand  -  pairs with Simple_Size_and_Param.ipynb')
notes(s, 'Videos 4-6 of M3.1: Size & Trainable Parameters Pt 1-3.')

s = blank(prs); header(s, 'Module 3.1 - Size & Trainable Parameters', 'The mission')
cb = rect(s, 0.85, 2.05, 5.9, 4.35, DARK, shape=MSO_SHAPE.ROUNDED_RECTANGLE); cb.adjustments[0] = 0.04
text(s, 1.15, 2.25, 5.3, 0.35, 'THE CODE', size=13, color=SOFT, bold=True)
code_lines = [
    ('from tensorflow.keras import layers, models', 0),
    ('', 0),
    ('model = models.Sequential()', 0),
    ("model.add(layers.Conv2D(3, (5, 5), activation='relu',", 1),
    ('                        input_shape=(28, 28, 1)))', 1),
    ('model.add(layers.MaxPooling2D((2, 2)))', 0),
    ("model.add(layers.Conv2D(5, (3, 3), activation='relu'))", 1),
    ('model.add(layers.MaxPooling2D((2, 2)))', 0),
    ('model.add(layers.Flatten())', 0),
    ("model.add(layers.Dense(256, activation='relu'))", 1),
    ("model.add(layers.Dense(2, activation='softmax'))", 1),
    ('', 0),
    ('model.summary()', 0),
]
for k, (ln, hot) in enumerate(code_lines):
    text(s, 1.15, 2.62 + k*0.27, 5.5, 0.27, ln if ln else ' ', size=13,
         color=(SOFT if hot else RGBColor(0xD8, 0xDA, 0xE2)), font='Consolas')
card(s, 7.0, 2.05, 5.5, 4.35, 'what model.summary() will print')
rows2 = [('conv2d (Conv2D)', '(None, 24, 24, 3)', '78'),
         ('max_pooling2d', '(None, 12, 12, 3)', '0'),
         ('conv2d_1 (Conv2D)', '(None, 10, 10, 5)', '140'),
         ('max_pooling2d_1', '(None, 5, 5, 5)', '0'),
         ('flatten (Flatten)', '(None, 125)', '0'),
         ('dense (Dense)', '(None, 256)', '32,256'),
         ('dense_1 (Dense)', '(None, 2)', '514')]
for k, (a, b, c) in enumerate(rows2):
    yy = 2.62 + k*0.42
    text(s, 7.35, yy, 2.3, 0.35, a, size=13, color=INK, font='Consolas')
    text(s, 9.55, yy, 1.9, 0.35, b, size=13, color=GREY, font='Consolas')
    text(s, 11.55, yy, 0.8, 0.35, c, size=13, color=(GOLDD if c != '0' else GREY), bold=(c != '0'), font='Consolas', align=PP_ALIGN.RIGHT)
ln2 = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, IN(7.35), IN(5.62), IN(12.35), IN(5.62))
ln2.line.color.rgb = GOLDD; ln2.line.width = Pt(1.5); ln2.shadow.inherit = False
text(s, 7.35, 5.74, 3.4, 0.4, 'Total params:', size=15, color=INK, bold=True, font='Consolas')
text(s, 10.8, 5.72, 1.55, 0.42, '32,988', size=18, color=INK, bold=True, font='Consolas', align=PP_ALIGN.RIGHT)
text(s, 0.85, 6.62, 11.65, 0.4, [[('Given the code, produce the summary by hand - every shape, every count. ', {'bold': True, 'size': 15, 'color': INK}), ('That is mastery. That is also the exam.', {'size': 15, 'color': GOLDT, 'bold': True})]], size=15)
footer(s, 2); notes(s, 'Code <-> summary in both directions. NOTE: the second conv now makes FIVE maps - 3 in, 5 out, so nobody can confuse the two roles.')

s = blank(prs); header(s, 'Module 3.1 - Size & Trainable Parameters', 'Why ConvNets? Look at the parms')
card(s, 0.85, 2.3, 5.75, 3.4)
text(s, 1.2, 2.75, 5.0, 0.5, 'YOUR M2 MNIST DENSE NET', size=15, color=GOLDD, bold=True)
text(s, 1.2, 3.25, 5.0, 1.0, '~407,000', size=54, color=GREY, bold=True)
text(s, 1.2, 4.45, 5.0, 0.8, 'parameters - and it falls apart if the digit moves off-center', size=15, color=GREY)
card(s, 6.85, 2.3, 5.65, 3.4)
text(s, 7.2, 2.75, 5.0, 0.5, "TODAY'S CONVNET", size=15, color=GOLDD, bold=True)
text(s, 7.2, 3.25, 5.0, 1.0, '32,988', size=54, color=INK, bold=True)
text(s, 7.2, 4.45, 5.0, 0.8, 'parameters - 12x fewer, and it handles shifted/rotated images', size=15, color=INK)
text(s, 0.85, 6.1, 11.65, 0.6, 'Fewer parameters, better behavior. The rest of this deck shows exactly where 32,988 comes from.', size=17, color=GOLDT, bold=True)
footer(s, 3); notes(s, 'The hook: 407K vs 33K.')

s = blank(prs); header(s, 'Module 3.1 - Size & Trainable Parameters', 'The cast of characters')
rows = [('M, N', 'filter size (e.g. a 5 x 5 kernel)'),
        ('L', "channels coming INTO this layer - image: 1 BW / 3 RGB; deeper: the previous layer's F"),
        ('B', 'bias - always 1 PER FILTER'),
        ('F', 'feature maps this layer creates'),
        ('Stride', 'always 1 in our conv layers (so it never appears in the formulas)')]
for i, (a, b) in enumerate(rows):
    y = 2.2 + i*0.86
    bx = rect(s, 0.85, y, 1.7, 0.7, DARK, shape=MSO_SHAPE.ROUNDED_RECTANGLE); bx.adjustments[0] = 0.25
    text(s, 0.85, y+0.13, 1.7, 0.5, a, size=22, color=SOFT, bold=True, align=PP_ALIGN.CENTER)
    text(s, 2.85, y+0.14, 9.6, 0.6, b, size=17, color=INK)
tr = rect(s, 2.85, 6.28, 9.6, 0.55, GOLD, shape=MSO_SHAPE.ROUNDED_RECTANGLE); tr.adjustments[0] = 0.5
text(s, 3.1, 6.38, 9.2, 0.4, "The L is the trap: from layer 2 on, L = the previous layer's F. Not RGB!", size=15, color=DARK, bold=True)
footer(s, 4); notes(s, 'Same letters as the cheat sheet and the notebook. Drill L.')

s = blank(prs); header(s, 'Module 3.1 - Size & Trainable Parameters', 'Only two formulas to rule them all')
card(s, 0.85, 2.15, 11.65, 1.75, 'output size (conv, no padding)')
text(s, 1.2, 2.8, 11, 0.9, [[('new size = old size - (M - 1)', {'bold': True, 'size': 32, 'color': INK})],
                            [('shapes print as (BATCH, ROWS, COLS, CHANNELS) - batch is None until you fit; channels = that layer\'s F', {'size': 14, 'color': GREY})]], spacing=1.15)
card(s, 0.85, 4.15, 11.65, 1.75, 'trainable parameters')
text(s, 1.2, 4.8, 11, 0.9, [[('Conv2D: ((M x N x L) + B) x F      Dense: (n + 1) x m      Pool/Flatten: 0', {'bold': True, 'size': 23, 'color': INK})],
                            [('pooling is naive - just max values, nothing to learn', {'size': 14, 'color': GREY})]], spacing=1.2)
wk = rect(s, 0.85, 6.05, 11.65, 0.72, DARK, shape=MSO_SHAPE.ROUNDED_RECTANGLE); wk.adjustments[0] = 0.3
text(s, 1.2, 6.14, 11.1, 0.3, [[('WORKED:  ', {'bold': True, 'size': 13, 'color': SOFT}), ('28x28 image, 5x5 kernel, F=3  ->  size: 28-(5-1)=24 -> (None,24,24,3)  ·  parms: ((5x5x1)+1)x3 = 78', {'size': 13, 'color': RGBColor(0xD2,0xD4,0xDC)})]], size=13)
text(s, 1.2, 6.44, 11.1, 0.3, '"Size" = the rows/cols of the map. That little shrink IS the light downsampling. (Pooling is the aggressive kind: 24/2 = 12.)', size=13, color=SOFT, bold=True)
footer(s, 5); notes(s, 'Pt 1 anchor slide. Everything after is these two lines applied eight times.')

s = blank(prs); header(s, 'Module 3.1 - Size & Trainable Parameters', 'Reminder: what Conv2D is doing')
pic_fit(s, MM + r'\s07_img0.png', 0.85, 2.1, 11.6, 4.2)
text(s, 0.85, 6.4, 11.6, 0.5, 'Sliding kernel, stride 1, lots of overlap - the map shrinks a little. Light downsampling.', size=16, color=GREY)
footer(s, 6); notes(s, 'Quick recall, then we start counting.')

calc_slide(prs, 7, 0, 'Start here: the input image',
    ['Given in the code:', 'input_shape = (28, 28, 1)', '(None, 28, 28, 1)'],
    ['Nothing to learn yet...', '', '0 parms'],
    '0', 'One grayscale channel. Batch prints as None - decided at fit time.')

calc_slide(prs, 8, 1, 'Layer 1 - Conv2D: 3 maps @ 5x5',
    ['28 - (5 - 1)', '', '= 24   ->   (None, 24, 24, 3)'],
    ['((5 x 5 x 1) + 1) x 3', '', '= 78 parms'],
    '78', 'First conv: L=1 (grayscale). 25 weights + 1 bias per filter, 3 filters. Output channels = F = 3.')

calc_slide(prs, 9, 2, 'Layer 2 - MaxPooling 2x2',
    ['24 / 2', '', '= 12   ->   (None, 12, 12, 3)'],
    ['Nothing is learned - naive max', '', '0 parms'],
    '78', '2x2 kernel, stride 2, no overlap: halves it. Same 3 maps, just smaller.')

calc_slide(prs, 10, 3, 'Layer 3 - Conv2D: 5 maps @ 3x3',
    ['12 - (3 - 1)', '', '= 10   ->   (None, 10, 10, 5)'],
    ['((3 x 3 x 3) + 1) x 5', '', '= 140 parms'],
    '78 + 140 = 218',
    'THE TRAP SLIDE. L=3 because pooling handed us 3 maps; F=5 because WE asked for 5. Each filter is a 3x3x3 brick (27 weights + 1 bias = 28), x5 filters = 140. Three in, five out - the two numbers do different jobs!',
    trap='CAREFUL: L = 3 (maps coming IN), F = 5 (maps we MAKE)!')

calc_slide(prs, 11, 4, 'Layer 4 - MaxPooling 2x2',
    ['10 / 2', '', '= 5   ->   (None, 5, 5, 5)'],
    ['Still nothing to learn', '', '0 parms'],
    '218', 'Halve it again. Dense 5x5x5 nuggets of information now.')

calc_slide(prs, 12, 5, 'Layer 5 - Flatten',
    ['5 x 5 x 5', '', '= 125   ->   (None, 125)'],
    ['Just reshaping - no weights', '', '0 parms'],
    '218', 'Unroll the maps into one row of 125 numbers - like the first row of a dataframe. Ready for dense layers.')

calc_slide(prs, 13, 6, 'Layer 6 - Dense 256',
    ['256 hidden units', '', '(None, 256)'],
    ['(125 + 1) x 256', '', '= 32,256 parms'],
    '218 + 32,256 = 32,474', 'Module 2 formula, unchanged. This is where most of the parms live.')

calc_slide(prs, 14, 7, 'Layer 7 - Dense 2 (softmax)',
    ['2 output nodes', '', '(None, 2)'],
    ['(256 + 1) x 2', '', '= 514 parms'],
    '32,474 + 514 = 32,988', 'Binary classification, softmax over 2 nodes. Regression would be 1 node, linear.')

s = blank(prs); header(s, 'Module 3.1 - Size & Trainable Parameters', 'The whole chain - check the summary')
chain_strip(s, 7, y=2.3, small=False)
card(s, 0.85, 4.3, 11.65, 1.5)
text(s, 1.2, 4.6, 11, 0.9, [[('TOTAL  =  78 + 140 + 32,256 + 514  =  32,988', {'bold': True, 'size': 32, 'color': INK})],
                            [('exactly what model.summary() prints - run the notebook and check yourself', {'size': 15, 'color': GREY})]], spacing=1.2)
text(s, 0.85, 6.1, 11.65, 0.55, 'If your chain matches the summary shape-for-shape and parm-for-parm, you own this material.', size=17, color=GOLDT, bold=True)
footer(s, 15); notes(s, 'Pt 1 ends here. The chain IS the cheat-sheet answer table.')

s = blank(prs); header(s, 'Module 3.1 - Size & Trainable Parameters', 'Round 2: ugly numbers (no eyeballing!)')
rows2 = [('Conv2D 29 @ 5x5', '(None, 24, 24, 29)', '((5x5x1)+1) x 29  =  754'),
         ('MaxPool 2x2', '(None, 12, 12, 29)', '0'),
         ('Conv2D 87 @ 3x3', '(None, 10, 10, 87)', '((3x3x29)+1) x 87  =  22,794'),
         ('MaxPool 2x2 -> Flatten', '(None, 5, 5, 87) -> (None, 2175)', '0'),
         ('Dense 256 -> Dense 2', '(None, 256) -> (None, 2)', '(2175+1)x256 = 557,056  ·  (256+1)x2 = 514')]
for i, (a, b, c) in enumerate(rows2):
    y = 2.1 + i*0.86
    text(s, 0.85, y+0.12, 3.05, 0.6, a, size=15, color=INK, bold=True)
    text(s, 4.0, y+0.12, 3.55, 0.6, b, size=13.5, color=GREY)
    text(s, 7.7, y+0.12, 4.8, 0.6, c, size=14.5, color=INK)
    if i < 4:
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, IN(0.85), IN(y+0.78), IN(12.5), IN(y+0.78))
        ln.line.color.rgb = RGBColor(0xE0, 0xDE, 0xD6); ln.line.width = Pt(1); ln.shadow.inherit = False
tr = rect(s, 0.85, 6.28, 11.65, 0.55, GOLD, shape=MSO_SHAPE.ROUNDED_RECTANGLE); tr.adjustments[0] = 0.5
text(s, 1.1, 6.38, 11.2, 0.4, '29 maps and 87 filters exist so you CANNOT eyeball it - the formula is the only way through. Try before peeking!', size=15, color=DARK, bold=True)
footer(s, 16); notes(s, 'Pt 2: model 2 in the notebook. The calculator cell proves 22,794.')

s = blank(prs); header(s, 'Module 3.1 - Size & Trainable Parameters', 'Round 3: play with channels')
card(s, 0.85, 2.2, 5.75, 3.6, 'grayscale (L = 1)')
text(s, 1.2, 3.1, 5.0, 1.6, [[('((5 x 5 x 1) + 1) x 29', {'size': 24, 'color': GREY})], [('', {'size': 10})],
                             [('= 754 parms', {'bold': True, 'size': 34, 'color': INK})]], spacing=1.1)
card(s, 6.85, 2.2, 5.65, 3.6, 'now make it RGB (L = 3)')
text(s, 7.2, 3.1, 5.0, 1.6, [[('((5 x 5 x 3) + 1) x 29', {'size': 24, 'color': GREY})], [('', {'size': 10})],
                             [('= 2,204 parms', {'bold': True, 'size': 34, 'color': INK})]], spacing=1.1)
text(s, 0.85, 6.1, 11.65, 0.9, [[('PREDICT before you run the cell. ', {'bold': True, 'color': GOLDT, 'size': 18})],
                                [('Then grab the cheat sheet and do one full chain by hand - that is the whole assignment-prep loop.', {'size': 16, 'color': INK})]], spacing=1.15)
footer(s, 17); notes(s, 'Pt 3: change channels 1->3 in input_shape. Only the FIRST conv layer changes.')

s = blank(prs); header(s, 'Module 3.1 - Size & Trainable Parameters', 'Your toolkit')
tools = [('THE NOTEBOOK', 'Simple_Size_and_Param.ipynb', 'both models pre-built: run, then rebuild by hand'),
         ('THE CHEAT SHEET', 'ConvNet Math Cheat Sheet', 'every formula + a worked answer table'),
         ('THE PLAYGROUND', 'setosa.io/ev/image-kernels', 'drag kernel values, watch the image respond')]
for i, (a, b, c) in enumerate(tools):
    x = 0.85 + i*4.0
    card(s, x, 2.3, 3.7, 3.3, a)
    text(s, x+0.35, 3.1, 3.0, 0.9, b, size=18, color=INK, bold=True)
    text(s, x+0.35, 4.15, 3.0, 1.3, c, size=14, color=GREY)
text(s, 0.85, 6.0, 11.65, 0.6, 'All three are linked on the HuskyCT M3.1 page.', size=15, color=GREY)
footer(s, 18); notes(s, 'Wrap the recorded portion here.')

s = section_slide(prs, 'Appendix', 'Kernels in action: the gallery',
                  'Screenshots from setosa.io/ev/image-kernels: the same face through different kernels - watch the dot product panel build each output pixel.')
notes(s, 'Optional to record - flip through a couple of kernels and connect back to the setosa demo from video 1.')

for i, n in enumerate(range(17, 26)):
    s = blank(prs)
    pic_fit(s, MM + '\\s%02d_img0.png' % n, 0.4, 0.25, 12.5, 6.9)
    footer(s, 20+i)

s = blank(prs); header(s, 'Appendix', 'Good links (great reading, too)')
links = [('Visualizing ConvNets with Keras and cats', 'hackernoon.com/visualizing-parts-of-convolutional-neural-networks-using-keras-and-cats-5cc01b214e59'),
         ('Image kernels, explained visually', 'setosa.io/ev/image-kernels'),
         ('Easy-peasy 2D convolution (with video)', 'ricardodeazambuja.com - easy-peasy_conv_deep_learning_two'),
         ('Stanford CS231n ConvNet notes', 'cs231n.github.io/convolutional-networks'),
         ('The StackOverflow param-counting classic', 'stackoverflow.com/questions/42786717')]
for i, (a, b) in enumerate(links):
    y = 2.3 + i*0.85
    rect(s, 0.85, y+0.08, 0.14, 0.14, GOLD, shape=MSO_SHAPE.OVAL)
    text(s, 1.15, y-0.03, 11.3, 0.45, a, size=17, color=INK, bold=True)
    text(s, 1.15, y+0.36, 11.3, 0.4, b, size=13, color=GREY)
footer(s, 29); notes(s, 'All verified alive Sep 2026.')

prs.save(os.path.join(OUT, 'Math for a Simple ConvNet.pptx'))
print('MATH deck saved:', len(prs.slides._sldIdLst), 'slides')
