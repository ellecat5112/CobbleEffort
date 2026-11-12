"""
"2D sprite" collections (collection config "mode": "sprite"): the Pokémon becomes a flat, layered Game Boy sprite.

For every look Cobblemon can resolve for a species (each combination of its variations' aspects: shiny, female,
regional forms, megas...), the model is posed in its idle pose (the standing pose's animations at time 0, its hidden
parts hidden) and rendered here, front and back, at one pixel per model unit, in a few depth slices. Each slice is
reduced to four Game Boy tones (dark outlines, a little ordered dithering): the classic green screen, or for shinies
a Game Boy Color palette taken from the shiny texture. The slices become flat planes stacked a little apart (a
pop-up of layered 2D artwork: head-on it is the sprite, at an angle the layers separate) in a model of our own, with a
poser of our own (the original's portrait/profile framing, an 8-bit bob when idle and a hop when walking). No foreign
art is read: only Cobblemon's and derivative mods' models, posers, animations and textures (the Stack's rules).

Everything here is deterministic (a software renderer, no GPU), so reruns produce identical files.
"""
from __future__ import annotations

import colorsys
import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image

DMG = [(15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15)]   # darkest .. lightest
SLICES = 3
GAP = 2.0                       # model units between the layers
GROUP = "cobbleeffort_gbsprite"  # our animation group (bob, hop, cry)
BAYER = np.array([[0, 2], [3, 1]]) / 4.0


# ---------------------------------------------------------------------------------------------
# pose: the standing pose's animations at time 0
# ---------------------------------------------------------------------------------------------

def _molang(expr):
    if isinstance(expr, (int, float)):
        return float(expr)
    s = str(expr).lower()
    s = re.sub(r"\b(q|query|v|variable|t|temp)\.[a-z_]+", "0", s)
    s = s.replace("math.pi", str(math.pi))
    env = {"sin": lambda d: math.sin(math.radians(d)), "cos": lambda d: math.cos(math.radians(d)),
           "abs": abs, "clamp": lambda v, a, b: max(a, min(b, v)), "lerp": lambda a, b, t: a + (b - a) * t,
           "min": min, "max": max, "sqrt": math.sqrt, "floor": math.floor, "ceil": math.ceil, "round": round,
           "mod": lambda a, b: a % b if b else 0, "pow": pow, "exp": math.exp}
    s = s.replace("math.", "")
    try:
        return float(eval(s, {"__builtins__": {}}, env))        # Cobblemon's own animation files (trusted data)
    except Exception:
        return 0.0


def _at_zero(channel):
    """A bone channel's value at time 0: [x, y, z] or keyframes {"0.0": [..] | {"post": [..]}}."""
    if channel is None:
        return None
    if isinstance(channel, dict) and channel:
        try:
            first = min(channel, key=lambda k: float(k))
        except ValueError:
            return None
        v = channel[first]
        if isinstance(v, dict):
            v = v.get("pre", v.get("post"))
        channel = v
    if isinstance(channel, (int, float, str)):
        channel = [channel] * 3
    if not isinstance(channel, list) or len(channel) != 3:
        return None
    return [_molang(c) for c in channel]


def load_pose(stack, poser_id, kotlin_dir, kotlin_convert, find_model_class):
    """(poser json dict or None, {bone: {"rotation": [..], "position": [..]}}, {hidden bone names})."""
    data = None
    hit = stack.poser(poser_id) if poser_id else None
    if hit is not None:
        data = hit[0].json(hit[1])
    elif poser_id and poser_id.startswith("cobblemon:") and kotlin_dir is not None:
        kt = find_model_class(kotlin_dir, poser_id.split(":", 1)[1])
        if kt:
            data, _ = kotlin_convert(kt.read_text())
    bones, hidden = {}, set()
    if not data:
        return None, bones, hidden
    poses = data.get("poses", {})
    stand = next((p for p in poses.values() if "STAND" in p.get("poseTypes", [])), None) or next(iter(poses.values()), {})
    for a in stand.get("animations", []):
        m = re.search(r"bedrock\(\s*'([^']+)'\s*,\s*'([^']+)'", str(a)) or re.search(r"bedrock\(\s*([\w]+)\s*,\s*([\w]+)", str(a))
        if not m:
            continue
        group, name = m.group(1), m.group(2)
        ahit = stack.anim(group)
        if ahit is None:
            continue
        anims = ahit[0].json(ahit[1]).get("animations", {})
        anim = anims.get(f"animation.{group}.{name}")
        if not anim:
            continue
        for bone, ch in anim.get("bones", {}).items():
            cur = bones.setdefault(bone, {"rotation": [0, 0, 0], "position": [0, 0, 0]})
            for key in ("rotation", "position"):
                v = _at_zero(ch.get(key))
                if v:
                    cur[key] = [a + b for a, b in zip(cur[key], v)]
    for part in stand.get("transformedParts", []):
        name = part.get("part")
        if not name:
            continue
        if part.get("isVisible") is False:
            hidden.add(name)
        cur = bones.setdefault(name, {"rotation": [0, 0, 0], "position": [0, 0, 0]})
        for key in ("rotation", "position"):
            if isinstance(part.get(key), list) and len(part[key]) == 3:
                cur[key] = [a + float(b) for a, b in zip(cur[key], part[key])]
    return data, bones, hidden


