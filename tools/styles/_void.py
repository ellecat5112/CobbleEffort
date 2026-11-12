"""
Abyss collection: Pokemon touched by the void that stares back (not the sea: the Deep Sea collection is styles/_abyss.py).

Looks (one per line, three lines each):
  void         inky starless black with a faint violet shimmer, motes of violet light drifting over it
  rift         obsidian split by a web of glowing magenta cracks, as if the void shows through
  eyes         dark hide covered in pale yellow slit-pupilled eyes that blink
  shadowflame  black with dark violet flames licking up from the feet, flickering
  sigil        dark slate carved with glowing green-cyan rune circles and glyph bands
  veins        dark crimson-black with branching veins of red light that pulse up the body
Every look: glowing eyes, and an emissive animated layer (GAZE).
Shiny: the void's light turned round the colour wheel.
"""
from __future__ import annotations

import math

import numpy as np

from ._arc import bolts, dilate
from ._cosmic import centre_of, even, hue_turn_fast, noise, ramp
from ._fx import make as _make

GAZE = {"name": "gaze", "emissive": True, "translucent": True, "frames": 4, "fps": 4}


def _area(c):
    return max(1.0, c.alpha.sum() / float(c.u * c.u))


def voronoi_cracks(c, rng, cell):
    """Borders between random cells (about half of them kept), one or two pixels wide."""
    ys, xs = np.nonzero(c.alpha)
    n = max(4, int(len(xs) / float(cell * cell)))
    k = rng.integers(len(xs), size=n)
    px, py = xs[k].astype(np.float32), ys[k].astype(np.float32)
    best = np.full((c.h, c.w), 1e9, np.float32)
    second = np.full((c.h, c.w), 1e9, np.float32)
    idx = np.zeros((c.h, c.w), np.int32)
    for i in range(n):
        d = np.sqrt((c.xx - px[i]) ** 2 + (c.yy - py[i]) ** 2)
        closer = d < best
        second = np.where(closer, best, np.minimum(second, d))
        idx = np.where(closer, i, idx)
        best = np.where(closer, d, best)
    keep = rng.random(n) < 0.6
    return (second - best < max(1.0, c.u * 0.6)) & keep[idx] & c.alpha


