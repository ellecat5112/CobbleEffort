"""
Shared toolkit for the Five Nights at Freddy's collection: Pokémon re-made as pizzeria animatronics.

Common pieces: felt "costume" fur, stitched seams, rivets, grime, torn patches showing the metal endoskeleton and
wires, square animatronic teeth, and eyes that glow in the dark (an extra emissive layer: pinprick pupils).

Looks, one per game:
  classic     FNAF 1: worn felt costume, seams, teeth, white pinprick pupils
  withered    FNAF 2: faded, filthy, torn open to the endoskeleton
  toy         FNAF 2: glossy plastic, brighter colours, rosy cheeks, shiny eyes
  springtrap  FNAF 3: rotten olive-yellow suit, stains, dangling wires
  nightmare   FNAF 4: near-black, jagged tears lined with teeth, red pinprick eyes
  funtime     FNAF 5: white glossy plating with pink/purple panels, faceplate seams, rosy cheeks
  scrap       FNAF 6: rusted, patched with mismatched panels, burns and wires
plus the three named characters: freddy, chica, foxy.
"""
from __future__ import annotations

import colorsys
import math
import random

from PIL import Image

from ._festive import digest
from ._horror import components, find_eye_mask, mix, value_noise

METAL = (124, 128, 136)
METAL_DK = (70, 73, 80)
METAL_HI = (176, 180, 188)
TORN = (34, 22, 16)
WIRE = [(200, 40, 40), (50, 90, 210), (220, 190, 40), (40, 160, 70)]
TOOTH = (238, 234, 220)
TOOTH_GAP = (40, 30, 26)
SOCKET = (8, 6, 6)
CHEEK = (240, 120, 150)
WHITE_PLATE = (244, 242, 246)

LOOKS = ("classic", "withered", "toy", "springtrap", "nightmare", "funtime", "scrap")

EYESHINE = {"name": "eyeshine", "emissive": True, "translucent": True}


# ---------------------------------------------------------------------------------------------
# face finding: Cobblemon's alpha-eyes mask tells us where the eyes are; the chin is found by
# walking down the face from between the eyes until the painted area ends.
# ---------------------------------------------------------------------------------------------

def scaled(rect, hints, w, h):
    """A geometry-hint rectangle (geo UV units) scaled to this texture's pixels."""
    if not rect or not hints:
        return None
    tw, th = hints["tex_size"]
    sx, sy = w / tw, h / th
    x, y, rw, rh = rect
    return (int(x * sx), int(y * sy), max(1, int(rw * sx)), max(1, int(rh * sy)))


class Face:
    """Where to draw face details. Best source: the head's front face from the model (geometry hints).
    Fallback: guess from the eye pixels (only works when eyes are painted on the face itself)."""

    def __init__(self, eye_mask, alpha, w, h, hints=None):
        self.eyes = components([(x, y) for y in range(h) for x in range(w) if eye_mask[y][x]])
        self.pair = sorted(self.eyes, key=len, reverse=True)[:2]
        self.ok = False
        self.top = scaled(hints and hints.get("head_top"), hints, w, h)
        self.torso = scaled(hints and hints.get("torso_front"), hints, w, h)
        front = scaled(hints and hints.get("head_front"), hints, w, h)
        if front and front[3] >= 4 and front[2] >= 4:
            x0, y0, fw, fh = front
            self.front = front
            self.cx = x0 + fw // 2
            self.crown = y0
            self.eye_top = y0 + int(fh * 0.25)
            self.eye_bottom = y0 + int(fh * 0.5)
            self.chin = y0 + fh - 1
            self.span = max(4, int(fw * 0.5))
            self.ok = True
            return
        self.front = None
        if not self.eyes:
            return
        pair = self.pair
        xs = [p[0] for g in pair for p in g]
        ys = [p[1] for g in pair for p in g]
        self.cx = (min(xs) + max(xs)) // 2
        self.eye_top, self.eye_bottom = min(ys), max(ys)
        self.span = max(xs) - min(xs) + 1
        y = self.eye_bottom + 1
        while y < h and alpha[y][self.cx]:
            y += 1
        self.chin = y - 1
        y = self.eye_top - 1
        while y >= 0 and alpha[y][self.cx]:
            y -= 1
        self.crown = y + 1
        self.ok = self.chin - self.eye_bottom >= 2