# ---------------------------------------------------------------------------------------------
# a software renderer for Cobblemon (Bedrock) geometry, as the preview's three.js scene builds it
# ---------------------------------------------------------------------------------------------

def _rot(deg_xyz):
    """three.js Euler (rad(-x), rad(-y), rad(z)) in order 'ZYX' -> Rz @ Ry @ Rx."""
    a, b, c = math.radians(-deg_xyz[0]), math.radians(-deg_xyz[1]), math.radians(deg_xyz[2])
    rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return rz @ ry @ rx


def _P(v):
    v = v or [0, 0, 0]
    return np.array([-float(v[0]), float(v[1]), float(v[2])])


def _mat(R, t):
    M = np.eye(4)
    M[:3, :3] = R
    M[:3, 3] = t
    return M


# three.js BoxGeometry face planes: (u axis, v axis, w axis, udir, vdir, which size is width/height/depth, depth sign)
_PLANES = [("z", "y", "x", -1, -1, ("d", "h", "w"), 1), ("z", "y", "x", 1, -1, ("d", "h", "w"), -1),
           ("x", "z", "y", 1, 1, ("w", "d", "h"), 1), ("x", "z", "y", 1, -1, ("w", "d", "h"), -1),
           ("x", "y", "z", 1, -1, ("w", "h", "d"), 1), ("x", "y", "z", -1, -1, ("w", "h", "d"), -1)]
_AX = {"x": 0, "y": 1, "z": 2}


def faces_of(geo, pose_bones, hidden):
    """Every visible cube face in model (three) space: (4 corners (TL, TR, BL, BR) as 3-vectors, uv rect)."""
    bones = geo.get("bones", [])
    by = {b["name"]: b for b in bones}
    pivots = {b["name"]: _P(b.get("pivot")) for b in bones}
    world = {}

    def hidden_up(name):
        while name:
            if name in hidden:
                return True
            name = by.get(name, {}).get("parent")
        return False

    def world_of(name):
        if name in world:
            return world[name]
        b = by[name]
        parent = b.get("parent") if b.get("parent") in by else None
        pw = world_of(parent) if parent else np.eye(4)
        pp = pivots[parent] if parent else np.zeros(3)
        rest = list(b.get("rotation") or [0, 0, 0])
        anim = pose_bones.get(name, {})
        rot = [r + a for r, a in zip(rest, anim.get("rotation", [0, 0, 0]))]
        pos = pivots[name] - pp + _P(anim.get("position", [0, 0, 0]))
        world[name] = pw @ _mat(_rot(rot), pos)
        return world[name]

    out = []
    for b in bones:
        if b["name"].startswith("locator") or hidden_up(b["name"]):
            continue
        W = world_of(b["name"])
        for c in b.get("cubes", []):
            uv = c.get("uv")
            if not isinstance(uv, list):
                continue
            inf = c.get("inflate", 0) or 0
            sx, sy, sz = (float(v) for v in c["size"])
            dims = {"w": sx + 2 * inf, "h": sy + 2 * inf, "d": sz + 2 * inf}
            o = c["origin"]
            centre = np.array([-(o[0] + sx / 2), o[1] + sy / 2, o[2] + sz / 2])
            if c.get("rotation"):
                cp = _P(c.get("pivot"))
                M = W @ _mat(_rot(c["rotation"]), cp - pivots[b["name"]]) @ _mat(np.eye(3), centre - cp)
            else:
                M = W @ _mat(np.eye(3), centre - pivots[b["name"]])
            u, v = uv
            w, h, d = sx, sy, sz
            rects = [[u, v + d, d, h], [u + d + w, v + d, d, h], [u + d + w, v + d, -w, -d], [u + d + 2 * w, v, -w, d],
                     [u + 2 * d + w, v + d, w, h], [u + d, v + d, w, h]]
            if c.get("mirror"):
                rects = [rects[1], rects[0], rects[2], rects[3], rects[4], rects[5]]
                rects = [[f[0] + f[2], f[1], -f[2], f[3]] for f in rects]
            for (ua, va, wa, udir, vdir, (wk, hk, dk), dsign), rect in zip(_PLANES, rects):
                fw, fh, fd = dims[wk], dims[hk], dims[dk]
                corners = []
                for iy in (0, 1):
                    for ix in (0, 1):
                        p = np.zeros(3)
                        p[_AX[ua]] = (ix * fw - fw / 2) * udir
                        p[_AX[va]] = (iy * fh - fh / 2) * vdir
                        p[_AX[wa]] = fd / 2 * dsign
                        corners.append((M @ np.append(p, 1))[:3])
                out.append((corners, rect))
    return out


