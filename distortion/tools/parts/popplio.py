"""Popplio line (Water -> Grass, Primarina Grass/Steel): plant inspiration, flowers. The ruffs are petals, flowers
bloom on Brionne's and Primarina's heads and Primarina's stars are golden pollen."""
from __future__ import annotations

from _materials import PETAL_RAMP, Cutout, Remap, petal

LINE = ["popplio", "brionne", "primarina"]
RECOLOUR = {"dst": 110, "dst_shiny": 80, "width": 55}
BLOOM = Cutout(petal, *PETAL_RAMP)


def build(kit):
    kit.reskin(Remap(*PETAL_RAMP), *kit.named("front_ruff", "back_ruff", "left_ruff", "right_ruff", "ruff", "torso_ruff"))
    if kit.model == "primarina":
        kit.reskin(Remap([(170, 120, 20), (240, 200, 60), (255, 246, 180)], [(150, 150, 170), (220, 220, 236), (255, 255, 255)]), *kit.named("star"))
    if kit.model in ("brionne", "primarina"):
        head = "head_angle" if kit.has("head_angle") else "head"
        lo, hi = kit.bbox(head)
        for dx in (-2.5, 2.5):
            kit.cross(head, (dx, hi[1] - 0.3, (lo[2] + hi[2]) / 2), 3, 3, BLOOM, turn=20)
