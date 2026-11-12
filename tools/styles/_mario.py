"""
Super Mario collection: Pokemon dressed as power-ups and plumbing heroes (original painted patterns inspired by the
games; no sprites copied).

Looks (one per line, three lines each):
  mushroom        a red mushroom cap with big white spots over a cream stem (shiny: the green 1-up mushroom)
  fire_flower     white top, red bottom, a fire-flower emblem on the chest and glowing fireballs (shiny: ice flower)
  super_star      bright star gold with a star on the chest, flashing every colour when invincible (shiny: hues turned)
  question_block  golden ? blocks over a brown brick base, the ? marks blinking (shiny: blue underground blocks)
  plumber         a red shirt, blue overalls with gold buttons and brown boots (shiny: green shirt, navy overalls)
  koopa_shell     green shell plates with cream seams over yellow skin (shiny: a red shell)
"""
from __future__ import annotations

import math

import numpy as np

from ._cosmic import centre_of, even, hue_turn_fast, noise, ramp
from ._fx import make as _make
from ._void import voronoi_cracks

POWER = {"name": "power", "emissive": True, "translucent": True, "frames": 4, "fps": 6}
QMARK = ["0110", "1001", "0001", "0010", "0100", "0000", "0100"]     # a ? in 4x7


def _area(c):
    return max(1.0, c.alpha.sum() / float(c.u * c.u))


def shaded(c, colour, mottle, k=0.55):
    """A flat cartoon colour with the original's shading."""
    return np.asarray(colour, np.float32) * (1 - k / 2 + k * c.lum[..., None]) * (0.95 + 0.1 * mottle[..., None])


def star_mask(c, cx, cy, R):
    r = np.hypot(c.xx - cx, c.yy - cy)
    th = np.arctan2(c.yy - cy, c.xx - cx) + math.pi / 2
    return r <= R * (0.5 + 0.5 * np.abs(np.cos(2.5 * th)) ** 2)