def rasterize(faces, tex, tw, th, back=False, zrange=None, bounds=None):
    """Render faces orthographically (front: looking +z from in front, image x = -x; back: from behind) at 1 px per
    unit. Only fragments with depth in zrange are drawn. Returns (RGBA uint8 array, depth array, bounds)."""
    T = np.asarray(tex.convert("RGBA"))
    TH, TW = T.shape[:2]
    sxu, syv = TW / tw, TH / th                                     # texture pixels per UV unit
    pts = np.array([c for cs, _ in faces for c in cs])
    if bounds is None:
        xs = -pts[:, 0]
        bounds = (math.floor(xs.min()), math.ceil(xs.max()), math.floor(pts[:, 1].min()), math.ceil(pts[:, 1].max()))
    x0, x1, y0, y1 = bounds
    W, H = max(1, x1 - x0), max(1, y1 - y0)
    col = np.zeros((H, W, 4), np.uint8)
    dep = np.full((H, W), np.inf)
    for corners, (u, v, w, h) in faces:
        P = np.array(corners)
        X = (P[:, 0] if back else -P[:, 0]) - (x0 if not back else -x1)
        Y = y1 - P[:, 1]
        Z = -P[:, 2] if back else P[:, 2]
        o, a, b = np.array([X[0], Y[0]]), np.array([X[1] - X[0], Y[1] - Y[0]]), np.array([X[2] - X[0], Y[2] - Y[0]])
        det = a[0] * b[1] - a[1] * b[0]
        if abs(det) < 1e-9:
            continue                                                # edge-on
        cx0, cx1 = max(0, int(math.floor(X.min()))), min(W, int(math.ceil(X.max())))
        cy0, cy1 = max(0, int(math.floor(Y.min()))), min(H, int(math.ceil(Y.max())))
        if cx1 <= cx0 or cy1 <= cy0:
            continue
        gx, gy = np.meshgrid(np.arange(cx0, cx1) + 0.5, np.arange(cy0, cy1) + 0.5)
        dx, dy = gx - o[0], gy - o[1]
        s = (dx * b[1] - dy * b[0]) / det
        t = (a[0] * dy - a[1] * dx) / det
        inside = (s >= -1e-6) & (s <= 1 + 1e-6) & (t >= -1e-6) & (t <= 1 + 1e-6)
        if not inside.any():
            continue
        z = Z[0] + s * (Z[1] - Z[0]) + t * (Z[2] - Z[0])
        if zrange is not None:
            inside &= (z >= zrange[0]) & (z < zrange[1])
        tu = np.clip(np.floor((u + np.clip(s, 0, 0.9999) * w) * sxu), 0, TW - 1).astype(int)
        tv = np.clip(np.floor((v + np.clip(t, 0, 0.9999) * h) * syv), 0, TH - 1).astype(int)
        texel = T[tv, tu]
        ok = inside & (texel[..., 3] > 25)
        sub_d = dep[cy0:cy1, cx0:cx1]
        win = ok & (z < sub_d)
        sub_d[win] = z[win]
        sub_c = col[cy0:cy1, cx0:cx1]
        sub_c[win] = texel[win]
    return col, dep, bounds


# ---------------------------------------------------------------------------------------------
# Game Boy look
# ---------------------------------------------------------------------------------------------

