"""
Halloween collection, special look for the Charmander line: "Bone-Rot".

The Pokémon is a walking skeleton with its flesh rotting off the bones:

* the body becomes bone (ivory, cracked and pitted)
* the pale belly becomes an exposed rib cage, with dark gaps and glimpses of innards
* ragged patches of rotting flesh (dark red, maroon, bruise-purple, rot-green) still cling on,
  with blood and ichor dripping down from them and a few maggots
* the eyes are hollow black sockets with a flickering pink ember deep inside
* a skeletal grin with gnashing teeth, and a couple of extra eyes in the rotting flesh
* the tail fire (an animated glowing layer) burns PINK
* shiny: charred black bones instead of ivory
"""
from __future__ import annotations

import colorsys
import hashlib
import random

from PIL import Image

from . import _horror as H

EMISSIVE = "retexture"
FRAMES = len(H.GNASH)
FPS = 5

BONE = [(0.00, (52, 44, 34)), (0.35, (128, 114, 90)), (0.70, (214, 202, 172)), (1.00, (244, 238, 220))]
CHARRED = [(0.00, (14, 12, 14)), (0.35, (46, 42, 46)), (0.70, (92, 86, 92)), (1.00, (140, 134, 140))]
ROTTING = [(92, 16, 18), (118, 30, 26), (70, 22, 40), (74, 86, 38), (104, 44, 30)]
CAVITY = (16, 6, 6)
INNARDS = (96, 18, 22)
CRACK = (30, 22, 16)
MAGGOT = (236, 228, 196)
SOCKET = (6, 3, 4)
EMBER = [(255, 80, 178), (255, 170, 220), (255, 80, 178), (214, 40, 140)]
PINK_FIRE = [(0.0, (0, 0, 0)), (0.12, (110, 10, 70)), (0.35, (214, 36, 138)), (0.65, (255, 92, 182)), (0.85, (255, 180, 224)),
             (1.0, (255, 240, 250))]

_cache: dict = {}


def _ramp(stops, v: float):
    v = max(0.0, min(1.0, v))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if v <= p1:
            return H.mix(c0, c1, (v - p0) / (p1 - p0))
    return stops[-1][1]


def _digest(img: Image.Image | None) -> str:
    return "" if img is None else hashlib.md5(img.convert("RGBA").tobytes()).hexdigest()


def _pink_fire(base: Image.Image) -> Image.Image:
    base = base.convert("RGBA")
    out = Image.new("RGBA", base.size)
    s, o = base.load(), out.load()
    for y in range(base.height):
        for x in range(base.width):
            r, g, b, a = s[x, y]
            o[x, y] = _ramp(PINK_FIRE, (0.2 * r + 0.5 * g + 0.3 * b) / 255 * 1.15) + (a,) if a else (0, 0, 0, 0)
    return out


