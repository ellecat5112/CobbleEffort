"""The Digimon detail library (CobbleEffort: Digital, the user's call: much more detailed models): shaders that give
hand-built box models a painted finish. Bevels make blocks read rounded, materials carry gentle tonal variation, and
anatomy, armour and surface detail are drawn in model space so they line up across neighbouring boxes.

Every shader factory takes a palette function P(variant) -> {key: colour} (see _route.pal for shiny palettes) and
returns a shader(x, y, z, face, variant, box=..., **k) -> (rgba, glow or None) for _boxmodel.Model.box().

Pieces:
  local(), edge_t(), bevel()          face-local coordinates and edge treatment
  noise2/noise3/fbm                   smooth deterministic noise (tonal variation; no per-texel speckle)
  Bulge / muscles()                   anatomy: rounded masses lit from above, dark grooves between them
  veins()                             raised branching veins with a lit edge
  skin, scales, fur, feathers, armour, metal, fabric, leather, gem, solid   materials
  eye()                               iris rings, pupil, two glints, lid line
"""
from __future__ import annotations

import math
from functools import lru_cache

from _route import tone


# ---- coordinates ----------------------------------------------------------------------------------------------------

def local(x, y, z, face, box):
    """Position on the face: (u, v, W, H) in model units, v up (or toward -z on up/down faces)."""
    lo, sz = box.lo, box.size
    if face in ("north", "south"):
        return x - lo[0], y - lo[1], sz[0], sz[1]
    if face in ("east", "west"):
        return z - lo[2], y - lo[1], sz[2], sz[1]
    return x - lo[0], z - lo[2], sz[0], sz[2]


def plane(x, y, z, face):
    """Two world-space coordinates across the face, continuous between boxes facing the same way."""
    return {"up": (x, z), "down": (x, z), "north": (x, y), "south": (-x, y), "east": (z, y), "west": (-z, y)}[face]


def edge_t(u, v, W, H, width):
    """0 on the face's border, 1 at `width` units in."""
    d = min(u, W - u, v, H - v)
    return max(0.0, min(1.0, d / max(width, 1e-6)))


def bevel(u, v, W, H, face, width=0.45, amount=0.16):
    """Edge light: a dark rim on the sides and bottom of each face, a lit rim along its top edge."""
    if W < 0.9 or H < 0.9:
        return 1.0
    t = edge_t(u, v, W, H, width)
    if t >= 1:
        return 1.0
    top = face not in ("up", "down") and H - v < width
    return 1.0 + amount * 0.7 * (1 - t) if top else 1.0 - amount * (1 - t)


# ---- noise ----------------------------------------------------------------------------------------------------------

def _h(i, j, k=0, seed=0):
    n = math.sin(i * 127.1 + j * 311.7 + k * 74.7 + seed * 19.19) * 43758.5453
    return n - math.floor(n)


def _s(t):
    return t * t * (3 - 2 * t)


def noise2(a, b, seed=0):
    i, j = math.floor(a), math.floor(b)
    fa, fb = _s(a - i), _s(b - j)
    v00, v10, v01, v11 = _h(i, j, 0, seed), _h(i + 1, j, 0, seed), _h(i, j + 1, 0, seed), _h(i + 1, j + 1, 0, seed)
    return (v00 * (1 - fa) + v10 * fa) * (1 - fb) + (v01 * (1 - fa) + v11 * fa) * fb


def noise3(x, y, z, seed=0):
    i, j, k = math.floor(x), math.floor(y), math.floor(z)
    fx, fy, fz = _s(x - i), _s(y - j), _s(z - k)
    out = 0.0
    for di in (0, 1):
        for dj in (0, 1):
            for dk in (0, 1):
                w = (fx if di else 1 - fx) * (fy if dj else 1 - fy) * (fz if dk else 1 - fz)
                out += w * _h(i + di, j + dj, k + dk, seed)
    return out


def fbm(x, y, z, seed=0, octaves=3):
    v, a, f = 0.0, 0.5, 1.0
    for o in range(octaves):
        v += a * noise3(x * f, y * f, z * f, seed + o)
        a *= 0.5
        f *= 2.0
    return v / (1 - 0.5 ** octaves)


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    out = tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))
    return out + ((a[3],) if len(a) == 4 else ())