def paint(look, c):
    rng, u = c.rng, c.u
    mottle = noise(c.h, c.w, 6 * u, rng, 2)
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    c.extra["col"], c.extra["look"] = col, look
    eye_col = col((210, 170, 255))
    if look == "void":
        shimmer = noise(c.h, c.w, 10 * u, rng, 3)
        rgb = ramp(even([(1, 0, 4), (8, 4, 18), (26, 14, 46), (60, 36, 96)]), c.lum * 0.3 + shimmer * 0.45)
        sheen = np.clip((shimmer - 0.62) * 4, 0, 1)
        rgb = rgb + sheen[..., None] * col((70, 30, 120)) * 0.5
        c.shine(np.clip((shimmer - 0.7) * 3, 0, 1) * c.alpha, col((120, 60, 220)), 0.35)
        eye_col = col((235, 210, 255))
    elif look == "rift":
        rgb = ramp(even([(2, 1, 6), (14, 10, 22), (40, 32, 56), (84, 72, 104)]), c.lum * 0.45 + mottle * 0.35)
        crack = voronoi_cracks(c, rng, 7 * u) & ~c.eye
        glow_edge = dilate(crack, max(1, u // 2)) & c.alpha & ~c.eye
        rgb = np.where(glow_edge[..., None], rgb * 0.4 + col((160, 30, 140)) * 0.6, rgb)
        rgb = np.where(crack[..., None], col((255, 120, 230)), rgb)
        c.shine(glow_edge, col((200, 40, 200)), 0.6)
        c.shine(crack, col((255, 130, 240)), 1.0)
        eye_col = col((255, 150, 240))
    elif look == "eyes":
        rgb = ramp(even([(6, 3, 8), (24, 14, 28), (56, 38, 60), (100, 80, 104)]), c.lum * 0.55 + mottle * 0.35)
        ys, xs = np.nonzero(c.alpha & ~c.eye)
        eyes, sclera, pupil = [], np.zeros_like(c.alpha), np.zeros_like(c.alpha)
        for _ in range(max(3, int(_area(c) / 90))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            ex, ey = float(xs[k]), float(ys[k])
            rx, ry = rng.uniform(1.0, 1.8) * u, rng.uniform(0.6, 1.0) * u
            e = (((c.xx - ex) / rx) ** 2 + ((c.yy - ey) / ry) ** 2 <= 1)
            p = e & (np.abs(c.xx - ex) <= max(0.5, 0.25 * rx))
            sclera |= e
            pupil |= p
            eyes.append(e)
        sclera &= c.alpha & ~c.eye
        pupil &= sclera
        rgb = np.where(sclera[..., None], col((240, 226, 150)), rgb)
        rgb = np.where(pupil[..., None], np.array([10, 4, 8], np.float32), rgb)
        c.shine(sclera & ~pupil, col((255, 230, 120)), 0.9)
        c.extra["eyes"] = [e & c.alpha & ~c.eye & ~pupil for e in eyes]
        eye_col = col((255, 236, 130))
    elif look == "shadowflame":
        rgb = ramp(even([(2, 0, 6), (14, 6, 26), (40, 22, 64), (80, 56, 110)]), c.lum * 0.5 + mottle * 0.3)
        c.extra["flame_noise"] = noise(c.h, c.w, 2 * u, rng, 2)
        c.extra["flame_streak"] = noise(c.h, c.w, max(1, u), rng, 1)
        f = flames(c, 0)[..., None]
        fc = col((70, 20, 150)) * f + col((200, 150, 255)) * (1 - f)                # deep violet roots, lilac tips
        rgb = np.where(f > 0, rgb * (1 - 0.6 * f) + fc * 0.6 * f, rgb)
        eye_col = col((220, 160, 255))
    elif look == "sigil":
        rgb = ramp(even([(8, 10, 16), (24, 28, 40), (52, 58, 76), (100, 106, 126)]), c.lum * 0.55 + mottle * 0.3)
        rune = np.zeros_like(c.alpha)
        cx, cy, r = centre_of(c.face, c.alpha)
        rings = [(cx, cy, max(2.5 * u, min(r, 6 * u)))]
        ys, xs = np.nonzero(c.alpha & ~c.eye)
        for _ in range(max(1, int(_area(c) / 500))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            rings.append((float(xs[k]), float(ys[k]), rng.uniform(1.6, 3.0) * u))
        for rx, ry, rr in rings:
            d = np.sqrt((c.xx - rx) ** 2 + (c.yy - ry) ** 2)
            th = np.arctan2(c.yy - ry, c.xx - rx)
            rune |= np.abs(d - rr) < max(0.6, u * 0.5)                              # the ring
            rune |= (np.abs(d - rr * 0.72) < max(0.5, u * 0.4)) & (np.cos(th * 9) > 0.2)   # ticked inner ring
            for k3 in range(3):                                                    # an inscribed triangle
                a1, a2 = -math.pi / 2 + k3 * 2 * math.pi / 3, -math.pi / 2 + (k3 + 1) * 2 * math.pi / 3
                x1, y1 = rx + rr * 0.72 * math.cos(a1), ry + rr * 0.72 * math.sin(a1)
                x2, y2 = rx + rr * 0.72 * math.cos(a2), ry + rr * 0.72 * math.sin(a2)
                L = max(1e-6, math.hypot(x2 - x1, y2 - y1))
                t = np.clip(((c.xx - x1) * (x2 - x1) + (c.yy - y1) * (y2 - y1)) / (L * L), 0, 1)
                dd = np.hypot(c.xx - (x1 + t * (x2 - x1)), c.yy - (y1 + t * (y2 - y1)))
                rune |= dd < max(0.5, u * 0.4)
        band = np.abs((c.hm * 5) % 1 - 0.5) < 0.05                                  # glyph bands round the body
        cell = ((c.xx // max(1, u)).astype(int) * 7 + (c.yy // max(1, u)).astype(int) * 13) % 5
        rune |= band & (cell < 2)
        rune &= c.alpha & ~c.eye
        rgb = np.where(rune[..., None], col((150, 255, 210)), rgb)
        c.shine(rune, col((90, 255, 190)), 1.0)
        c.extra["rune"] = rune
        eye_col = col((140, 255, 210))
    elif look == "veins":
        rgb = ramp(even([(6, 1, 4), (26, 6, 14), (60, 20, 32), (110, 50, 64)]), c.lum * 0.5 + mottle * 0.35)
        n = max(3, int(_area(c) / 200))
        vein = bolts(c, rng, n, 14, 1.4 * u, jitter=0.45, branch=0.25) & ~c.eye
        thick = dilate(vein, max(0, u // 3)) & c.alpha & ~c.eye
        rgb = np.where(thick[..., None], col((150, 16, 40)), rgb)
        rgb = np.where(vein[..., None], col((255, 60, 80)), rgb)
        c.shine(thick, col((230, 30, 60)), 0.9)
        c.extra["vein"] = thick
        eye_col = col((255, 90, 100))
    else:
        rgb = c.a[..., :3]
    rgb = np.where(c.eye[..., None], eye_col, rgb)
    c.shine(c.eye, eye_col, 1.0)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def flames(c, frame):
    """Flame strength 0..1: tongues rising from the feet, shifted every frame."""
    nz = np.roll(c.extra["flame_noise"], -frame * max(1, c.u), axis=0)
    st = np.roll(c.extra["flame_streak"], -frame * max(1, c.u), axis=0)
    top = 0.1 + 0.32 * nz                                                         # ragged tongue tops
    f = np.clip((top - c.hm) / 0.1, 0, 1) * (0.55 + 0.45 * st) * c.alpha * ~c.eye
    return f.astype(np.float32)


def animate(glow, frame, c):
    look = c.extra.get("look")
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    col = c.extra["col"]
    rng = np.random.default_rng((c.seed * 31337 + frame * 7777) % (2 ** 32))
    if look == "void":
        motes = (rng.random(g.shape) < 0.012) & c.alpha & ~c.eye
        g = np.where(motes, 0.9, g)
        grgb = np.where(motes[..., None], col((200, 150, 255)), grgb)
    elif look == "rift":
        g = np.where(c.eye, g, g * [1.0, 0.75, 0.55, 0.75][frame % 4])
    elif look == "eyes":
        for e in c.extra["eyes"]:
            if rng.random() < 0.3:                                                  # this one blinks
                g = np.where(e, 0, g)
    elif look == "shadowflame":
        f = flames(c, frame)
        upd = f > g
        g = np.where(upd, f * 0.9, g)
        hot = np.clip(1 - f, 0, 1)[..., None]
        grgb = np.where(upd[..., None], col((120, 40, 230)) * (1 - hot) + col((230, 190, 255)) * hot, grgb)
    elif look == "sigil":
        g = np.where(c.extra["rune"], g * [1.0, 0.7, 0.45, 0.7][frame % 4], g)
    elif look == "veins":
        wave = 0.45 + 0.55 * np.clip(np.cos(2 * np.pi * (c.hm * 2 - frame / 4.0)), 0, 1)
        g = np.where(c.extra["vein"], g * wave, g)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