def paint(look, c):
    rng, u = c.rng, c.u
    mottle = noise(c.h, c.w, 6 * u, rng, 2)
    body = c.alpha & ~c.eye
    cx, cy, r = centre_of(c.face, c.alpha)
    s = c.shiny
    if look == "mushroom":
        cap = (120, 200, 60) if s else (222, 34, 30)
        top = c.hm > 0.55
        rgb = np.where(top[..., None], shaded(c, cap, mottle), shaded(c, (244, 226, 186), mottle))
        g = 6 * u
        jx = (c.xx // g) * g + g / 2
        jy = (c.yy // g) * g + g / 2
        spot = (np.hypot(c.xx - jx, c.yy - jy) < 2.0 * u) & top & body
        rgb = np.where(spot[..., None], shaded(c, (252, 252, 248), mottle, 0.3), rgb)
    elif look == "fire_flower":
        lower = (110, 170, 240) if s else (226, 40, 28)
        rgb = np.where((c.hm > 0.5)[..., None], shaded(c, (248, 248, 242), mottle, 0.4), shaded(c, lower, mottle))
        d = np.hypot(c.xx - cx, c.yy - cy)
        rr = max(2.0 * u, min(r, 4 * u))
        rings = [((40, 120, 255) if s else (255, 90, 20), 1.0), ((180, 230, 255) if s else (255, 210, 40), 0.66),
                 ((255, 255, 255), 0.33)]
        for colour, f in rings:
            rgb = np.where(((d <= rr * f) & body)[..., None], np.asarray(colour, np.float32), rgb)
        emblem = (d <= rr) & body
        balls = np.zeros_like(c.alpha)
        ys, xs = np.nonzero(body)
        for _ in range(max(2, int(_area(c) / 220))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            balls |= np.hypot(c.xx - xs[k], c.yy - ys[k]) <= 1.2 * u
        balls &= body & ~emblem
        fire = (150, 220, 255) if s else (255, 150, 30)
        rgb = np.where(balls[..., None], np.asarray(fire, np.float32), rgb)
        c.shine(balls, fire, 1.0)
        c.shine(emblem, fire, 0.4)
        c.extra["flicker"] = balls | emblem
    elif look == "super_star":
        rgb = shaded(c, (255, 212, 40), mottle, 0.5)
        st = star_mask(c, cx, cy, max(2.5 * u, min(r, 5 * u))) & body
        rgb = np.where(st[..., None], np.array([255, 248, 200], np.float32), rgb)
        if s:
            rgb = hue_turn_fast(rgb, 0.45)
        c.extra["rainbow"] = body
    elif look == "question_block":
        blk = 5 * u
        bx, by = c.xx % blk, c.yy % blk
        top = c.hm > 0.4
        gold = (60, 110, 230) if s else (232, 160, 30)
        brick = (40, 70, 150) if s else (176, 86, 36)
        rgb = np.where(top[..., None], shaded(c, gold, mottle, 0.3), shaded(c, brick, mottle, 0.4))
        border = ((bx < max(1, u // 2)) | (by < max(1, u // 2))) & body
        rgb = np.where(border[..., None], rgb * 0.55, rgb)
        rivet = top & (((bx == u) | (bx == blk - u)) & ((by == u) | (by == blk - u))) & body
        rgb = np.where(rivet[..., None], rgb * 0.4, rgb)
        q = np.zeros_like(c.alpha)
        if blk >= 8:                                                                # room for a ? mark
            sc = max(1, blk // 9)
            ox, oy = (blk - 4 * sc) // 2, (blk - 7 * sc) // 2
            lx, ly = (bx - ox) // sc, (by - oy) // sc
            ok = (lx >= 0) & (lx < 4) & (ly >= 0) & (ly < 7)
            bits = np.array([[int(ch) for ch in row] for row in QMARK], bool)
            q = ok & bits[np.clip(ly, 0, 6).astype(int), np.clip(lx, 0, 3).astype(int)] & top & body
        else:
            q = (bx == blk // 2) & (by >= 1) & (by <= blk - 2) & ((by != blk - 3)) & top & body
        mark = (220, 235, 255) if s else (255, 236, 170)
        rgb = np.where(q[..., None], np.asarray(mark, np.float32), rgb)
        c.shine(q, mark, 0.7)
        c.extra["flicker"] = q
    elif look == "plumber":
        shirt, overall = ((40, 170, 50), (40, 40, 120)) if s else ((222, 34, 30), (40, 76, 210))
        line = 0.55
        rgb = np.where((c.hm > line)[..., None], shaded(c, shirt, mottle), shaded(c, overall, mottle))
        boots = (c.hm < 0.07) & body
        rgb = np.where(boots[..., None], shaded(c, (110, 60, 30), mottle), rgb)
        if c.face.torso:
            x, y, w, h = c.face.torso
            for bxp in (x + w * 0.28, x + w * 0.72):
                btn = (np.hypot(c.xx - bxp, c.yy - (y + h * 0.3)) <= max(1.0, 0.8 * u)) & body
                rgb = np.where(btn[..., None], np.array([250, 210, 40], np.float32), rgb)
    elif look == "koopa_shell":
        shell = (210, 40, 30) if s else (60, 170, 60)
        rgb = np.where((c.hm > 0.3)[..., None], shaded(c, shell, mottle), shaded(c, (240, 206, 90), mottle))
        seam = voronoi_cracks(c, rng, 5 * u) & (c.hm > 0.3) & body
        rgb = np.where(seam[..., None], np.array([240, 232, 196], np.float32), rgb)
    else:
        rgb = c.a[..., :3]
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)                            # the eyes stay their own
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    if "rainbow" in c.extra:                                                       # invincible: flashing colours
        m = c.extra["rainbow"]
        hue = (frame / 4.0 + c.hm * 0.5) % 1.0
        rgb = np.stack([0.5 + 0.5 * np.cos(2 * np.pi * (hue + o)) for o in (0.0, 0.33, 0.67)], -1) * 255
        g = np.where(m, 0.25, g)
        grgb = np.where(m[..., None], rgb, grgb)
    if "flicker" in c.extra:
        g = np.where(c.extra["flicker"], g0 * [1.0, 0.6, 1.0, 0.3][frame % 4], g)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
