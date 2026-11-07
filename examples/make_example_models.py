"""Generates the example Blockbench models used by the example project and tests.

Run:  python examples/make_example_models.py
It writes .bbmodel files (Blockbench 4 format, Bedrock Entity, box UV,
embedded texture) for a quadruped (Emberpup), its evolution (Blazehound, as a
.geo.json + .png to show that path), and a bird (Skylark).
"""

from __future__ import annotations

import base64
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cobbleeffort.model import load_model  # noqa: E402
from cobbleeffort.textures import RGBAImage  # noqa: E402


class Builder:
    """Tiny Blockbench project builder (coordinates are Blockbench's, i.e. pre-export)."""

    def __init__(self, name: str, tex_size: int = 64):
        self.name = name
        self.tex = tex_size
        self.elements: list[dict] = []
        self.u = 0
        self.v = 0
        self.row_h = 0
        self.paint: list[tuple[int, int, int, int, tuple]] = []  # u, v, w, h, colour

    def _uv(self, size: list[float], colour: tuple) -> list[int]:
        w = int(2 * (size[0] + size[2]) + 0.999)
        h = int(size[1] + size[2] + 0.999)
        if self.u + w > self.tex:
            self.u = 0
            self.v += self.row_h
            self.row_h = 0
        uv = [self.u, self.v]
        self.paint.append((self.u, self.v, w, h, colour))
        self.u += w
        self.row_h = max(self.row_h, h)
        return uv

    def cube(self, name: str, frm: list[float], to: list[float], colour: tuple, rotation=None, origin=None) -> str:
        size = [to[i] - frm[i] for i in range(3)]
        e = {
            "name": name, "box_uv": True, "rescale": False, "locked": False,
            "from": frm, "to": to, "autouv": 0, "color": 0,
            "origin": origin or [(frm[i] + to[i]) / 2 for i in range(3)],
            "uv_offset": self._uv(size, colour), "faces": {f: {"uv": [0, 0, 0, 0], "texture": 0}
                                                         for f in ("north", "east", "south", "west", "up", "down")},
            "type": "cube", "uuid": str(uuid.uuid4()),
        }
        if rotation:
            e["rotation"] = rotation
        self.elements.append(e)
        return e["uuid"]

    @staticmethod
    def group(name: str, origin: list[float], children: list, rotation=None) -> dict:
        g = {"name": name, "origin": origin, "color": 0, "uuid": str(uuid.uuid4()), "export": True,
             "mirror_uv": False, "isOpen": True, "locked": False, "visibility": True, "autouv": 0,
             "children": children}
        if rotation:
            g["rotation"] = rotation
        return g

    def texture(self, eye_colour=(20, 20, 30, 255)) -> RGBAImage:
        px = [(0, 0, 0, 0)] * (self.tex * self.tex)
        for u, v, w, h, col in self.paint:
            for y in range(v, min(self.tex, v + h)):
                for x in range(u, min(self.tex, u + w)):
                    shade = 1.0 - 0.18 * ((x + y) % 3 == 0) - 0.1 * (y - v > h * 0.6)
                    px[y * self.tex + x] = (int(col[0] * shade), int(col[1] * shade), int(col[2] * shade), 255)
        return RGBAImage(self.tex, self.tex, px)

    def save(self, path: Path, outliner: list, embed: bool = True) -> RGBAImage:
        img = self.texture()
        data = {
            "meta": {"format_version": "4.10", "model_format": "bedrock", "box_uv": True},
            "name": self.name, "model_identifier": self.name, "visible_box": [2, 2, 0],
            "resolution": {"width": self.tex, "height": self.tex},
            "elements": self.elements, "outliner": outliner,
            "textures": [], "animations": [],
        }
        if embed:
            data["textures"].append({
                "path": "", "name": f"{self.name}.png", "folder": "", "namespace": "", "id": "0",
                "width": self.tex, "height": self.tex, "uv_width": self.tex, "uv_height": self.tex,
                "particle": False, "render_mode": "default", "visible": True, "mode": "bitmap",
                "saved": True, "uuid": str(uuid.uuid4()),
                "source": "data:image/png;base64," + base64.b64encode(img.to_png_bytes()).decode(),
            })
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=1))
        return img