def mul(c, f):
    out = tuple(max(0, min(255, int(round(ch * f)))) for ch in c[:3])
    return out + ((c[3],) if len(c) == 4 else ())


def _finish(col, face, f=1.0):
    if len(col) == 4 and col[3] < 255:
        return mul(col, f)
    return tone(mul(col, f), face)


# ---- anatomy --------------------------------------------------------------------------------------------------------

class Bulge:
    """A rounded mass on a face plane (`face` direction, centre (cu, cv), radii (ru, rv) in plane() coordinates):
    lit toward its top, shadowed toward its lower rim, with a dark groove round its edge."""

    def __init__(self, face, cu, cv, ru, rv, groove=0.22, light=0.14, shadow=0.22, tilt=0.0):
        self.face, self.cu, self.cv, self.ru, self.rv = face, cu, cv, ru, rv
        self.groove, self.light, self.shadow, self.tilt = groove, light, shadow, tilt

    def at(self, face, a, b):
        if face != self.face:
            return None
        du, dv = (a - self.cu) / self.ru, (b - self.cv) / self.rv
        if self.tilt:
            c, s = math.cos(self.tilt), math.sin(self.tilt)
            du, dv = du * c - dv * s, du * s + dv * c
        d = math.hypot(du, dv)
        if d > 1.0 + self.groove:
            return None
        if d > 1.0:
            return 1.0 - 0.5 * (1 - (d - 1.0) / self.groove)             # the groove between masses
        return 1.0 + self.light * max(0.0, dv) * (1 - d) - self.shadow * max(0.0, -dv) * d ** 1.5


def muscles(bulges, a, b, face):
    """Combined shading factor from a list of Bulges (1.0 where none applies)."""
    f = 1.0
    for bu in bulges:
        r = bu.at(face, a, b)
        if r is not None:
            f *= r
    return f


def torso_bulges(cx, top, width, face="north", abs_rows=3, lean=0.0):
    """Pectorals and a six- (or eight-) pack on a front plane: chest top at y=top, half-width `width`."""
    out = []
    pw = width * 0.48
    for s in (-1, 1):
        out.append(Bulge(face, cx + s * width * 0.48, top - width * 0.42, pw, width * 0.36, groove=0.18,
                         light=0.3, shadow=0.42, tilt=s * 0.25))
    row_h = width * 0.30
    y = top - width * 0.95 - row_h * 0.5
    for r in range(abs_rows):
        for s in (-1, 1):
            out.append(Bulge(face, cx + s * width * 0.24, y - r * row_h * 1.05, width * 0.21, row_h * 0.46,
                             groove=0.35, light=0.32, shadow=0.4))
    for s in (-1, 1):                                           # obliques
        out.append(Bulge(face, cx + s * width * 0.78, top - width * 1.55, width * 0.2, width * 0.55, groove=0.2,
                         light=0.08, shadow=0.2, tilt=-s * 0.35))
    return out


# ---- veins ----------------------------------------------------------------------------------------------------------

@lru_cache(maxsize=256)
def _vein_paths(seed, u0, v0, u1, v1, count):
    """Branching random walks inside a plane rectangle: lists of segments ((a, b), (a2, b2))."""
    segs = []
    for n in range(count):
        a = u0 + (u1 - u0) * _h(n, 1, 0, seed)
        b = v0 + (v1 - v0) * _h(n, 2, 0, seed)
        ang = math.pi * (0.35 + 0.3 * _h(n, 3, 0, seed)) * (1 if _h(n, 4, 0, seed) > 0.5 else -1)
        stack = [(a, b, ang, 9, 1.0)]
        while stack:
            a, b, ang, steps, w = stack.pop()
            for st in range(steps):
                ang += (_h(n, st, int(a * 10), seed) - 0.5) * 0.8
                a2, b2 = a + math.cos(ang) * 0.9, b + math.sin(ang) * 0.9
                if not (u0 <= a2 <= u1 and v0 <= b2 <= v1):
                    break
                segs.append(((a, b), (a2, b2), w))
                if _h(n, st, 7, seed) > 0.78 and w > 0.5:
                    stack.append((a2, b2, ang + (0.9 if _h(n, st, 8, seed) > 0.5 else -0.9), steps - st - 1, w * 0.7))
                a, b = a2, b2
    return tuple(segs)


