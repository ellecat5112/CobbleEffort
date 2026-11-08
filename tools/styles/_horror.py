"""
Shared pixel-art horror toolkit for the Halloween styles.

Everything is drawn straight into texture (UV) space, scaled to the texture's resolution
(64 px textures use 1 px features; 128 px use 2 px; and so on). Placement is deterministic for a
given seed, and only the animated parts (jaws, pupils, blinks, drips) change between frames.
"""
from __future__ import annotations

import math
import random

from PIL import Image

BLOOD_DARK = (58, 0, 4)
BLOOD = (122, 6, 12)
BLOOD_WET = (176, 18, 24)
BLOOD_SHINE = (226, 92, 92)
FLESH = [(92, 12, 16), (128, 26, 30), (168, 48, 52), (204, 92, 92)]
FAT = (222, 196, 140)
STITCH = (28, 16, 10)
LID = (26, 4, 6)
SCLERA = (226, 216, 172)
VEIN = (176, 30, 34)
PUPIL = (6, 2, 2)
MOUTH_DEEP = (14, 0, 2)
MOUTH = (52, 4, 8)
LIP = (70, 8, 14)
TOOTH = (232, 222, 188)
TOOTH_DIRTY = (178, 160, 112)

# jaw openness per frame: open, closing, shut, opening -> gnashing
GNASH = [1.0, 0.55, 0.12, 0.55]


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


def value_noise(w: int, h: int, cell: int, rng: random.Random):
    """Smooth value noise (bilinear), values 0..1."""
    gw, gh = w // cell + 2, h // cell + 2
    grid = [[rng.random() for _ in range(gw)] for _ in range(gh)]
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        gy, fy = divmod(y / cell, 1)
        gy = int(gy)
        for x in range(w):
            gx, fx = divmod(x / cell, 1)
            gx = int(gx)
            a = lerp(grid[gy][gx], grid[gy][gx + 1], fx)
            b = lerp(grid[gy + 1][gx], grid[gy + 1][gx + 1], fx)
            out[y][x] = lerp(a, b, fy)
    return out