def quadruped(name: str, s: float = 1.0, main=(220, 90, 40, 255), accent=(250, 200, 70, 255)) -> tuple[Builder, list]:
    b = Builder(name)
    S = lambda *v: [round(x * s, 3) for x in v]  # noqa: E731
    # Blockbench +X is the model's RIGHT (it flips on export), so left parts sit at -X here.
    legs = []
    for nm, x, z in (("leg_front_left", -2, -3), ("leg_front_right", 2, -3),
                     ("leg_back_left", -2, 3), ("leg_back_right", 2, 3)):
        c = b.cube(nm, S(x - 1, 0, z - 1), S(x + 1, 6, z + 1), main)
        paw = b.cube(nm + "_paw", S(x - 1.2, 0, z - 1.5), S(x + 1.2, 1, z + 0.5), accent)
        legs.append(b.group(nm, S(x, 6, z), [c, b.group(nm.replace("leg", "paw"), S(x, 1, z), [paw])]))
    body_c = b.cube("body", S(-3, 6, -5), S(3, 11, 5), main)
    head_c = b.cube("head", S(-3, 9, -10), S(3, 14, -5), main)
    snout = b.cube("snout", S(-1.5, 9, -12), S(1.5, 11, -10), accent)
    jaw_c = b.cube("jaw", S(-1.5, 8, -11.5), S(1.5, 9, -8), accent)
    eye_l = b.cube("eye", S(-2.5, 11.5, -10.1), S(-1.5, 12.5, -10), (20, 20, 30, 255))
    eye_r = b.cube("eye", S(1.5, 11.5, -10.1), S(2.5, 12.5, -10), (20, 20, 30, 255))
    ear_l = b.cube("ear", S(-3, 14, -8), S(-1, 17, -7), accent)
    ear_r = b.cube("ear", S(1, 14, -8), S(3, 17, -7), accent)
    t1 = b.cube("tail", S(-1, 9, 5), S(1, 11, 9), main)
    t2 = b.cube("tail2", S(-1, 9.2, 9), S(1, 10.8, 13), accent)
    flame = b.cube("flame", S(-1.5, 9, 13), S(1.5, 13, 15), (255, 160, 30, 255))
    head = b.group("head", S(0, 11, -5), [
        head_c, snout,
        b.group("jaw", S(0, 9, -8), [jaw_c]),
        b.group("eye_left", S(-2, 12, -10), [eye_l]),
        b.group("eye_right", S(2, 12, -10), [eye_r]),
        b.group("ear_left", S(-2, 14, -7.5), [ear_l]),
        b.group("ear_right", S(2, 14, -7.5), [ear_r]),
    ])
    tail = b.group("tail", S(0, 10, 5), [t1, b.group("tail2", S(0, 10, 9), [t2, b.group("flame", S(0, 11, 13), [flame])])])
    body = b.group("body", S(0, 8, 0), [body_c, b.group("neck", S(0, 10, -4), [head]), tail])
    root = b.group(name, [0, 0, 0], [body] + legs)
    return b, [root]


def bird(name: str) -> tuple[Builder, list]:
    b = Builder(name)
    blue, white, orange = (70, 120, 220, 255), (235, 235, 245, 255), (240, 150, 40, 255)
    body_c = b.cube("body", [-2.5, 4, -3], [2.5, 9, 3], blue)
    belly = b.cube("belly", [-2, 4.5, -3.2], [2, 8, -2.9], white)
    head_c = b.cube("head", [-2, 9, -4], [2, 13, 0], blue)
    beak = b.cube("beak", [-0.75, 10, -6], [0.75, 11, -4], orange)
    beak_low = b.cube("beak_lower", [-0.75, 9.5, -5.5], [0.75, 10, -4], orange)
    eye_l = b.cube("eye", [-2.05, 11, -3], [-2, 12, -2], (15, 15, 20, 255))
    eye_r = b.cube("eye", [2, 11, -3], [2.05, 12, -2], (15, 15, 20, 255))
    wl = b.cube("wing", [-3.5, 5, -2], [-2.5, 9, 3], blue)
    wl_tip = b.cube("wing_tip", [-3.5, 4, 3], [-2.5, 8, 6], white)
    wr = b.cube("wing", [2.5, 5, -2], [3.5, 9, 3], blue)
    wr_tip = b.cube("wing_tip", [2.5, 4, 3], [3.5, 8, 6], white)
    tail_c = b.cube("tail", [-1.5, 5, 3], [1.5, 6, 8], blue)
    legs = []
    for nm, x in (("leg_left", -1), ("leg_right", 1)):
        c = b.cube(nm, [x - 0.5, 0, -0.5], [x + 0.5, 4, 0.5], orange)
        legs.append(b.group(nm, [x, 4, 0], [c]))
    head = b.group("head", [0, 9, -1], [head_c, beak, b.group("jaw", [0, 10, -4], [beak_low]),
                                          b.group("eye_left", [-2, 11.5, -2.5], [eye_l]),
                                          b.group("eye_right", [2, 11.5, -2.5], [eye_r])])
    wing_l = b.group("wing_left", [-2.5, 8.5, 0], [wl, b.group("wing_left_tip", [-3, 7, 3], [wl_tip])])
    wing_r = b.group("wing_right", [2.5, 8.5, 0], [wr, b.group("wing_right_tip", [3, 7, 3], [wr_tip])])
    body = b.group("body", [0, 6, 0], [body_c, belly, head, wing_l, wing_r, b.group("tail", [0, 5.5, 3], [tail_c])])
    return b, [b.group(name, [0, 0, 0], [body] + legs)]


def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    b, outliner = quadruped("emberpup")
    b.save(out / "emberpup.bbmodel", outliner)

    # The evolution: bigger, delivered as Bedrock .geo.json + .png (the other supported input)
    b2, outliner2 = quadruped("blazehound", s=1.6, main=(170, 40, 30, 255), accent=(255, 210, 60, 255))
    img2 = b2.save(out / "_blazehound_tmp.bbmodel", outliner2, embed=False)
    geo = load_model(out / "_blazehound_tmp.bbmodel")
    (out / "blazehound.geo.json").write_text(json.dumps(geo.to_geo_json("blazehound"), indent=1))
    img2.save(out / "blazehound.png")
    (out / "_blazehound_tmp.bbmodel").unlink()

    b3, outliner3 = bird("skylark")
    b3.save(out / "skylark.bbmodel", outliner3)
    print(f"Example models written to {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "models")