def put(px, alpha, x, y, c):
    if 0 <= y < len(alpha) and 0 <= x < len(alpha[0]) and alpha[y][x]:
        px[x, y] = tuple(int(v) for v in c[:3]) + (alpha[y][x],)


def felt(c, x, y, rng, strength=0.07):
    """Felt costume fur: soft vertical fibres plus fine speckle."""
    f = 1 + math.sin(x * 2.3 + (y // 3) * 0.7) * strength * 0.6 + rng.uniform(-strength, strength)
    return tuple(max(0, min(255, int(v * f))) for v in c)


def seams(px, alpha, eye, w, h, scale, colour_fn):
    """Dashed stitching just inside the edge of every painted area."""
    def opaque(x, y):
        return 0 <= x < w and 0 <= y < h and alpha[y][x]
    for y in range(h):
        for x in range(w):
            if not alpha[y][x] or eye[y][x]:
                continue
            inner = all(opaque(x + dx * scale, y + dy * scale) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            near = not all(opaque(x + dx * 2 * scale, y + dy * 2 * scale) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if inner and near and ((x + y) // scale) % 3 == 0:
                put(px, alpha, x, y, colour_fn(px[x, y][:3]))


def rivets(px, alpha, eye, w, h, rng, scale, count):
    for _ in range(count):
        x, y = rng.randrange(w), rng.randrange(h)
        if alpha[y][x] and not eye[y][x]:
            for sy in range(scale):
                for sx in range(scale):
                    put(px, alpha, x + sx, y + sy, METAL_HI if sx == sy == 0 else METAL)


def grime(px, alpha, w, h, rng, scale, amount):
    stain = value_noise(w, h, max(3, 5 * scale), rng)
    for y in range(h):
        for x in range(w):
            if alpha[y][x] and stain[y][x] > 1 - amount:
                put(px, alpha, x, y, mix(px[x, y][:3], (40, 30, 18), (stain[y][x] - (1 - amount)) * 2))


def endoskeleton(px, alpha, eye, w, h, rng, scale, count, used, teeth=False):
    """Torn patches in the costume, showing the metal endoskeleton and coloured wires behind."""
    for _ in range(count):
        rw, rh = rng.randint(4, 8) * scale, rng.randint(3, 6) * scale
        for _ in range(80):
            x0, y0 = rng.randrange(1, max(2, w - rw - 1)), rng.randrange(1, max(2, h - rh - 1))
            cells = [(x, y) for y in range(y0, y0 + rh) for x in range(x0, x0 + rw)]
            if all(alpha[y][x] and not eye[y][x] and not used[y][x] for x, y in cells):
                break
        else:
            continue
        cx, cy = x0 + rw / 2, y0 + rh / 2
        bar = rng.randrange(y0 + scale, y0 + rh - scale) if rh > 2 * scale else y0
        wire = rng.choice(WIRE)
        for x, y in cells:
            d = ((x - cx) / (rw / 2)) ** 2 + ((y - cy) / (rh / 2)) ** 2 + rng.uniform(-0.3, 0.3)
            if d > 1.0:
                continue
            used[y][x] = True
            if d > 0.75:
                c = TORN                                     # ragged torn fabric edge
            elif teeth and d > 0.5:
                c = TOOTH if (x // scale) % 2 == 0 else TOOTH_GAP   # nightmare tears are lined with teeth
            elif abs(y - bar) < scale:
                c = METAL_HI                                 # an endoskeleton strut
            elif (x + 2 * y) % (5 * scale) < scale:
                c = wire                                     # wires
            else:
                c = METAL_DK if (x + y) % 2 else METAL
            put(px, alpha, x, y, c)


def teeth(px, alpha, face, scale, rows=2, sharp=False):
    """The animatronic grin: rows of square (or sharp) teeth between the eyes and the chin."""
    if not face.ok:
        return
    mouth = face.eye_bottom + max(scale, int((face.chin - face.eye_bottom) * 0.55))
    half = max(2 * scale, face.span // 2)
    for x in range(face.cx - half, face.cx + half + 1):
        k = (x - (face.cx - half)) // scale
        for r in range(rows):
            for dy in range(scale):
                y = mouth + (r * (scale + 1) if r else 0) + dy - (scale if r == 0 else 0)
                if sharp:
                    col = TOOTH if (k % 2 == 0 and dy < scale) else TOOTH_GAP
                else:
                    col = TOOTH if ((x - face.cx) % (2 * scale)) < 2 * scale - 1 else TOOTH_GAP
                put(px, alpha, x, y, col)
        put(px, alpha, x, mouth + (scale if rows > 1 else 0) - (0 if rows > 1 else scale), TOOTH_GAP)


def cheeks(px, alpha, face, scale, colour=CHEEK):
    if not face.ok:
        return
    spots = [(face.cx + d * face.span // 2, face.eye_bottom + scale) for d in (-1, 1)] if face.front else \
            [(sum(p[0] for p in g) // len(g), face.eye_bottom + 2 * scale) for g in face.pair]
    for gx, y in spots:
        for dy in range(scale):
            for dx in range(-scale, scale + 1):
                put(px, alpha, gx + dx, y + dy, colour)


def eyes(px, alpha, face, scale, iris, socket=SOCKET, glint=False):
    """Black sockets with a single glowing pupil each; returns the pupil cells for the eyeshine layer."""
    pupils = []
    for g in face.eyes:
        for x, y in g:
            put(px, alpha, x, y, socket)
        cx = sorted(p[0] for p in g)[len(g) // 2]
        cy = sorted(p[1] for p in g)[len(g) // 2]
        cells = set(g)
        for sy in range(scale):
            for sx in range(scale):
                if (cx + sx, cy + sy) in cells and iris is not None:
                    put(px, alpha, cx + sx, cy + sy, iris)
                    pupils.append((cx + sx, cy + sy, iris))
        if glint and (cx - scale, cy - scale) in cells:
            put(px, alpha, cx - scale, cy - scale, (255, 255, 255))
    return pupils


def shine_layer(size, pupils):
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    o = out.load()
    for x, y, c in pupils:
        o[x, y] = tuple(c[:3]) + (255,)
    return out


# ---------------------------------------------------------------------------------------------
# colour schemes
# ---------------------------------------------------------------------------------------------

def hls(c):
    return colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255)


def from_hls(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h % 1.0, max(0.0, min(1.0, l)), max(0.0, min(1.0, s)))
    return (int(r * 255), int(g * 255), int(b * 255))


def ramp(stops, v):
    v = max(0.0, min(1.0, v))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if v <= p1:
            return mix(c0, c1, (v - p0) / (p1 - p0))
    return stops[-1][1]


def recolour(look, c, shiny):
    h, l, s = hls(c)
    if look == "classic":
        return from_hls(h, l * 0.95, s * 0.85)
    if look == "withered":
        return from_hls(h, l * 0.75, s * 0.5)
    if look == "toy":
        return from_hls(h, min(0.85, l * 1.05 + 0.08), min(1.0, s * 1.3 + 0.1))
    if look == "springtrap":
        return from_hls(0.16 + (h - 0.16) * 0.15, l * 0.7 + 0.05, 0.35 * (0.6 + s))
    if look == "nightmare":
        return from_hls(h, l * 0.45, s * 0.7)
    if look == "funtime":
        if s < 0.25 or l > 0.7:
            return mix(WHITE_PLATE, (190, 186, 200), max(0.0, 0.7 - l))
        return from_hls(0.9 if h < 0.5 else 0.8, 0.62, 0.75)      # pinks and purples
    if look == "scrap":
        return mix(from_hls(h, l * 0.8, s * 0.6), (122, 66, 30), 0.4)
    return c


def shiny_shift(c):
    """Shiny for the generic looks: a 'Golden' animatronic, like Golden Freddy."""
    h, l, s = hls(c)
    return from_hls(0.12, l * 0.9 + 0.08, 0.55)


# ---------------------------------------------------------------------------------------------
# the style factory
# ---------------------------------------------------------------------------------------------

_cache: dict = {}


def plan(look, base, eyes_img, seed, shiny, hints=None):
    key = (look, digest(base), digest(eyes_img), seed, shiny, repr(hints))
    if key in _cache:
        return _cache[key]
    _cache.clear()
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)
    alpha = [[src[x, y][3] for x in range(w)] for y in range(h)]
    eye_mask = find_eye_mask(base, eyes_img)
    face = Face(eye_mask, alpha, w, h, hints)
    img = Image.new("RGBA", (w, h))
    px = img.load()
    used = [[False] * w for _ in range(h)]
    memo = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            if (r, g, b) not in memo:
                c = CHARACTER[look](r, g, b, shiny) if look in CHARACTER else recolour(look, (r, g, b), shiny)
                if shiny and look not in CHARACTER:
                    c = shiny_shift(c)
                memo[(r, g, b)] = c
            c = memo[(r, g, b)]
            if look not in ("toy", "funtime"):
                c = felt(c, x, y, rng)
            px[x, y] = tuple(c) + (a,)
    units = max(1, (w * h) // (64 * 64 * scale * scale))
    seam_dark = lambda c: mix(c, (20, 14, 10), 0.45)
    pupils = []

    if look in ("toy", "funtime"):
        # glossy plastic: a bright highlight along the top edge of each painted area
        for y in range(1, h):
            for x in range(w):
                if alpha[y][x] and not alpha[y - 1][x] and not eye_mask[y][x]:
                    put(px, alpha, x, y, mix(px[x, y][:3], (255, 255, 255), 0.55))
        if look == "funtime":
            for y in range(h):
                for x in range(w):
                    if alpha[y][x] and not eye_mask[y][x] and (x % (8 * scale) == 0 or y % (8 * scale) == 0):
                        put(px, alpha, x, y, mix(px[x, y][:3], (90, 86, 100), 0.5))   # faceplate panel lines
        cheeks(px, alpha, face, scale)
        pupils = eyes(px, alpha, face, scale, (120, 200, 255) if look == "toy" else (230, 120, 255), glint=True)
        teeth(px, alpha, face, scale, rows=1)
    elif look in CHARACTER:
        pupils = CHARACTER_DETAIL[look](px, alpha, eye_mask, face, w, h, rng, scale, units, used, shiny)
    else:
        seams(px, alpha, eye_mask, w, h, scale, seam_dark)
        rivets(px, alpha, eye_mask, w, h, rng, scale, 3 * units)
        if look == "classic":
            grime(px, alpha, w, h, rng, scale, 0.15)
            teeth(px, alpha, face, scale)
            pupils = eyes(px, alpha, face, scale, (255, 255, 255))
        elif look == "withered":
            grime(px, alpha, w, h, rng, scale, 0.35)
            endoskeleton(px, alpha, eye_mask, w, h, rng, scale, 3 * units, used)
            teeth(px, alpha, face, scale)
            pupils = eyes(px, alpha, face, scale, (255, 255, 255))[:1]   # one eye has gone dark
        elif look == "springtrap":
            grime(px, alpha, w, h, rng, scale, 0.4)
            endoskeleton(px, alpha, eye_mask, w, h, rng, scale, 2 * units, used)
            teeth(px, alpha, face, scale)
            pupils = eyes(px, alpha, face, scale, (230, 230, 210))
        elif look == "nightmare":
            endoskeleton(px, alpha, eye_mask, w, h, rng, scale, 3 * units, used, teeth=True)
            teeth(px, alpha, face, scale, rows=2, sharp=True)
            pupils = eyes(px, alpha, face, scale, (255, 40, 40))
        elif look == "scrap":
            grime(px, alpha, w, h, rng, scale, 0.3)
            for _ in range(4 * units):     # mismatched patch panels, stitched on
                pw, ph = rng.randint(3, 6) * scale, rng.randint(3, 5) * scale
                x0, y0 = rng.randrange(max(1, w - pw)), rng.randrange(max(1, h - ph))
                col = rng.choice([METAL, (150, 110, 60), (90, 120, 150), (140, 60, 60)])
                for y in range(y0, y0 + ph):
                    for x in range(x0, x0 + pw):
                        if alpha[y][x] and not eye_mask[y][x] and not used[y][x]:
                            edge = x in (x0, x0 + pw - 1) or y in (y0, y0 + ph - 1)
                            put(px, alpha, x, y, (40, 30, 24) if edge and (x + y) % 2 else felt(col, x, y, rng))
            endoskeleton(px, alpha, eye_mask, w, h, rng, scale, 2 * units, used)
            teeth(px, alpha, face, scale)
            pupils = eyes(px, alpha, face, scale, (255, 220, 120))[:1]
    _cache[key] = (img, pupils)
    return _cache[key]


# ---------------------------------------------------------------------------------------------
# the three classic characters
# ---------------------------------------------------------------------------------------------

FREDDY = [(0.0, (46, 26, 14)), (0.5, (110, 66, 34)), (1.0, (158, 104, 60))]
FREDDY_MUZZLE = [(0.0, (150, 112, 74)), (1.0, (222, 186, 140))]
GOLDEN = [(0.0, (90, 66, 14)), (0.5, (186, 146, 42)), (1.0, (236, 204, 96))]
CHICA = [(0.0, (150, 112, 10)), (0.5, (240, 200, 40)), (1.0, (255, 236, 130))]
CHICA_ORANGE = [(0.0, (170, 70, 10)), (1.0, (250, 150, 40))]
TOY_CHICA = [(0.0, (200, 150, 20)), (0.5, (255, 214, 60)), (1.0, (255, 245, 170))]
FOXY = [(0.0, (60, 18, 10)), (0.5, (150, 54, 32)), (1.0, (200, 96, 60))]
FOXY_TAN = [(0.0, (150, 110, 70)), (1.0, (226, 194, 150))]
MANGLE = [(0.0, (190, 180, 190)), (1.0, (252, 250, 252))]
MANGLE_PINK = [(0.0, (200, 60, 120)), (1.0, (255, 150, 200))]


def freddy_colour(r, g, b, shiny):
    h, l, s = hls((r, g, b))
    if l > 0.72 and 0.05 <= h <= 0.17:            # cream muzzle / crescent / belly (not the fur's light speckles)
        return ramp(GOLDEN if shiny else FREDDY_MUZZLE, l * 1.2 - 0.3)
    return ramp(GOLDEN if shiny else FREDDY, l * 1.25)


def chica_colour(r, g, b, shiny):
    h, l, s = hls((r, g, b))
    body = TOY_CHICA if shiny else CHICA
    if s > 0.3 and (h < 0.105 or h > 0.93) and l < 0.75:      # reds / oranges -> Chica yellow
        return ramp(body, l * 1.3)
    if s > 0.3 and 0.105 <= h < 0.2:                          # yellows -> orange beak, feet
        return ramp(CHICA_ORANGE, l)
    if l > 0.6:                                               # creams -> bib white
        return (246, 244, 236)
    return ramp(body, l * 1.4)


def foxy_colour(r, g, b, shiny):
    h, l, s = hls((r, g, b))
    if l < 0.22:                                              # black stripes / dark parts
        return (70, 64, 66) if shiny else (52, 26, 16)
    if l > 0.8 and s < 0.6:                                   # only the palest parts stay tan (muzzle, belly)
        return ramp(MANGLE if shiny else FOXY_TAN, l)
    if 0.85 < h or h < 0.02:                                  # pinks / reds (Krookodile) -> rust
        return ramp(MANGLE_PINK if shiny else FOXY, l * 1.3)
    return ramp(MANGLE_PINK if shiny else FOXY, l * 1.15)


def freddy_detail(px, alpha, eye_mask, face, w, h, rng, scale, units, used, shiny):
    seams(px, alpha, eye_mask, w, h, scale, lambda c: mix(c, (20, 12, 6), 0.45))
    if face.ok:
        half = max(3 * scale, int(face.span * 0.7))
        # top hat: the head's top face goes black (a smaller square on top, like the crown of the hat),
        # and the top rows of the face become the hat's brim
        if face.top:
            tx, ty, tw_, th_ = face.top
            for y in range(ty, ty + th_):
                for x in range(tx, tx + tw_):
                    inner = tw_ // 4 <= x - tx < tw_ - tw_ // 4 and th_ // 4 <= y - ty < th_ - th_ // 4
                    put(px, alpha, x, y, (14, 12, 14) if inner else (34, 30, 34))
        else:
            for y in range(max(0, face.crown - 6 * scale), face.crown):
                for x in range(face.cx - half, face.cx + half + 1):
                    put(px, alpha, x, y, (20, 18, 20))
        for y in range(face.crown, face.crown + scale):
            for x in range(face.cx - half, face.cx + half + 1):
                put(px, alpha, x, y, (40, 36, 40))
        # bow tie under the chin
        by = face.chin - scale
        for dy in range(-scale, scale + 1):
            for dx in range(-3 * scale, 3 * scale + 1):
                if abs(dx) >= abs(dy) or abs(dx) <= scale // 2:
                    put(px, alpha, face.cx + dx, by + dy, (16, 14, 16))
    teeth(px, alpha, face, scale)
    if shiny:   # Golden Freddy: empty black sockets, the faintest white pinpricks
        return eyes(px, alpha, face, scale, (255, 255, 255))
    return eyes(px, alpha, face, scale, (70, 150, 255), glint=True)   # Freddy's blue eyes


def chica_detail(px, alpha, eye_mask, face, w, h, rng, scale, units, used, shiny):
    seams(px, alpha, eye_mask, w, h, scale, lambda c: mix(c, (60, 40, 0), 0.4))
    if face.ok:
        # the "LET'S EAT!!!" bib: white, with rows of tiny coloured letters
        if face.torso and face.torso[3] >= 6:
            bx, by, bw, bh = face.torso
            top, cx, half, rows = by + scale, bx + bw // 2, max(2 * scale, int(bw * 0.4)), min(6 * scale, bh - 2)
        else:
            top = face.eye_bottom + max(2 * scale, int((face.chin - face.eye_bottom) * 0.75))
            cx, half, rows = face.cx, max(3 * scale, face.span), 6 * scale
        letters = [(240, 60, 60), (60, 160, 240), (240, 160, 30), (120, 200, 60), (190, 80, 220)]
        for y in range(top, top + rows):
            for x in range(cx - half, cx + half + 1):
                if not (0 <= y < h and 0 <= x < w and alpha[y][x]):
                    continue
                row = (y - top) // scale
                if row in (1, 3) and ((x - cx) // scale) % 2 == 0:
                    put(px, alpha, x, y, letters[((x - cx) // scale + row) % len(letters)])
                else:
                    put(px, alpha, x, y, (248, 246, 240) if row < 5 else (210, 206, 200))
        if shiny:
            cheeks(px, alpha, face, scale)
    teeth(px, alpha, face, scale)
    return eyes(px, alpha, face, scale, (200, 90, 255), glint=True)    # Chica's violet eyes


def foxy_detail(px, alpha, eye_mask, face, w, h, rng, scale, units, used, shiny):
    seams(px, alpha, eye_mask, w, h, scale, lambda c: mix(c, (20, 8, 4), 0.45))
    rivets(px, alpha, eye_mask, w, h, rng, scale, 2 * units)
    endoskeleton(px, alpha, eye_mask, w, h, rng, scale, (4 if not shiny else 3) * units, used)
    teeth(px, alpha, face, scale, rows=2, sharp=True)
    pupils = eyes(px, alpha, face, scale, (255, 210, 40), glint=True)   # Foxy's amber eyes
    if face.ok and len(face.pair) >= 1 and not shiny:
        # the eye patch over one eye, with its strap running across the head
        patched = face.pair[0]
        cells = set(patched)
        gy = face.eye_top + scale if face.front else sum(p[1] for p in patched) // len(patched)
        px0 = min(p[0] for p in patched) - scale
        px1 = max(p[0] for p in patched) + scale
        for y in range(min(p[1] for p in patched) - scale, max(p[1] for p in patched) + scale + 1):
            for x in range(px0, px1 + 1):
                put(px, alpha, x, y, (12, 10, 10))
        if face.front:   # the strap runs across the face and round the sides of the head
            x = face.cx
            while x > 0 and alpha[gy][x - 1]:
                x -= 1
            while x < w and alpha[gy][x]:
                put(px, alpha, x, gy, (24, 20, 20))
                x += 1
        pupils = [p for p in pupils if (p[0], p[1]) not in cells]
    return pupils


CHARACTER = {"freddy": freddy_colour, "chica": chica_colour, "foxy": foxy_colour}
CHARACTER_DETAIL = {"freddy": freddy_detail, "chica": chica_detail, "foxy": foxy_detail}


def make(look):
    """Build the style functions for one look (used by the thin fnaf_<look>.py modules)."""
    def retexture(base, eyes_img, seed, shiny, frame: int = 0, layer=False, hints=None):
        if layer:
            return base.convert("RGBA").copy()      # existing glow / extra layers keep their look
        return plan(look, base, eyes_img, seed, shiny, hints)[0].copy()

    def extra_layer(name, base, eyes_img, seed, shiny, frame, hints=None):
        img, pupils = plan(look, base, eyes_img, seed, shiny, hints)
        return shine_layer(img.size, pupils) if pupils else None

    return retexture, extra_layer
