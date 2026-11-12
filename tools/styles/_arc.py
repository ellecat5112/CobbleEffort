"""
Arc Light collection: Pokemon crackling with electric light.

Looks (one per line, three lines each):
  tesla          dark blued steel scarred with pale Lichtenberg branches; blue-white bolts strike across it
  plasma         smoky violet glass with a glowing heart on the chest and pink-violet filaments reaching out
  welding        scorched, heat-tinted metal with white-hot molten seams and showers of orange sparks
  storm          storm-cloud grey with big yellow lightning bolts forking downwards
  ladder         dark slate with violet arcs stretched sideways across the body, climbing it like a Jacob's ladder
  ball_lightning deep navy with glowing orbs of cyan-white light, each in a halo of crackling sparks
Every look: glowing eyes, and an emissive animated layer (ARC) where the arcs re-strike every frame.
Shiny: the electric light turned round the colour wheel.
"""
from __future__ import annotations

import math

import numpy as np

from ._cosmic import centre_of, even, hue_turn_fast, noise, outline, ramp
from ._fx import make as _make

ARC = {"name": "arc", "emissive": True, "translucent": True, "frames": 4, "fps": 8}


def dilate(mask, r):
    out = mask.copy()
    for _ in range(max(0, int(r))):
        p = np.pad(out, 1)
        out = out | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    return out