def veins(face_want, a, b, face, rect, seed=1, count=4, width=0.16):
    """-> (on_vein, lit_side) for raised veins drawn in a plane rectangle (u0, v0, u1, v1) on faces `face_want`."""
    if face not in face_want:
        return False, False
    u0, v0, u1, v1 = rect
    if not (u0 - 1 <= a <= u1 + 1 and v0 - 1 <= b <= v1 + 1):
        return False, False
    for (p, q, w) in _vein_paths(seed, u0, v0, u1, v1, count):
        dx, dy = q[0] - p[0], q[1] - p[1]
        L2 = dx * dx + dy * dy or 1e-9
        t = max(0.0, min(1.0, ((a - p[0]) * dx + (b - p[1]) * dy) / L2))
        px, py = p[0] + dx * t, p[1] + dy * t
        d = math.hypot(a - px, b - py)
        if d < width * w * 1.6:
            return True, (b - py) > 0
    return False, False


# ---- materials ------------------------------------------------------------------------------------------------------

def solid(P, key, glow=False, bevel_w=0.35):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        c = p[key]
        f = bevel(*local(x, y, z, face, box), face, bevel_w) if box is not None else 1.0
        return _finish(c, face, f), (c[:3] if glow else None)
    return s


def skin(P, key, dark=None, bulges=(), vein_rects=(), vein_key=None, var=0.05, bevel_w=0.5, seed=0, light=None,
         vein_width=0.22, vein_count=3):
    """Skin or hide: soft tonal variation, bevelled edges, muscle masses and raised veins. Highlights blend toward
    `light` (or a lifted base) and shadows toward `dark`, so muscle reads on dark hides as well as pale ones."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        base = p[key]
        f = 1.0 + var * (fbm(x * 0.35, y * 0.35, z * 0.35, seed) - 0.5) * 2
        if box is not None:
            f *= bevel(*local(x, y, z, face, box), face, bevel_w, 0.13)
        a, b = plane(x, y, z, face)
        if bulges:
            f *= muscles(bulges, a, b, face)
        col = base
        for rect, faces, vseed in vein_rects:
            on, lit = veins(faces, a, b, face, rect, seed=vseed, count=vein_count, width=vein_width)
            if on:
                vc = p[vein_key] if vein_key else mul(base, 0.85)
                col = mix(vc, p[light] if light else (255, 255, 255), 0.25) if lit else mul(vc, 0.8)
                break
        hi = p[light] if light else mix(base, (255, 255, 255), 0.35)
        lo = p[dark] if dark else mul(base, 0.55)
        if f > 1:
            col = mix(col, hi, (f - 1) * 3.5)
        else:
            col = mix(lo, col, 1 - (1 - f) * 2.0)
        return _finish(col, face, 1.0), None
    return s


def scales(P, key, rim, size=1.4, light=None, belly_key=None, belly=lambda x, y, z, face: False, seed=0):
    """Overlapping scales: each a rounded cell lit at its top, with a darker rim and a lighter centre."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if belly_key and belly(x, y, z, face):
            a, b = plane(x, y, z, face)
            band = (b % (size * 0.9)) / (size * 0.9)
            c = mul(p[belly_key], 0.88 if band < 0.16 else 1.0 + 0.06 * band)
            return _finish(c, face, bevel(*local(x, y, z, face, box), face) if box else 1), None
        a, b = plane(x, y, z, face)
        row = math.floor(b / (size * 0.75))
        aa = a + (size * 0.5 if row % 2 else 0)
        cu = (math.floor(aa / size) + 0.5) * size
        cv = (row + 0.5) * size * 0.75
        du, dv = (aa - cu) / (size * 0.5), (b - cv) / (size * 0.5)
        d = math.hypot(du, dv * 1.25)
        base = p[key]
        if d > 0.92:
            col = p[rim]
        else:
            col = mul(base, 1.0 + 0.16 * max(0, dv) * (1 - d) - 0.1 * d)
            if light and d < 0.35 and dv > 0:
                col = mix(col, p[light], 0.5)
        col = mul(col, 1 + 0.05 * (fbm(x * 0.3, y * 0.3, z * 0.3, seed) - 0.5))
        f = bevel(*local(x, y, z, face, box), face) if box is not None else 1
        return _finish(col, face, f), None
    return s