def gbc_palette(img: Image.Image):
    """A Game Boy Color sprite palette from a texture: white, a light and a dark shade of its most common strong
    hue, and near-black."""
    a = np.asarray(img.convert("RGBA")).reshape(-1, 4)
    a = a[a[:, 3] > 25][:, :3] / 255.0
    best, hue = -1, 0.0
    hist = np.zeros(24)
    for r, g, b in a[:: max(1, len(a) // 4000)]:
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        if s > 0.25 and 0.15 < l < 0.85:
            hist[int(h * 24) % 24] += s
    if hist.sum() > 0:
        hue = (int(np.argmax(hist)) + 0.5) / 24
    conv = lambda h, l, s: tuple(int(c * 255) for c in colorsys.hls_to_rgb(h, l, s))
    return [(24, 20, 28), conv(hue, 0.32, 0.65), conv(hue, 0.66, 0.7), (248, 248, 240)]


def gameboy(images, depths, palette):
    """Quantize RGBA layer images to the palette's 4 tones (index 0 darkest): outlines in the darkest tone (round
    each layer and wherever the depth jumps between parts, as sprites outline overlapping limbs), the rest by
    brightness against the whole sprite's spread, shaded a little from the depth (lit from the top left), with 2x2
    ordered dithering at the tone boundaries."""
    lums = []
    for im, dp in zip(images, depths):
        lum = 0.299 * im[..., 0] + 0.587 * im[..., 1] + 0.114 * im[..., 2]
        d = np.where(np.isfinite(dp), dp, np.nan)
        gy, gx = np.gradient(np.nan_to_num(d, nan=np.nanmean(d) if np.isfinite(d).any() else 0.0))
        gx, gy = np.clip(gx, -2, 2), np.clip(gy, -2, 2)
        n = np.stack([-gx, -gy, np.ones_like(gx)], -1)
        n /= np.linalg.norm(n, axis=-1, keepdims=True)
        light = np.array([-0.45, -0.55, 1.0])
        light /= np.linalg.norm(light)
        lam = np.clip((n * light).sum(-1), 0, 1)
        lums.append(lum * (0.72 + 0.36 * lam))
    allv = np.concatenate([l[im[..., 3] > 0] for l, im in zip(lums, images)]) if images else np.array([0.0])
    if allv.size == 0:
        allv = np.array([0.0])
    lo, hi = np.percentile(allv, 6), np.percentile(allv, 94)
    out = []
    pal = np.array(palette, np.uint8)
    for im, lum, dp in zip(images, lums, depths):
        a = im[..., 3] > 0
        n = np.clip((lum - lo) / max(hi - lo, 1e-6), 0, 1)
        H, W = a.shape
        yy, xx = np.mgrid[0:H, 0:W]
        dth = BAYER[yy % 2, xx % 2] - 0.375
        tone = np.clip(1 + np.floor(n * 2.999 + dth * 0.5), 1, 3).astype(int)   # tones 1..3 inside
        tone[(lum < 40) & a] = 0                                                # very dark texels: black
        pad = np.pad(a, 1)
        edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        dpad = np.pad(np.where(a, dp, np.inf), 1, constant_values=np.inf)
        for sl in ((slice(None, -2), slice(1, -1)), (slice(1, -1), slice(None, -2))):
            nb = dpad[sl[0], sl[1]]
            jump = a & np.isfinite(nb) & (nb - dp > 1.5)                       # a part in front of its neighbour
            edge |= jump
        for sl in ((slice(2, None), slice(1, -1)), (slice(1, -1), slice(2, None))):
            nb = dpad[sl[0], sl[1]]
            edge |= a & np.isfinite(nb) & (nb - dp > 1.5)
        tone[edge] = 0
        rgba = np.zeros((H, W, 4), np.uint8)
        rgba[..., :3] = pal[tone]
        rgba[..., 3] = np.where(a, 255, 0)
        out.append(rgba)
    return out


# ---------------------------------------------------------------------------------------------
# a sprite: render, stylise, build the layered model
# ---------------------------------------------------------------------------------------------

def build_sprite(geo, tex: Image.Image, pose_bones, hidden, shiny_palette_from: Image.Image | None):
    d = geo["description"]
    tw, th = float(d["texture_width"]), float(d["texture_height"])
    faces = faces_of(geo, pose_bones, hidden)
    if not faces:
        return None
    _, depth, bounds = rasterize(faces, tex, tw, th)
    zs = np.array([c[2] for cs, _ in faces for c in cs])
    z0, z1 = zs.min() - 0.01, zs.max() + 0.01
    cuts = np.linspace(z0, z1, SLICES + 1)
    fronts, backs, fd, bd = [], [], [], []
    for k in range(SLICES):
        f, fdep, _ = rasterize(faces, tex, tw, th, False, (cuts[k], cuts[k + 1]), bounds)
        b, bdep, _ = rasterize(faces, tex, tw, th, True, (-cuts[k + 1], -cuts[k]), bounds)
        fronts.append(f)
        backs.append(b)
        fd.append(fdep)
        bd.append(bdep[:, ::1])
    keep = [k for k in range(SLICES) if fronts[k][..., 3].any() or backs[k][..., 3].any()]
    palette = gbc_palette(shiny_palette_from) if shiny_palette_from is not None else DMG
    styled = gameboy([fronts[k] for k in keep] + [backs[k] for k in keep], [fd[k] for k in keep] + [bd[k] for k in keep],
                     palette)
    n = len(keep)
    x0, x1, y0, y1 = bounds
    W, H = x1 - x0, y1 - y0
    atlas = np.zeros((H * n, 2 * W, 4), np.uint8)
    for i in range(n):
        atlas[i * H:(i + 1) * H, :W] = styled[i]
        atlas[i * H:(i + 1) * H, W:] = styled[n + i]
    centre_z = (z0 + z1) / 2
    planes = []
    for i, k in enumerate(keep):
        z = centre_z + (i - (n - 1) / 2) * GAP                     # front slice nearest the viewer (-z)
        planes.append({"origin": [float(x0), float(y0), round(float(z), 3)], "size": [float(W), float(H), 0.0], "uv": [0, i * H]})
    return Image.fromarray(atlas, "RGBA"), planes, (2 * W, H * n)


def model_json(name, planes, tex_size):
    W, H = tex_size
    bones = [{"name": "gbsprite", "pivot": [0, 0, 0]}, {"name": "sprite", "parent": "gbsprite", "pivot": [0, 0, 0]}]
    for i, p in enumerate(planes):
        bones.append({"name": f"layer{i}", "parent": "sprite", "pivot": [0, 0, 0], "cubes": [p]})
    return {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": f"geometry.{name}", "texture_width": W, "texture_height": H,
                        "visible_bounds_width": 4, "visible_bounds_height": 4, "visible_bounds_offset": [0, 1, 0]},
        "bones": bones}]}


