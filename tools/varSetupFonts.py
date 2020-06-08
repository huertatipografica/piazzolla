font = Glyphs.font
list = """A
Aacute
Adieresis
Atilde
B
C
Ccedilla
D
E
Eacute
F
G
H
I
Iacute
J
K
L
M
N
Ntilde
O
Oacute
Otilde
P
Q
R
S
T
U
Uacute
Udieresis
V
W
X
Y
Z
a
aacute
atilde
b
c
ccedilla
d
e
eacute
f
g
h
i
idotless
iacute
j
jdotless
k
l
m
n
ntilde
o
oacute
otilde
p
q
r
s
t
u
uacute
udieresis
v
w
x
y
z
fi
fl
zero
one
two
three
four
five
six
seven
eight
nine
period
comma
colon
semicolon
ellipsis
exclam
exclamdown
question
questiondown
periodcentered
bullet
asterisk
numbersign
slash
parenleft
parenright
hyphen
endash
emdash
underscore
quotesinglbase
quotedblleft
quotedblright
quoteleft
quoteright
guilsinglleft
guilsinglright
space
cent
dollar
sterling
plus
multiply
divide
equal
at
ampersand
dieresiscomb
dotaccentcomb
acutecomb
tildecomb
cedillacomb
a.sc
aacute.sc
atilde.sc
b.sc
c.sc
ccedilla.sc
d.sc
e.sc
eacute.sc
f.sc
g.sc
h.sc
i.sc
idotless.sc
iacute.sc
j.sc
k.sc
l.sc
m.sc
n.sc
ntilde.sc
o.sc
oacute.sc
otilde.sc
p.sc
q.sc
r.sc
s.sc
t.sc
u.sc
uacute.sc
udieresis.sc
v.sc
w.sc
x.sc
y.sc
z.sc
Oslash.rl-Weight_118_208
oslash.rl-Weight_118_208
oslash.sc.rl-Weight_118_208
cent.rl-Weight_118_208
dollar.rl-Weight_118_208
Oslash
oslash
oslash.sc
"""
charset = list.splitlines()
deletableGlyphs = [g.name for g in font.glyphs if g.name not in charset]

font.disableUpdateInterface()

#decompose ligatures
for layer in font.glyphs['fi'].layers:
    layer.decomposeComponents()

for layer in font.glyphs['fl'].layers:
    layer.decomposeComponents()

# remove
for glyph in deletableGlyphs:
    del(font.glyphs[glyph])

#reset features
features = [t.name for t in font.features]
for f in features:
    del(font.features[f])

featurePrefixes = [t.name for t in font.featurePrefixes]
for f in featurePrefixes:
    del(font.featurePrefixes[f])

classes = [t.name for t in font.classes]
for f in classes:
    del(font.classes[f])

font.updateFeatures()

font.enableUpdateInterface()

Glyphs.showNotification('Setup fonts', 'The setup fonts have been done, saved and closed')
font.save(font.filepath.replace('.glyphs', '-VARsetup.glyphs'))
font.close()