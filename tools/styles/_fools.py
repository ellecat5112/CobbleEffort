"""
April Fools' Day collection: Pokemon playing pranks.

Looks (one per line, three lines each):
  jester   a red-and-yellow harlequin diamond motley
  clown    clown white with big bright polka dots and a red nose on the face
  googly   its own colours, but covered in wobbly googly eyes (its real eyes too), which look around
  swapped  "wrong colours": every colour swapped round the colour wheel, a prank palette
  mosaic   pixelated into chunky blocks, as if the game forgot to load it
  confetti its own colours showered with party confetti and streamers that twinkle
Emissive layer (PRANK) for the twinkling confetti and the googly eyes' look-around.
Shiny: the prank colours turned round the colour wheel (swapped: back the other way).
"""
from __future__ import annotations

import numpy as np

from ._cosmic import centre_of, hue_turn_fast
from ._fx import make as _make

PRANK = {"name": "prank", "emissive": True, "translucent": True, "frames": 4, "fps": 3}
BRIGHT = [(230, 40, 40), (250, 200, 30), (40, 160, 230), (60, 190, 80), (230, 90, 200), (250, 130, 30)]


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    orig = c.a[..., :3]
    lit = (0.75 + 0.35 * c.lum)[..., None]
    keep_eyes = True
    if look == "jester":
        g = 3 * u
        d = (((c.xx + c.yy) // g + (c.xx - c.yy) // g) % 2) == 0
        rgb = np.where(d[..., None], col((210, 30, 40)), col((250, 200, 40))) * lit
    elif look == "clown":
        rgb = np.array([248, 246, 244], np.float32) * lit
        g = 5 * u
        jx, jy = (c.xx // g) * g + g / 2, (c.yy // g) * g + g / 2
        dot = np.hypot(c.xx - jx, c.yy - jy) <= max(1.0, 1.4 * u)
        which = ((c.xx // g) * 7 + (c.yy // g) * 3).astype(int) % len(BRIGHT)
        pal = np.stack([col(b) for b in BRIGHT])
        rgb = np.where(dot[..., None], pal[which] * lit, rgb)
        if c.face.front:
            x, y, w, h = c.face.front
            nose = np.hypot(c.xx - (x + w / 2), c.yy - (y + h * 0.6)) <= max(1.2, min(w, h) * 0.14)
            rgb = np.where((nose & body)[..., None], np.array([230, 20, 30], np.float32), rgb)
    elif look == "googly":
        rgb = orig.copy()
        eyes = []
        ys, xs = np.nonzero(body)
        for _ in range(max(4, int(c.alpha.sum() / float(u * u) / 110))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            eyes.append((float(xs[k]), float(ys[k]), max(2.6, rng.uniform(1.2, 2.0) * u)))
        c.extra["googly"] = eyes
        rgb = draw_googly(c, rgb, eyes, 0)
        eye_white = c.eye
        rgb = np.where(eye_white[..., None], np.array([250, 250, 250], np.float32), rgb)
        pupil = c.eye & ((c.xx + c.yy) % 3 == 0)
        rgb = np.where(pupil[..., None], np.array([10, 10, 10], np.float32), rgb)
        keep_eyes = False
    elif look == "swapped":
        rgb = hue_turn_fast(orig, -0.5 if c.shiny else 0.5)
        mean = rgb.mean(-1, keepdims=True)
        rgb = np.clip(mean + (rgb - mean) * 1.3, 0, 255)
    elif look == "mosaic":
        b = max(5, 4 * u)
        H, W = (c.h // b) * b, (c.w // b) * b
        blocks = orig.copy()
        if H and W:
            sm = orig[:H, :W].reshape(H // b, b, W // b, b, 3).mean((1, 3))
            blocks[:H, :W] = np.repeat(np.repeat(sm, b, 0), b, 1)
        blocks = np.round(blocks / 48.0) * 48.0                                      # crunchy, few colours
        rgb = hue_turn_fast(blocks, turn) if turn else blocks
        grid = ((c.xx % b) == 0) | ((c.yy % b) == 0)
        rgb = np.where((grid & body)[..., None], rgb * 0.88, rgb)
    elif look == "confetti":
        rgb = orig.copy()
        conf = (rng.random((c.h, c.w)) < 0.05) & body
        which = rng.integers(len(BRIGHT), size=(c.h, c.w))
        pal = np.stack([col(b) for b in BRIGHT])
        rgb = np.where(conf[..., None], pal[which], rgb)
        streamer = (np.abs(np.sin(c.xx / (2.0 * u) + c.yy / (5.0 * u))) < 0.12) & body
        rgb = np.where(streamer[..., None], col((240, 90, 200)), rgb)
        c.extra["confetti"] = conf
    else:
        rgb = orig
    if keep_eyes:
        rgb = np.where(c.eye[..., None], orig, rgb)
    return rgb


def draw_googly(c, rgb, eyes, frame):
    for i, (x, y, r) in enumerate(eyes):
        d = np.hypot(c.xx - x, c.yy - y)
        white = (d <= r) & c.alpha & ~c.eye
        rgb = np.where(white[..., None], np.array([250, 250, 250], np.float32), rgb)
        rim = white & (d > r - max(0.5, 0.25 * c.u))
        rgb = np.where(rim[..., None], np.array([30, 30, 30], np.float32), rgb)
        a = (i * 2.1 + frame * 1.6)
        px, py = x + np.cos(a) * r * 0.4, y + np.sin(a) * r * 0.4
        pupil = (np.hypot(c.xx - px, c.yy - py) <= r * 0.5) & white
        rgb = np.where(pupil[..., None], np.array([10, 10, 10], np.float32), rgb)
    return rgb


def animate(glow, frame, c):
    if "confetti" in c.extra:
        rng = np.random.default_rng((c.seed * 97 + frame) % (2 ** 32))
        m = c.extra["confetti"] & (rng.random(glow.shape) < 0.4)
        c.glow_rgb = np.where(m[..., None], np.array([255, 240, 200], np.float32), c.glow_rgb)
        return np.where(m, 0.7, glow)
    if "googly" in c.extra:                                                         # the pupils roll around
        img = draw_googly(c, np.zeros((c.h, c.w, 3), np.float32), c.extra["googly"], frame)
        m = (img.sum(-1) > 0) & c.alpha & ~c.eye
        c.glow_rgb = np.where(m[..., None], img, c.glow_rgb)
        return np.where(m, 0.55, glow)
    return glow


def make(look):
    return _make(paint, look, animate, paint_layers=True)