def fur(P, key, dark, tip=None, length=1.6, density=2.2, flow=(0, -1), seed=0):
    """Fur in clumps: strands streaked along `flow` (a plane direction), darker roots, lighter tips."""
    fl = math.hypot(*flow) or 1
    fx, fy = flow[0] / fl, flow[1] / fl

    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        a, b = plane(x, y, z, face)
        along = a * fx + b * fy
        across = -a * fy + b * fx
        n = noise2(across * density, along / length, seed)
        clump = noise2(across * 0.6, along * 0.25, seed + 5)
        strand = (n * 7 + clump * 3) % 1.0
        col = p[key]
        if strand < 0.18:
            col = mix(p[dark], col, strand / 0.18)
        elif tip and strand > 0.86:
            col = mix(col, p[tip], (strand - 0.86) / 0.14)
        f = 1 + 0.08 * (clump - 0.5)
        if box is not None:
            f *= bevel(*local(x, y, z, face, box), face, 0.6, 0.12)
        return _finish(col, face, f), None
    return s


def feathers(P, key, dark, shaft=None, size=(1.6, 2.6), flow=(0, -1), tip=None, seed=0):
    """Rows of overlapping feathers along `flow`, each with a central shaft and darker edges; optional coloured tips."""
    fl = math.hypot(*flow) or 1
    fx, fy = flow[0] / fl, flow[1] / fl
    w, h = size

    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        a, b = plane(x, y, z, face)
        along = a * fx + b * fy
        across = -a * fy + b * fx
        row = math.floor(along / (h * 0.6))
        ac = across + (w * 0.5 if row % 2 else 0)
        cu = (math.floor(ac / w) + 0.5) * w
        lu = (ac - cu) / (w * 0.5)
        lv = (along - row * h * 0.6) / (h * 0.6)
        col = p[key]
        if shaft and abs(lu) < 0.12:
            col = p[shaft]
        elif abs(lu) > 0.82 or lv > 0.92:
            col = p[dark]
        else:
            col = mul(col, 1.0 - 0.12 * abs(lu) + 0.06 * (1 - lv))
            if (abs(lu) * 6 + lv * 3) % 1.0 < 0.15:
                col = mul(col, 0.93)                                       # barbs
        if tip and lv < 0.22:
            col = mix(col, p[tip], 1 - lv / 0.22)
        f = bevel(*local(x, y, z, face, box), face, 0.4, 0.1) if box is not None else 1
        return _finish(col, face, f), None
    return s


def armour(P, key, dark, light=None, trim=None, panel=None, rivets=False, engrave=None, glow_key=None, seams=(),
           trim_w=0.5, trim_edges=("top", "bottom"), seed=0):
    """Smooth plate armour: lighter toward each plate's top with a broad soft highlight band, a darker lower rim,
    optional trim colour round every plate edge (with a thin dark line inside it), optional seam lines at plane
    heights `seams`, an optional panel grid (pw, ph), rivets, an engraved pattern (engrave(a, b) -> bool) and
    glowing seams (glow_key)."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box) if box is not None else (1, 1, 9, 9)
        a, b = plane(x, y, z, face)
        col = p[key]
        side = face not in ("up", "down")
        if trim and side and H >= 1.5:
            dist = min([H - v] * ("top" in trim_edges) + [v] * ("bottom" in trim_edges) +
                       [u, W - u] * ("sides" in trim_edges) + [99])
            if dist < trim_w:
                col = p[trim]
                if v > H - trim_w:
                    col = mix(col, (255, 255, 255), 0.2)
                return _finish(col, face, 1.0), None
            if dist < trim_w + 0.18:
                return _finish(p[dark], face, 1.0), None
        g = 0.9 + 0.2 * (v / max(H, 1e-6)) if side else 1.05
        band = math.exp(-(((v / max(H, 1e-6)) - 0.68) / 0.12) ** 2) if side else 0.0
        col = mix(col, p[light], band * 0.45) if light else mul(col, 1 + 0.12 * band)
        if any(abs(b - sh) < 0.14 for sh in seams) and side:
            if glow_key:
                return p[glow_key][:3] + (255,), p[glow_key][:3]
            return _finish(p[dark], face, 1.0), None
        if panel:
            pw, ph = panel
            if min(a % pw, pw - a % pw) < 0.12 or min(b % ph, ph - b % ph) < 0.12:
                if glow_key:
                    return p[glow_key][:3] + (255,), p[glow_key][:3]
                return _finish(p[dark], face, 1.0), None
            if rivets and math.hypot(min(a % pw, pw - a % pw) - 0.45, min(b % ph, ph - b % ph) - 0.45) < 0.2:
                col = p[light] if light else mul(col, 1.25)
        if engrave and engrave(a, b):
            col = mix(p[dark], col, 0.3)
        f = g * bevel(u, v, W, H, face, 0.6, 0.18)
        return _finish(col, face, f), None
    return s


def strands(P, key, dark, tip=None, root=None, lines=3):
    """A lock of hair or a flame-tongue of fur (for rods): darker at the root, lighter toward the tip, with a few
    darker strand lines running its length."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        along = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)        # 0 at the root
        u, v, W, H = local(x, y, z, face, box)
        across = (u / max(W, 1e-6)) if face in ("up", "down", "north", "south") else (v / max(H, 1e-6))
        col = mix(p[root or dark], p[key], min(1, along * 2.5))
        if tip and along > 0.7:
            col = mix(col, p[tip], (along - 0.7) / 0.3)
        if (across * lines) % 1.0 < 0.14:
            col = mul(col, 0.82)
        return _finish(col, face, 1.0 - 0.1 * (1 - along)), None
    return s


