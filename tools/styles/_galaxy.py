"""
Star Wars collection: Pokemon from a galaxy far, far away (inspired by Star Wars; original patterns, no film art).

Looks (one per line, three lines each):
  jedi        a cream tunic and belt under a brown robe, a blue saber blade glowing at the side
  sith        a black robe with a dark red undertone, a red blade and red glowing eyes
  trooper     white armour plates with black seams and grey details
  beskar      polished silver armour plates with a dark visor band and a leather belt
  astromech   a white droid shell with blue panels and blinking lights
  rebel       an orange flight suit with a white vest harness and a striped helmet top
Emissive layer (KYBER) for the blades, lights and eyes.
Shiny: the other side: a green blade, a purple blade, black shadow armour, gold beskar, red panels, a green suit.
"""
from __future__ import annotations

import numpy as np

from ._cosmic import even, noise, ramp
from ._fx import make as _make

KYBER = {"name": "kyber", "emissive": True, "translucent": True, "frames": 4, "fps": 6}


def mat(c, colour, k=0.5):
    return np.asarray(colour, np.float32) * (1 - k / 2 + k * c.lum[..., None])


def plates(c, n=7):
    """Armour panel seams: horizontal bands by height plus vertical joints."""
    row = (c.hm * n) % 1
    joint = ((c.xx // max(1, 4 * c.u)) % 2 == 0) & ((c.xx % max(1, 4 * c.u)) < max(1, c.u // 2))
    return (row < 0.07) | joint


def blade(c):
    """A vertical saber blade down the side of the chest (or the texture's middle if there is no torso hint)."""
    if c.face.torso:
        x, y, w, h = c.face.torso
        bx, y0, y1 = x + w * 0.85, y, y + h
    else:
        bx, y0, y1 = c.w * 0.5, c.h * 0.3, c.h * 0.7
    return (np.abs(c.xx - bx) <= max(0.6, 0.45 * c.u)) & (c.yy >= y0) & (c.yy <= y1)


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    s = c.shiny
    glow_m, gcol, eyes = np.zeros_like(c.alpha), (120, 200, 255), None
    if look == "jedi":
        rgb = np.where((c.hm > 0.35)[..., None], mat(c, (222, 202, 160)), mat(c, (112, 76, 48)))
        belt = (np.abs(c.hm - 0.42) < 0.025) & body
        rgb = np.where(belt[..., None], mat(c, (80, 54, 34)), rgb)
        glow_m = blade(c) & body
        gcol = (120, 255, 110) if s else (110, 190, 255)
    elif look == "sith":
        rgb = ramp(even([(6, 4, 6), (30, 14, 16), (70, 30, 34)]), c.lum * 0.6 + noise(c.h, c.w, 6 * u, rng, 2) * 0.3)
        glow_m = blade(c) & body
        gcol = (190, 80, 255) if s else (255, 30, 30)
        eyes = gcol
    elif look == "trooper":
        armour = (40, 40, 46) if s else (238, 238, 236)
        rgb = mat(c, armour, 0.35)
        rgb = np.where((plates(c) & body)[..., None], np.array([20, 20, 24] if not s else [200, 200, 210], np.float32), rgb)
        detail = (np.abs(c.hm - 0.62) < 0.015) & body
        rgb = np.where(detail[..., None], np.array([130, 130, 136], np.float32), rgb)
    elif look == "beskar":
        metal = even([(60, 40, 10), (170, 120, 40), (240, 200, 90), (255, 240, 190)]) if s else \
            even([(50, 54, 60), (130, 136, 146), (200, 206, 214), (245, 248, 252)])
        refl = 0.5 + 0.5 * np.sin(c.hm * 12 + c.xx / (8.0 * u))
        rgb = ramp(metal, c.lum * 0.5 + refl * 0.4)
        rgb = np.where((plates(c, 6) & body)[..., None], rgb * 0.55, rgb)
        belt = (np.abs(c.hm - 0.4) < 0.025) & body
        rgb = np.where(belt[..., None], mat(c, (110, 76, 46)), rgb)
        if c.face.front:
            x, y, w, h = c.face.front
            visor = (c.yy >= y + h * 0.35) & (c.yy <= y + h * 0.5) & (c.xx >= x) & (c.xx < x + w) & body
            rgb = np.where(visor[..., None], np.array([16, 16, 20], np.float32), rgb)
    elif look == "astromech":
        panel = (200, 40, 40) if s else (40, 80, 200)
        rgb = mat(c, (240, 240, 244), 0.35)
        g = 4 * u
        cell = (((c.xx // g) + 2 * (c.yy // g)) % 5 == 0) & ((c.xx % g) > 0) & ((c.yy % g) > 0)
        rgb = np.where((cell & body)[..., None], mat(c, panel, 0.3), rgb)
        lights = (rng.random((c.h, c.w)) < 0.01) & body
        rgb = np.where(lights[..., None], np.array([255, 60, 60], np.float32), rgb)
        glow_m = lights
        gcol = (255, 80, 80)
    elif look == "rebel":
        suit = (60, 150, 70) if s else (232, 112, 30)
        rgb = mat(c, suit)
        if c.face.torso:
            x, y, w, h = c.face.torso
            strap = ((np.abs(c.xx - (x + w * 0.3)) <= max(0.6, 0.5 * u)) | (np.abs(c.xx - (x + w * 0.7)) <= max(0.6, 0.5 * u))) \
                & (c.yy >= y) & (c.yy <= y + h) & body
            rgb = np.where(strap[..., None], mat(c, (240, 240, 236), 0.3), rgb)
        helmet = (c.hm > 0.85) & body
        rgb = np.where(helmet[..., None], mat(c, (240, 240, 236), 0.3), rgb)
        stripe = helmet & (np.abs(((c.xx / (3.0 * u)) % 1) - 0.5) < 0.12)
        rgb = np.where(stripe[..., None], mat(c, (200, 40, 30), 0.3), rgb)
    else:
        rgb = c.a[..., :3]
    glow_m &= body
    rgb = np.where(glow_m[..., None], np.asarray(gcol, np.float32) * 0.6 + 100, rgb)
    c.shine(glow_m, gcol, 1.0)
    if eyes is not None:
        rgb = np.where(c.eye[..., None], np.asarray(eyes, np.float32), rgb)
        c.shine(c.eye, eyes, 1.0)
    else:
        rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.extra["glow_m"] = glow_m
    c.extra["blink"] = look == "astromech"
    return rgb


def animate(glow, frame, c):
    m = c.extra["glow_m"]
    if c.extra["blink"]:
        rng = np.random.default_rng((c.seed + frame * 17) % (2 ** 32))
        return np.where(m, glow * (rng.random(glow.shape) < 0.6), glow)
    return np.where(m, glow * [1.0, 0.85, 0.95, 0.8][frame % 4], glow)                # the blade hums


def make(look):
    return _make(paint, look, animate, paint_layers=True)
