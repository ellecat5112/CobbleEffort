"""Animated previews: renders the model + animations to GIFs/PNGs (needs Pillow).

This is a small software renderer (orthographic, painter's algorithm, one quad
per texel so the texture shows). It understands the same Bedrock geometry and
animation data that Cobblemon loads, including the Molang expressions the
generator writes, so you can eyeball every animation before launching the game.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from .model import Geometry
from .textures import RGBAImage
from .util import CobbleEffortError

try:
    from PIL import Image, ImageDraw  # type: ignore
except Exception:  # pragma: no cover
    Image = None
    ImageDraw = None

Mat = list[list[float]]


# ------------------------------------------------------------------ math


def _mul(a: Mat, b: Mat) -> Mat:
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def _ident() -> Mat:
    return [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]


def _trans(x: float, y: float, z: float) -> Mat:
    m = _ident()
    m[0][3], m[1][3], m[2][3] = x, y, z
    return m


def _scale(x: float, y: float, z: float) -> Mat:
    m = _ident()
    m[0][0], m[1][1], m[2][2] = x, y, z
    return m


def _rot(rx: float, ry: float, rz: float) -> Mat:
    """Euler ZYX (three.js / Blockbench): R = Rz * Ry * Rx, angles in degrees."""
    x, y, z = (math.radians(v) for v in (rx, ry, rz))
    cx, sx, cy, sy, cz, sz = math.cos(x), math.sin(x), math.cos(y), math.sin(y), math.cos(z), math.sin(z)
    Rx = [[1, 0, 0, 0], [0, cx, -sx, 0], [0, sx, cx, 0], [0, 0, 0, 1]]
    Ry = [[cy, 0, sy, 0], [0, 1, 0, 0], [-sy, 0, cy, 0], [0, 0, 0, 1]]
    Rz = [[cz, -sz, 0, 0], [sz, cz, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    return _mul(Rz, _mul(Ry, Rx))


def _apply(m: Mat, p: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = p
    return (m[0][0] * x + m[0][1] * y + m[0][2] * z + m[0][3],
            m[1][0] * x + m[1][1] * y + m[1][2] * z + m[1][3],
            m[2][0] * x + m[2][1] * y + m[2][2] * z + m[2][3])


# ---------------------------------------------------------------- molang

_MOLANG_FUNCS = {
    "sin": lambda d: math.sin(math.radians(d)),
    "cos": lambda d: math.cos(math.radians(d)),
    "abs": abs,
    "clamp": lambda v, lo, hi: max(lo, min(hi, v)),
    "lerp": lambda a, b, t: a + (b - a) * t,
    "sqrt": lambda v: math.sqrt(max(0.0, v)),
    "min": min, "max": max, "floor": math.floor, "ceil": math.ceil, "round": round,
    "pow": pow, "mod": lambda a, b: a % b if b else 0.0,
    "pi": math.pi,
}
_EXPR_CACHE: dict[str, Any] = {}


def eval_molang(expr: Any, t: float) -> float:
    if isinstance(expr, (int, float)):
        return float(expr)
    if not isinstance(expr, str):
        return 0.0
    code = _EXPR_CACHE.get(expr)
    if code is None:
        s = expr.lower()
        s = re.sub(r"\b(?:q|query)\.(?:anim_time|life_time)\b", "T", s)
        s = re.sub(r"\bmath\.(\w+)", r"\1", s)
        s = re.sub(r"\b(?:q|query|v|variable|t|temp|c|context)\.\w+", "0", s)
        try:
            code = compile(s, "<molang>", "eval")
        except SyntaxError:
            code = compile("0", "<molang>", "eval")
        _EXPR_CACHE[expr] = code
    try:
        return float(eval(code, {"__builtins__": {}}, {**_MOLANG_FUNCS, "T": t}))
    except Exception:
        return 0.0


def _vec(v: Any, t: float, default: float) -> list[float]:
    if isinstance(v, dict):
        v = v.get("post", v.get("pre", [default] * 3))
    if isinstance(v, (int, float, str)):
        v = [v, v, v]
    return [eval_molang(x, t) for x in v]


def sample_channel(track: Any, t: float, default: float) -> list[float]:
    if isinstance(track, (list, int, float, str)):
        return _vec(track, t, default)
    if not isinstance(track, dict) or not track:
        return [default] * 3
    keys = sorted(track.items(), key=lambda kv: float(kv[0]))
    times = [float(k) for k, _ in keys]
    if t <= times[0]:
        return _vec(keys[0][1], t, default)
    if t >= times[-1]:
        last = keys[-1][1]
        return _vec(last["post"] if isinstance(last, dict) and "post" in last else last, t, default)
    for i in range(len(times) - 1):
        if times[i] <= t <= times[i + 1]:
            a = keys[i][1]
            b = keys[i + 1][1]
            av = _vec(a["post"] if isinstance(a, dict) and "post" in a else a, t, default)
            bv = _vec(b["pre"] if isinstance(b, dict) and "pre" in b else b, t, default)
            f = (t - times[i]) / (times[i + 1] - times[i] or 1)
            f = f * f * (3 - 2 * f)  # smoothstep stands in for catmull-rom
            return [av[j] + (bv[j] - av[j]) * f for j in range(3)]
    return [default] * 3


# --------------------------------------------------------------- render


def _face_quads(cube: dict, tw: int, th: int):
    """Yield (corners[4] in bedrock model space, (u, v) texel) for each texel of each face."""
    ox, oy, oz = (float(c) for c in cube["origin"])
    sx, sy, sz = (float(c) for c in cube["size"])
    inf = float(cube.get("inflate", 0) or 0)
    x0, y0, z0 = ox - inf, oy - inf, oz - inf
    x1, y1, z1 = ox + sx + inf, oy + sy + inf, oz + sz + inf
    uv = cube.get("uv", [0, 0])
    mirror = bool(cube.get("mirror", False))
    # face -> (u, v, uw, vh) rectangles
    if isinstance(uv, list):
        u, v = float(uv[0]), float(uv[1])
        w, h, d = math.floor(sx), math.floor(sy), math.floor(sz)
        rects = {
            "north": (u + d, v + d, w, h), "south": (u + 2 * d + w, v + d, w, h),
            "east": (u, v + d, d, h), "west": (u + d + w, v + d, d, h),
            "up": (u + d, v, w, d), "down": (u + d + w, v, w, d),
        }
        if mirror:
            rects["east"], rects["west"] = rects["west"], rects["east"]
    else:
        rects = {}
        for f, e in uv.items():
            rects[f] = (float(e["uv"][0]), float(e["uv"][1]), float(e["uv_size"][0]), float(e["uv_size"][1]))
    # face geometry: origin corner + two edge vectors spanning (u -> right, v -> down) on the texture
    faces = {
        "north": ((x1, y1, z0), (x0 - x1, 0, 0), (0, y0 - y1, 0)),
        "south": ((x0, y1, z1), (x1 - x0, 0, 0), (0, y0 - y1, 0)),
        "east": ((x1, y1, z1), (0, 0, z0 - z1), (0, y0 - y1, 0)),
        "west": ((x0, y1, z0), (0, 0, z1 - z0), (0, y0 - y1, 0)),
        "up": ((x1, y1, z1), (x0 - x1, 0, 0), (0, 0, z0 - z1)),
        "down": ((x1, y0, z0), (x0 - x1, 0, 0), (0, 0, z1 - z0)),
    }
    for f, (o, eu, ev) in faces.items():
        if f not in rects:
            continue
        ru, rv, rw, rh = rects[f]
        nu = max(1, min(32, int(round(abs(rw))))) if abs(rw) >= 1 else 1
        nv = max(1, min(32, int(round(abs(rh))))) if abs(rh) >= 1 else 1
        for i in range(nu):
            for j in range(nv):
                a0, a1 = i / nu, (i + 1) / nu
                b0, b1 = j / nv, (j + 1) / nv
                pts = []
                for a, b in ((a0, b0), (a1, b0), (a1, b1), (a0, b1)):
                    pts.append((o[0] + eu[0] * a + ev[0] * b, o[1] + eu[1] * a + ev[1] * b, o[2] + eu[2] * a + ev[2] * b))
                tu = ru + (i + 0.5) / nu * rw
                tv = rv + (j + 0.5) / nv * rh
                yield f, pts, (tu, tv)


class Renderer:
    def __init__(self, geo: Geometry, texture: RGBAImage | None, size: int = 256, yaw: float = 35, pitch: float = 20):
        if Image is None:
            raise CobbleEffortError("Previews need Pillow: pip install pillow")
        self.geo = geo
        self.tex = texture
        self.size = size
        self.view = _mul(_rot(pitch, 0, 0), _rot(0, yaw, 0))
        # pre-build quads per bone in Blockbench/three.js space (bedrock X flipped)
        self.quads: dict[str, list] = {}
        tw, th = geo.texture_width, geo.texture_height
        for b in geo.bones:
            qs = []
            for c in b.get("cubes", []):
                cm = _ident()
                if c.get("rotation"):
                    p = c.get("pivot", [0, 0, 0])
                    pv = (-float(p[0]), float(p[1]), float(p[2]))
                    r = c["rotation"]
                    cm = _mul(_trans(*pv), _mul(_rot(-float(r[0]), -float(r[1]), float(r[2])), _trans(-pv[0], -pv[1], -pv[2])))
                for face, pts, (tu, tv) in _face_quads(c, tw, th):
                    pts = [_apply(cm, (-x, y, z)) for x, y, z in pts]
                    qs.append((face, pts, self._texel(tu, tv)))
            self.quads[b["name"]] = qs
        lo, hi = geo.bounds()
        self.extent = max(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2], 8) * 1.25
        self.centre_y = (lo[1] + hi[1]) / 2

    def _texel(self, u: float, v: float) -> tuple[int, int, int, int]:
        if not self.tex:
            return (200, 200, 200, 255)
        tw, th = self.geo.texture_width, self.geo.texture_height
        x = int(u / tw * self.tex.width) % self.tex.width
        y = int(v / th * self.tex.height) % self.tex.height
        return self.tex.pixels[y * self.tex.width + x]

    def bone_matrices(self, anim: dict | None, t: float) -> dict[str, Mat]:
        bones_anim = (anim or {}).get("bones", {})
        mats: dict[str, Mat] = {}
        for b in self.geo.bones:  # parents come first
            name = b["name"]
            p = b.get("pivot", [0, 0, 0])
            pv = (-float(p[0]), float(p[1]), float(p[2]))
            r = [float(x) for x in b.get("rotation", [0, 0, 0])]
            ba = bones_anim.get(name, {})
            ar = sample_channel(ba.get("rotation"), t, 0.0) if "rotation" in ba else [0.0, 0.0, 0.0]
            ap = sample_channel(ba.get("position"), t, 0.0) if "position" in ba else [0.0, 0.0, 0.0]
            asc = sample_channel(ba.get("scale"), t, 1.0) if "scale" in ba else [1.0, 1.0, 1.0]
            local = _mul(_trans(-ap[0], ap[1], ap[2]),
                         _mul(_trans(*pv), _mul(_rot(-(r[0] + ar[0]), -(r[1] + ar[1]), r[2] + ar[2]),
                                                _mul(_scale(*asc), _trans(-pv[0], -pv[1], -pv[2])))))
            parent = mats.get(b.get("parent")) if b.get("parent") else None
            mats[name] = _mul(parent, local) if parent else local
        return mats

    def frame(self, anim: dict | None, t: float, ss: int = 2) -> "Image.Image":
        S = self.size * ss
        img = Image.new("RGBA", (S, S), (32, 36, 44, 255))
        draw = ImageDraw.Draw(img)
        # ground line
        k = S / self.extent
        cy = S * 0.5 + self.centre_y * k * 0.9
        mats = self.bone_matrices(anim, t)
        polys = []
        light = (0.35, 0.8, -0.5)
        for name, qs in self.quads.items():
            m = _mul(self.view, mats[name])
            for face, pts, col in qs:
                if col[3] < 16:
                    continue
                tp = [_apply(m, p) for p in pts]
                # normal for culling + shading
                ax, ay, az = (tp[1][i] - tp[0][i] for i in range(3))
                bx, by, bz = (tp[3][i] - tp[0][i] for i in range(3))
                nx, ny, nz = ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx
                ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
                nx, ny, nz = nx / ln, ny / ln, nz / ln
                shade = 0.55 + 0.45 * abs(nx * light[0] + ny * light[1] + nz * light[2])
                depth = sum(p[2] for p in tp) / 4
                scr = [(S / 2 - p[0] * k, cy - p[1] * k) for p in tp]
                polys.append((depth, scr, tuple(int(c * shade) for c in col[:3])))
        polys.sort(key=lambda x: -x[0])
        for _, scr, col in polys:
            draw.polygon(scr, fill=col + (255,))
        draw.line([(0, cy), (S, cy)], fill=(90, 100, 110, 255), width=ss)
        return img.resize((self.size, self.size), Image.LANCZOS)


def render_previews(geo: Geometry, texture: RGBAImage | None, animations: dict[str, dict], out_dir: Path,
                    group: str, size: int = 200, fps: int = 12) -> list[Path]:
    """Writes one GIF per animation plus a contact sheet PNG. Returns written files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    r = Renderer(geo, texture, size=size)
    written: list[Path] = []
    sheet_frames: list[tuple[str, "Image.Image"]] = [("rest", r.frame(None, 0))]
    for full, anim in animations.items():
        short = full.split(".")[-1]
        length = float(anim.get("animation_length", 1.0) or 1.0)
        n = max(2, min(48, int(length * fps)))
        frames = [r.frame(anim, length * i / n).convert("P", palette=Image.ADAPTIVE) for i in range(n)]
        if anim.get("loop") is not True:
            frames += [frames[-1]] * (fps // 2)
        gif = out_dir / f"{group}_{short}.gif"
        frames[0].save(gif, save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0, disposal=2)
        written.append(gif)
        mid = 0.25 * length if anim.get("loop") is True else 0.5 * length
        if short in ("faint", "sleep"):
            mid = length * 0.99
        sheet_frames.append((short, r.frame(anim, mid)))
    cols = 4
    rows = (len(sheet_frames) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * size, rows * (size + 18)), (20, 22, 28, 255))
    d = ImageDraw.Draw(sheet)
    for i, (label, im) in enumerate(sheet_frames):
        x, y = (i % cols) * size, (i // cols) * (size + 18)
        sheet.paste(im, (x, y + 18))
        d.text((x + 6, y + 3), label, fill=(230, 230, 230, 255))
    sp = out_dir / f"{group}_contact_sheet.png"
    sheet.save(sp)
    written.append(sp)
    return written
