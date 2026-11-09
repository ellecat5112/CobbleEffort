"""Oshawott line (Water -> Grass, Hisuian Samurott Grass/Fairy): plant inspiration, bamboo. The scalchop is a cut
bamboo slice, Samurott's helmet and seamitars are bamboo, Hisuian Samurott's horn a bamboo shoot."""
from __future__ import annotations

from _materials import BAMBOO_RAMP, LEAF_RAMP, Bands, Cutout, Remap, leaf, midrib

LINE = ["oshawott", "dewott", "samurott"]
RECOLOUR = {"dst": 95, "dst_shiny": 70, "width": 55}
BAMBOO = Remap(*BAMBOO_RAMP)
POLE = Bands([(126, 172, 62), (144, 192, 74), (126, 172, 62), (72, 112, 40)],
             [(110, 170, 150), (130, 190, 170), (110, 170, 150), (60, 110, 100)], period=2)
LEAVES = Cutout(leaf, *LEAF_RAMP, veins=midrib)


def build(kit):
    kit.reskin(BAMBOO, *kit.named("scalchop", "helmet", "seamitar"))
    if kit.model in ("oshawott", "dewott"):
        head = "head"
        lo, hi = kit.bbox(head)
        kit.cross(head, (2, hi[1] - 0.3, (lo[2] + hi[2]) / 2), 3, 5, LEAVES, turn=15)   # bamboo leaves sprouting
        kit.cross(head, (-1.5, hi[1] - 0.3, (lo[2] + hi[2]) / 2 + 1), 2.5, 4, LEAVES, turn=-30)
    else:
        lo, hi = kit.bbox("torso")                       # a stand of bamboo on Samurott's back, like a quiver
        up = kit.upright("torso")
        for dx, h in ((-2.5, 22), (0, 28), (2.5, 18)):
            kit.box(up, [dx - 1, hi[1] - 2, hi[2] - 3], [2, h, 2], POLE)
            kit.cross(up, (dx, hi[1] - 2 + h, hi[2] - 2), 4, 5, LEAVES, turn=dx * 10)
    if kit.model == "samurott_hisuian":
        kit.reskin(BAMBOO, *kit.named("bone"))