class Canvas:
    """RGBA pixel access plus an occupancy map, so stamped features don't overlap each other."""

    def __init__(self, img: Image.Image, src_alpha, eye_mask):
        self.img = img
        self.px = img.load()
        self.w, self.h = img.size
        self.alpha = src_alpha            # alpha[y][x] of the source texture
        self.eye = eye_mask               # True where Cobblemon paints this Pokémon's real eyes
        self.used = [[False] * self.w for _ in range(self.h)]

    def opaque(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h and self.alpha[y][x] > 0

    def put(self, x, y, c):
        if self.opaque(x, y):
            self.px[x, y] = tuple(int(v) for v in c[:3]) + (self.alpha[y][x],)

    def get(self, x, y):
        return self.px[x, y][:3]

    def free_rect(self, x0, y0, w, h, pad=1):
        for y in range(y0 - pad, y0 + h + pad):
            for x in range(x0 - pad, x0 + w + pad):
                if not self.opaque(x, y) or self.used[y][x] or self.eye[y][x]:
                    return False
        return True

    def claim(self, x0, y0, w, h):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                self.used[y][x] = True

    def find_spot(self, rng: random.Random, w, h, tries=300):
        if w >= self.w or h >= self.h:
            return None
        for _ in range(tries):
            x0, y0 = rng.randrange(1, self.w - w - 1), rng.randrange(1, self.h - h - 1)
            if self.free_rect(x0, y0, w, h):
                self.claim(x0, y0, w, h)
                return x0, y0
        return None


# ---------------------------------------------------------------------------------------------
# features. "plan" functions use the RNG (same for every frame); "draw" functions take the frame.
# ---------------------------------------------------------------------------------------------

def plan_eyes(cv: Canvas, rng: random.Random, scale: int, count: int):
    eyes = []
    for _ in range(count):
        big = rng.random() < 0.35
        ew, eh = (7, 5) if big else (5, 3)
        ew, eh = ew * scale, eh * scale
        spot = cv.find_spot(rng, ew, eh)
        if not spot:
            continue
        eyes.append({
            "x": spot[0], "y": spot[1], "w": ew, "h": eh,
            "iris": rng.choice([(150, 12, 12), (196, 170, 30), (90, 120, 40), (20, 20, 20), (210, 210, 200)]),
            "dart": [rng.choice((-1, 0, 1)) for _ in GNASH],
            "blink": rng.randrange(len(GNASH)) if rng.random() < 0.4 else -1,
            "veins": [(rng.randrange(ew), rng.randrange(eh)) for _ in range(2 * scale)],
            "tear": rng.random() < 0.5,
        })
    return eyes


def draw_eye(cv: Canvas, e, frame: int, scale: int):
    x0, y0, ew, eh = e["x"], e["y"], e["w"], e["h"]
    cx, cy = x0 + (ew - 1) / 2, y0 + (eh - 1) / 2
    rx, ry = ew / 2, eh / 2
    closed = e["blink"] == frame % len(GNASH)
    for y in range(y0, y0 + eh):
        for x in range(x0, x0 + ew):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d > 1.05:
                continue
            if closed:
                cv.put(x, y, LID if abs(y - cy) < scale else mix(cv.get(x, y), LID, 0.5))
            elif d > 0.62:
                cv.put(x, y, LID)
            else:
                cv.put(x, y, SCLERA)
    if closed:
        return
    for vx, vy in e["veins"]:
        x, y = x0 + vx, y0 + vy
        if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 0.6:
            cv.put(x, y, VEIN)
    dart = e["dart"][frame % len(GNASH)] * scale
    ir = max(1, int(min(ew, eh) * 0.34))
    for y in range(y0, y0 + eh):
        for x in range(x0, x0 + ew):
            dx, dy = x - (cx + dart), y - cy
            if dx * dx + dy * dy <= ir * ir and ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 0.62:
                cv.put(x, y, PUPIL if dx * dx + dy * dy <= (ir * 0.5) ** 2 else e["iris"])
    if e["tear"]:   # a bloody tear running from the lower lid
        tx = int(cx) + scale
        for i in range(eh // 2 + 1, eh // 2 + 1 + 4 * scale):
            if cv.opaque(tx, int(cy) + i):
                cv.put(tx, int(cy) + i, BLOOD if i % 3 else BLOOD_WET)


def plan_mouths(cv: Canvas, rng: random.Random, scale: int, count: int):
    mouths = []
    for _ in range(count):
        mw, mh = rng.choice(((9, 5), (11, 6), (7, 4))) if count > 1 else (11, 6)
        mw, mh = mw * scale, mh * scale
        spot = cv.find_spot(rng, mw, mh)
        if not spot:
            continue
        mouths.append({
            "x": spot[0], "y": spot[1], "w": mw, "h": mh,
            "phase": rng.randrange(len(GNASH)),
            "teeth": [rng.choice((1, 2, 2, 3)) for _ in range(mw // scale + 1)],
            "bloody": {rng.randrange(mw // scale) for _ in range(2)},
        })
    return mouths


def draw_mouth(cv: Canvas, m, frame: int, scale: int):
    x0, y0, mw, mh = m["x"], m["y"], m["w"], m["h"]
    openness = GNASH[(frame + m["phase"]) % len(GNASH)]
    mid = y0 + mh // 2
    half = max(scale, int(round((mh / 2) * openness)))
    top, bot = mid - half, mid + half
    for x in range(x0, x0 + mw):
        edge = min(x - x0, x0 + mw - 1 - x)
        taper = min(1.0, (edge + 1) / (2 * scale))           # lips pinch at the corners
        t = int(top + (mid - top) * (1 - taper))
        b = int(bot - (bot - mid) * (1 - taper))
        for y in range(y0, y0 + mh):
            if t <= y <= b:
                depth = 1 - abs(y - mid) / max(1, half)
                cv.put(x, y, mix(MOUTH, MOUTH_DEEP, depth))
            elif t - scale <= y < t or b < y <= b + scale:
                cv.put(x, y, LIP)
        # jagged teeth hanging from the top lip and rising from the bottom one
        i = (x - x0) // scale
        tooth = m["teeth"][i] * scale
        if (x - x0) % (2 * scale) < scale or tooth > 2 * scale:
            col = BLOOD_WET if i in m["bloody"] else (TOOTH if i % 3 else TOOTH_DIRTY)
            for k in range(min(tooth, max(scale, b - t))):
                if t + k <= mid:
                    cv.put(x, t + k, col)
                if b - k >= mid:
                    cv.put(x, b - k, TOOTH if i % 2 else TOOTH_DIRTY)


def blood_splatter(cv: Canvas, rng: random.Random, scale: int, count: int):
    drips = []
    for _ in range(count):
        x, y = rng.randrange(cv.w), rng.randrange(cv.h)
        if not cv.opaque(x, y) or cv.eye[y][x]:
            continue
        r = rng.uniform(1.2, 3.2) * scale
        for yy in range(int(y - r - 1), int(y + r + 2)):
            for xx in range(int(x - r - 1), int(x + r + 2)):
                d = math.hypot(xx - x, yy - y)
                if d <= r and cv.opaque(xx, yy) and not cv.used[yy][xx] and not cv.eye[yy][xx]:
                    cv.put(xx, yy, BLOOD_DARK if d > r - scale else (BLOOD if rng.random() < 0.7 else BLOOD_WET))
        for _ in range(4 * scale):   # flecks around the splash
            a, d = rng.uniform(0, 6.283), rng.uniform(r + scale, r + 4 * scale)
            fx, fy = int(x + math.cos(a) * d), int(y + math.sin(a) * d)
            if cv.opaque(fx, fy) and not cv.used[fy][fx] and not cv.eye[fy][fx]:
                cv.put(fx, fy, BLOOD)
        if rng.random() < 0.7:
            drips.append({"x": int(x), "y": int(y + r), "len": rng.randint(3, 9) * scale})
    return drips


def draw_drips(cv: Canvas, drips, frame: int, scale: int):
    """Blood runs straight down (in texture space) and a drop creeps further each frame."""
    for d in drips:
        x, y = d["x"], d["y"]
        n = 0
        while n < d["len"] and cv.opaque(x, y + n):
            for sx in range(scale):
                if cv.opaque(x + sx, y + n) and not cv.used[y + n][x + sx]:
                    cv.put(x + sx, y + n, BLOOD if n % (3 * scale) else BLOOD_WET)
            n += 1
        drop = y + n + (frame % len(GNASH)) * scale // 2
        for dy in range(scale + 1):
            for sx in range(scale + 1):
                if cv.opaque(x + sx, drop + dy):
                    cv.put(x + sx, drop + dy, BLOOD_SHINE if dy == 0 and sx == 0 else BLOOD_WET)


def wound(cv: Canvas, rng: random.Random, scale: int, stitched: bool):
    """A torn patch of raw flesh with a ragged edge, sometimes crudely stitched shut."""
    ww, wh = rng.randint(6, 12) * scale, rng.randint(3, 6) * scale
    spot = cv.find_spot(rng, ww, wh, tries=150)
    if not spot:
        return
    x0, y0 = spot
    cx, cy = x0 + ww / 2, y0 + wh / 2
    for y in range(y0, y0 + wh):
        for x in range(x0, x0 + ww):
            d = ((x - cx) / (ww / 2)) ** 2 + ((y - cy) / (wh / 2)) ** 2 + rng.uniform(-0.25, 0.25)
            if d < 0.55:
                c = rng.choice(FLESH[:3])
                cv.put(x, y, FAT if rng.random() < 0.06 else c)
            elif d < 1.0:
                cv.put(x, y, mix(cv.get(x, y), BLOOD_DARK, 0.75))
    if stitched:
        for x in range(x0 + scale, x0 + ww - scale, 3 * scale):
            for k in range(-scale, wh // 2 + scale):
                cv.put(x, int(cy) + k - wh // 4, STITCH)
        for x in range(x0, x0 + ww):
            cv.put(x, int(cy), STITCH)


def lump(cv: Canvas, rng: random.Random, scale: int, tint):
    """A swollen, bruised growth: a highlight on top, a shadow ring below."""
    r = rng.randint(3, 6) * scale
    spot = cv.find_spot(rng, 2 * r, 2 * r, tries=120)
    if not spot:
        return
    cx, cy = spot[0] + r, spot[1] + r
    for y in range(cy - r, cy + r):
        for x in range(cx - r, cx + r):
            d = math.hypot(x - cx, y - cy) / r
            if d > 1:
                continue
            base = mix(cv.get(x, y), tint, 0.45 * (1 - d))
            light = (cy - y) / r * 0.35 * (1 - d) - (0.4 if d > 0.82 else 0)
            cv.put(x, y, tuple(max(0, min(255, int(c * (1 + light)))) for c in base))


def find_eye_mask(base: Image.Image, eyes: Image.Image | None):
    w, h = base.size
    src = base.load()
    mask = [[False] * w for _ in range(h)]
    if eyes is not None:
        e = eyes.convert("RGBA").resize((w, h), Image.NEAREST).load()
        for y in range(h):
            for x in range(w):
                mask[y][x] = e[x, y][3] > 0 and src[x, y][3] > 0
    return mask


def components(points):
    """Split a pixel list into 4-connected groups (e.g. a Pokémon's separate eyes)."""
    left, groups = set(points), []
    while left:
        stack, group = [left.pop()], []
        while stack:
            x, y = stack.pop()
            group.append((x, y))
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in left:
                    left.remove(n)
                    stack.append(n)
        groups.append(sorted(group))
    return sorted(groups)