def poser_json(original):
    out = {"rootBone": "gbsprite"}
    for k in ("portraitScale", "portraitTranslation", "profileScale", "profileTranslation"):
        if original and k in original:
            out[k] = original[k]
    out.setdefault("portraitScale", 1.0)
    out.setdefault("portraitTranslation", [0, 0, 0])
    out.setdefault("profileScale", 1.0)
    out.setdefault("profileTranslation", [0, 0, 0])
    out["animations"] = {"cry": f"q.bedrock_stateful('{GROUP}', 'cry')"}
    out["poses"] = {
        "standing": {"poseTypes": ["STAND", "NONE", "PORTRAIT", "PROFILE", "HOVER", "FLOAT", "SLEEP", "SHOULDER_LEFT",
                                   "SHOULDER_RIGHT", "OPEN"],
                     "animations": [f"q.bedrock('{GROUP}', 'idle')"]},
        "walking": {"poseTypes": ["WALK", "SWIM", "FLY", "GLIDE"], "animations": [f"q.bedrock('{GROUP}', 'walk')"]},
    }
    return out


def animations_json():
    def steps(times_values, length):
        return {f"{t:.2f}": [0, v, 0] for t, v in times_values}
    return {"format_version": "1.8.0", "animations": {
        # a two-frame 8-bit bob: up a pixel, down a pixel (keys just apart make it a step, not a glide)
        f"animation.{GROUP}.idle": {"loop": True, "animation_length": 1.0, "bones": {"sprite": {"position":
            steps([(0.0, 0), (0.49, 0), (0.5, 1), (0.99, 1), (1.0, 0)], 1.0)}}},
        # a hop on every step
        f"animation.{GROUP}.walk": {"loop": True, "animation_length": 0.5, "bones": {"sprite": {"position":
            steps([(0.0, 0), (0.12, 2), (0.24, 0), (0.25, 0), (0.37, 2), (0.49, 0), (0.5, 0)], 0.5)}}},
        # the cry: a quick jump
        f"animation.{GROUP}.cry": {"animation_length": 0.4, "bones": {"sprite": {"position":
            steps([(0.0, 0), (0.1, 3), (0.2, 0), (0.3, 2), (0.4, 0)], 0.4)}}},
    }}


def digest(*parts) -> str:
    return hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:10]