def flame_inside(tongues=4, lean=0.0, seed=0, base=0.45):
    """A flame silhouette on a plane box (for cutout): a teardrop body (narrow at the root, widest low down) that
    splits into `tongues` pointed tongues of differing heights, leaning by `lean`."""
    cs = [(-0.28 + 0.56 * j / max(tongues - 1, 1), 0.62 + 0.38 * _h(j, 3, 0, seed)) for j in range(tongues)]

    def inside(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        t = v / max(H, 1e-6)
        uu = u / max(W, 1e-6) - 0.5 - lean * t * t
        body = 0.48 * math.sin(math.pi * min(1.0, (t / base) * 0.5 + 0.08)) * (1 - max(0, t - base) / (1 - base))
        if abs(uu) < body * (0.85 + 0.15 * math.sin(t * 17 + seed)):
            return True
        if t < base * 0.6:
            return False
        for c, h in cs:
            if t < h:
                w = 0.13 * (1 - (t - base * 0.6) / max(h - base * 0.6, 1e-6)) ** 0.8
                if abs(uu - c * (0.6 + 0.6 * t)) < w:
                    return True
        return False
    return inside


def metal(P, key, dark=None, light=None, streak=3.2, seed=0):
    """Polished metal: a diagonal specular streak across each face and a dark lower rim."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box) if box is not None else (0, 0, 9, 9)
        a, b = plane(x, y, z, face)
        t = ((a * 0.7 + b) % streak) / streak
        spec = math.exp(-((t - 0.5) / 0.08) ** 2)
        col = p[key]
        if light:
            col = mix(col, p[light], spec * 0.8)
        else:
            col = mul(col, 1 + 0.35 * spec)
        if dark and v < H * 0.25 and face not in ("up", "down"):
            col = mix(p[dark], col, v / (H * 0.25))
        return _finish(col, face, bevel(u, v, W, H, face, 0.4, 0.18)), None
    return s


def fabric(P, key, dark, axis="y", period=2.4, seam=None, seed=0):
    """Cloth: soft folds running along `axis`, warped so they don't look ruled; optional seam colour at box edges."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box) if box is not None else (0, 0, 9, 9)
        a, b = plane(x, y, z, face)
        across = a if axis == "y" else b
        along = b if axis == "y" else a
        w = across + 0.8 * noise2(across * 0.3, along * 0.25, seed)
        fold = 0.5 + 0.5 * math.sin(w / period * 2 * math.pi)
        col = mix(p[dark], p[key], 0.55 + 0.45 * fold)
        if seam and edge_t(u, v, W, H, 0.3) < 1:
            col = p[seam]
        return _finish(col, face, bevel(u, v, W, H, face, 0.5, 0.1)), None
    return s


def leather(P, key, dark, stitch=None):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box) if box is not None else (0, 0, 9, 9)
        col = mul(p[key], 1 + 0.1 * (fbm(x * 0.8, y * 0.8, z * 0.8, 3) - 0.5))
        if stitch and 0.3 < edge_t(u, v, W, H, 1.0) < 0.5 and int((u + v) * 2.5) % 2 == 0:
            col = p[stitch]
        elif edge_t(u, v, W, H, 0.25) < 1:
            col = p[dark]
        return _finish(col, face, bevel(u, v, W, H, face, 0.4, 0.12)), None
    return s