def bolts(c, rng, count, length, step, angle=None, jitter=0.7, branch=0.12, starts=None):
    """Jagged, branching bolt lines (one pixel wide) on the painted area: `count` bolts of `length` steps of `step`
    pixels, heading at `angle` (radians in texture space; random per bolt if None), forking now and then."""
    m = np.zeros((c.h, c.w), bool)
    ys, xs = np.nonzero(c.alpha)
    if len(xs) == 0:
        return m
    todo = []
    for i in range(count):
        if starts is not None and i < len(starts):
            x, y = starts[i]
        else:
            k = rng.integers(len(xs))
            x, y = float(xs[k]), float(ys[k])
        a = rng.uniform(0, 2 * math.pi) if angle is None else angle + rng.normal(0, 0.25)
        todo.append((x, y, a, length))
    while todo:
        x, y, a, n = todo.pop()
        for _ in range(n):
            t = a + rng.normal(0, jitter)
            nx, ny = x + step * math.cos(t), y + step * math.sin(t)
            num = int(step * 2) + 2
            for f in np.linspace(0, 1, num):
                px, py = int(x + (nx - x) * f), int(y + (ny - y) * f)
                if 0 <= px < c.w and 0 <= py < c.h:
                    m[py, px] = True
            x, y = nx, ny
            if not (0 <= x < c.w and 0 <= y < c.h):
                break
            if rng.random() < branch and n > 3:
                todo.append((x, y, a + rng.choice([-1, 1]) * rng.uniform(0.5, 1.0), n // 2))
    return m & c.alpha


def lichtenberg(c, rng, count):
    """Fern-like branching scars (static, for the body)."""
    return bolts(c, rng, count, 10, 1.5 * c.u, jitter=0.9, branch=0.3)


def _area(c):
    return max(1.0, c.alpha.sum() / float(c.u * c.u))


def paint(look, c):
    rng, u = c.rng, c.u
    mottle = noise(c.h, c.w, 6 * u, rng, 2)
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    c.extra["col"] = col
    c.extra["look"] = look
    n = max(2, int(_area(c) / 260))
    eye_col = col((220, 240, 255))
    if look == "tesla":
        rgb = ramp(even([(10, 14, 24), (34, 44, 66), (80, 96, 124), (150, 166, 190)]), c.lum * 0.65 + mottle * 0.3)
        scar = lichtenberg(c, rng, n) & ~c.eye
        rgb = np.where(scar[..., None], rgb * 0.5 + col((150, 190, 255)) * 0.5, rgb)
        c.extra["bolt"] = (col((240, 248, 255)), col((110, 170, 255)))
    elif look == "plasma":
        rgb = ramp(even([(14, 6, 24), (46, 24, 74), (100, 70, 140), (170, 150, 200)]), c.lum * 0.5 + mottle * 0.4)
        cx, cy, r = centre_of(c.face, c.alpha)
        c.extra["core"] = (cx, cy, max(1.5 * u, min(r * 0.45, 3 * u)))
        d = np.sqrt((c.xx - cx) ** 2 + (c.yy - cy) ** 2)
        heart = (d <= c.extra["core"][2]) & c.alpha & ~c.eye
        rgb = np.where(heart[..., None], col((255, 220, 255)), rgb)
        c.shine(heart, col((255, 200, 255)), 1.0)
        c.extra["bolt"] = (col((255, 200, 255)), col((200, 90, 255)))
        eye_col = col((255, 190, 255))
    elif look == "welding":
        rgb = ramp(even([(16, 14, 14), (54, 46, 42), (110, 98, 90), (170, 160, 150)]), c.lum * 0.6 + mottle * 0.35)
        temper = np.clip(1 - np.abs(mottle - 0.5) * 6, 0, 1)[..., None]     # blue-gold heat tint bands
        rgb = rgb * (1 - 0.35 * temper) + np.array([90, 80, 160], np.float32) * 0.35 * temper
        seam = (outline(c.alpha, 1, 30 * u * u) | ((np.abs((c.hm * 6) % 1 - 0.5) < 0.03) & c.alpha)) & ~c.eye
        bead = seam & (((c.xx + c.yy) // max(1, u)) % 2 == 0)
        rgb = np.where(seam[..., None], col((255, 150, 60)), rgb)
        rgb = np.where(bead[..., None], col((255, 236, 190)), rgb)
        c.shine(seam, col((255, 140, 40)), 0.8)
        c.shine(bead, col((255, 240, 200)), 1.0)
        c.extra["seam"] = seam
        eye_col = col((255, 230, 170))
    elif look == "storm":
        cloud = noise(c.h, c.w, 10 * u, rng, 3)
        rgb = ramp(even([(26, 28, 36), (64, 68, 82), (120, 126, 140), (196, 200, 210)]), c.lum * 0.35 + cloud * 0.6)
        c.extra["bolt"] = (col((255, 250, 200)), col((255, 210, 70)))
        eye_col = col((255, 245, 170))
    elif look == "ladder":
        rgb = ramp(even([(8, 8, 16), (30, 30, 48), (70, 70, 96), (130, 130, 160)]), c.lum * 0.6 + mottle * 0.3)
        rail = (np.abs((c.xx / (8.0 * u)) % 1 - 0.5) < 0.06) & c.alpha & ~c.eye   # copper electrode rails
        rgb = np.where(rail[..., None], np.array([196, 120, 60], np.float32), rgb)
        c.extra["bolt"] = (col((235, 225, 255)), col((150, 110, 255)))
        eye_col = col((200, 180, 255))
    elif look == "ball_lightning":
        rgb = ramp(even([(6, 8, 26), (22, 30, 70), (60, 80, 140), (130, 150, 210)]), c.lum * 0.6 + mottle * 0.3)
        ys, xs = np.nonzero(c.alpha & ~c.eye)
        orbs = []
        for _ in range(max(2, n)):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            orbs.append((float(xs[k]), float(ys[k]), rng.uniform(1.2, 2.4) * u))
        c.extra["orbs"] = orbs
        core = np.zeros_like(c.alpha)
        for ox, oy, r in orbs:
            core |= (np.sqrt((c.xx - ox) ** 2 + (c.yy - oy) ** 2) <= r)
        core &= c.alpha & ~c.eye
        rgb = np.where(core[..., None], col((230, 250, 255)), rgb)
        c.shine(core, col((200, 245, 255)), 1.0)
        c.extra["bolt"] = (col((230, 250, 255)), col((80, 200, 255)))
        eye_col = col((200, 250, 255))
    else:
        rgb = c.a[..., :3]
    rgb = np.where(c.eye[..., None], eye_col, rgb)
    c.shine(c.eye, eye_col, 1.0)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    """A fresh set of arcs every frame on top of the look's steady lights."""
    look = c.extra.get("look")
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    rng = np.random.default_rng((c.seed * 7919 + frame * 104729) % (2 ** 32))
    u = c.u
    n = max(2, int(_area(c) / 260))

    def put(mask, colour, strength):
        nonlocal g, grgb
        m = mask & c.alpha & ~c.eye
        upd = m & (strength > g)
        g = np.where(upd, strength, g)
        grgb = np.where(upd[..., None], np.asarray(colour, np.float32), grgb)

    if look == "welding":
        seam = c.extra["seam"]
        g = np.where(seam, g * [1.0, 0.75, 0.9, 0.6][frame % 4], g)
        sy, sx = np.nonzero(dilate(seam, 2 * u) & c.alpha)
        sparks = np.zeros_like(c.alpha)
        if len(sx):
            k = rng.integers(len(sx), size=max(4, len(sx) // 12))
            sparks[sy[k], sx[k]] = True
        put(sparks, c.extra["col"]((255, 200, 90)), 1.0)
    elif "bolt" in c.extra:
        core_c, halo_c = c.extra["bolt"]
        if look == "storm":
            m = bolts(c, rng, max(1, n // 2), 14, 2.0 * u, angle=math.pi / 2, jitter=0.8, branch=0.18)
        elif look == "ladder":
            band = (frame / 4.0) % 1.0
            starts = []
            ys, xs = np.nonzero(c.alpha & (np.abs(((c.hm - band) * 3) % 1 - 0.5) < 0.04))
            for _ in range(n):
                if len(xs):
                    k = rng.integers(len(xs))
                    starts.append((float(xs[k]), float(ys[k])))
            m = bolts(c, rng, len(starts), 8, 1.5 * u, angle=0.0 if rng.random() < 0.5 else math.pi, jitter=0.6,
                      branch=0.05, starts=starts)
        elif look == "plasma":
            cx, cy, r = c.extra["core"]
            starts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in rng.uniform(0, 2 * math.pi, 5)]
            m = bolts(c, rng, len(starts), 10, 1.5 * u, jitter=0.5, branch=0.08, starts=starts)
            m |= bolts(c, rng, max(1, n // 2), 6, 1.5 * u, jitter=0.6, branch=0.05)
        elif look == "ball_lightning":
            starts, m = [], np.zeros_like(c.alpha)
            for ox, oy, r in c.extra["orbs"]:
                for a in rng.uniform(0, 2 * math.pi, 3):
                    starts.append((ox + r * math.cos(a), oy + r * math.sin(a)))
            if starts:
                m = bolts(c, rng, len(starts), 3, 1.0 * u, jitter=1.0, branch=0.2, starts=starts)
            g = np.where(g0 > 0, g0 * [1.0, 0.8, 1.0, 0.7][frame % 4], g)
        else:
            m = bolts(c, rng, n, 10, 1.6 * u, jitter=0.75, branch=0.15)
        put(dilate(m, max(1, u // 2)), halo_c, 0.55)
        put(m, core_c, 1.0)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