def _plan(base: Image.Image, eyes: Image.Image | None, seed: int, shiny: bool):
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)
    units = max(1.0, (w * h) / (64 * 64) / (scale * scale))
    alpha = [[src[x, y][3] for x in range(w)] for y in range(h)]
    eye_mask = H.find_eye_mask(base, eyes)
    flesh_noise = H.value_noise(w, h, max(3, 5 * scale), rng)
    rot_noise = H.value_noise(w, h, max(3, 4 * scale), rng)
    bone_ramp = CHARRED if shiny else BONE

    img = Image.new("RGBA", (w, h))
    px = img.load()
    rib = [[False] * w for _ in range(h)]
    flesh = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if a == 0:
                px[x, y] = (0, 0, 0, 0)
                continue
            hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            # the pale belly (cream/yellow) becomes the rib cage
            rib[y][x] = (0.08 <= hh <= 0.2 and l > 0.6 and s > 0.25) or (l > 0.86 and s < 0.3)
            flesh[y][x] = not rib[y][x] and not eye_mask[y][x] and flesh_noise[y][x] > 0.52
            if rib[y][x]:
                period = 3 * scale
                c = _ramp(bone_ramp, 0.8) if (y % period) < 2 * scale else \
                    (INNARDS if rot_noise[y][x] > 0.6 else CAVITY)
            elif flesh[y][x]:
                c = ROTTING[int(rot_noise[y][x] * len(ROTTING)) % len(ROTTING)]
                c = H.mix(c, (20, 4, 6), max(0.0, 0.62 - flesh_noise[y][x]) * 4)   # darker at the torn edge
            else:
                c = _ramp(bone_ramp, 0.25 + l * 0.75 + rng.uniform(-0.04, 0.04))
            px[x, y] = tuple(int(v) for v in c) + (a,)
    cv = H.Canvas(img, alpha, eye_mask)

    # ragged dark rim where flesh tears away from bone
    for y in range(h):
        for x in range(w):
            if flesh[y][x] and any(cv.opaque(x + dx, y + dy) and not flesh[y + dy][x + dx] and not rib[y + dy][x + dx]
                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                                   if 0 <= x + dx < w and 0 <= y + dy < h):
                cv.put(x, y, H.BLOOD_DARK)
    # cracks and pits in exposed bone
    for _ in range(int(3 * units)):
        x, y = rng.randrange(w), rng.randrange(h)
        for _ in range(rng.randint(4, 10) * scale):
            if cv.opaque(x, y) and not flesh[y][x] and not rib[y][x] and not eye_mask[y][x]:
                cv.put(x, y, CRACK)
            x += rng.choice((-1, 0, 1))
            y += rng.choice((0, 1, 1))
            if not (0 <= x < w and 0 <= y < h):
                break
    # blood and ichor run down from the bottom edge of the flesh, maggots crawl in it
    drips = []
    for y in range(h - 1):
        for x in range(0, w, scale):
            if flesh[y][x] and not flesh[y + 1][x] and cv.opaque(x, y + 1) and rng.random() < 0.18:
                drips.append({"x": x, "y": y + 1, "len": rng.randint(2, 7) * scale})
            if flesh[y][x] and rng.random() < 0.012:
                cv.put(x, y, MAGGOT)
    for y in range(h):
        for x in range(w):
            if flesh[y][x] or rib[y][x]:
                cv.used[y][x] = False   # stamps may sit on flesh
    mouths = H.plan_mouths(cv, rng, scale, int(min(3, 1 + units / 2)))
    extra_eyes = H.plan_eyes(_FleshOnly(cv, flesh), rng, scale, int(min(6, 2 + units)))
    sockets = H.components([(x, y) for y in range(h) for x in range(w) if eye_mask[y][x]])
    return img, cv, scale, sockets, extra_eyes, mouths, drips


class _FleshOnly:
    """Canvas view that only allows stamps fully inside rotting flesh."""

    def __init__(self, cv, flesh):
        self.cv, self.flesh = cv, flesh
        self.w, self.h = cv.w, cv.h

    def find_spot(self, rng, w, h, tries=300):
        for _ in range(tries):
            spot = self.cv.find_spot(rng, w, h, tries=1)
            if spot and all(self.flesh[y][x] for y in range(spot[1], spot[1] + h) for x in range(spot[0], spot[0] + w)):
                return spot
        return None


def retexture(base: Image.Image, eyes: Image.Image | None, seed: int, shiny: bool,
              frame: int = 0, layer=False) -> Image.Image:
    if layer == "emissive":
        return _pink_fire(base)
    key = (_digest(base), _digest(eyes), seed, shiny)
    if key not in _cache:
        _cache.clear()
        _cache[key] = _plan(base, eyes, seed, shiny)
    img, cv0, scale, sockets, extra_eyes, mouths, drips = _cache[key]
    if layer:
        return img.copy()
    out = img.copy()
    cv = H.Canvas(out, cv0.alpha, cv0.eye)
    cv.used = cv0.used
    H.draw_drips(cv, drips, frame, scale)
    ember = EMBER[frame % len(EMBER)]
    for socket in sockets:
        for x, y in socket:
            cv.put(x, y, SOCKET)
        cx = sorted(p[0] for p in socket)[len(socket) // 2]
        cy = sorted(p[1] for p in socket)[len(socket) // 2]
        cells = set(socket)
        for sy in range(scale):
            for sx in range(scale):
                if (cx + sx, cy + sy) in cells:
                    cv.put(cx + sx, cy + sy, ember)
    for e in extra_eyes:
        H.draw_eye(cv, e, frame, scale)
    for m in mouths:
        H.draw_mouth(cv, m, frame, scale)
    return out