def gem(P, key, light, glow=True):
    """A cut gem: facets as a radial pattern, a bright highlight, glowing."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        du, dv = (u / max(W, 1e-6) - 0.5), (v / max(H, 1e-6) - 0.5)
        ang = math.atan2(dv, du)
        facet = (int((ang + math.pi) / (math.pi / 3)) % 2)
        col = mul(p[key], 0.85 if facet else 1.08)
        if math.hypot(du + 0.18, dv - 0.18) < 0.13:
            col = p[light]
        return col[:3] + (255,), (col[:3] if glow else None)
    return s


def eye(p, du, dv, r, iris, pupil="pupil", white="white", lid=None, slit=False, ring=None):
    """A detailed round eye (du, dv relative to its centre, radius r): sclera rim, iris with a darker outer ring and a
    lighter inner band, round or slit pupil, two glints, optional lid line above. -> colour or None."""
    d = math.hypot(du, dv)
    if lid and r < dv < r * 1.25 and abs(du) < r * 1.05:
        return p[lid]
    if d > r:
        return None
    if d > r * 0.9:
        return p[pupil]
    if math.hypot(du + r * 0.32, dv - r * 0.32) < r * 0.2 or math.hypot(du - r * 0.25, dv + r * 0.3) < r * 0.09:
        return p[white]
    pr = r * 0.32
    if (slit and abs(du) < r * 0.12 and abs(dv) < r * 0.75) or (not slit and d < pr):
        return p[pupil]
    if d > r * 0.74:
        return mul(p[ring] if ring else p[iris], 0.7)
    return mix(p[iris], (255, 255, 255), 0.18 * (1 - d / r)) if d < r * 0.55 else p[iris]


def cutout(inside, shader):
    """Make a shader transparent where inside(x, y, z, face, box) is false (for fins, wings, tattered cloth)."""
    def s(x, y, z, face, variant, box=None, **k):
        if not inside(x, y, z, face, box):
            return (0, 0, 0, 0), None
        return shader(x, y, z, face, variant, box=box, **k)
    return s


def twisted(P, key, dark, light=None, period=2.2, angle=0.6, seed=0):
    """Twisted rope / braided vine (for rods): smooth diagonal strands, each lit along its middle and shadowed at its
    edges, the strands spiralling round the rod."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        along = box.lo[2] + box.size[2] - z if box is not None else y
        around = {"north": u, "south": W - u, "east": W + u, "west": -u, "up": u, "down": -u}[face]
        t = ((around + along * angle) % period) / period
        prof = math.sin(t * math.pi)
        col = mix(p[dark], p[key], 0.35 + 0.65 * prof)
        if light and prof > 0.85:
            col = mix(col, p[light], (prof - 0.85) / 0.15 * 0.7)
        return _finish(col, face, 1.0), None
    return s


def riveted(P, key, dark, light=None, spacing=2.2, seed=0):
    """Hammered bronze / iron: soft mottling, rows of round rivets with a lit top."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        a, b = plane(x, y, z, face)
        col = mul(p[key], 1 + 0.12 * (fbm(x * 0.6, y * 0.6, z * 0.6, seed) - 0.5))
        ca, cb = (math.floor(a / spacing) + 0.5) * spacing, (math.floor(b / spacing) + 0.5) * spacing
        d = math.hypot(a - ca, b - cb)
        if d < 0.42:
            col = p[light] if (light and b > cb) else mul(p[key], 1.2)
        elif d < 0.55:
            col = p[dark]
        f = bevel(*local(x, y, z, face, box), face, 0.5, 0.18) if box is not None else 1
        return _finish(col, face, f), None
    return s
