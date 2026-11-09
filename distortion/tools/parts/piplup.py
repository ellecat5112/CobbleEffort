"""Piplup line (Water -> Grass, Empoleon Grass/Ground): plant inspiration, a pine forest. A pine sapling sprouts on
Piplup's head, Prinplup's crests are pine needles, Empoleon's crown is bark and its chest spikes are pinecone scales."""
from __future__ import annotations

from _materials import BARK_RAMP, PINE_RAMP, Cutout, Remap, pine

LINE = ["piplup", "prinplup", "empoleon"]
RECOLOUR = {"dst": 125, "dst_shiny": 90, "width": 55, "val": 0.85}
NEEDLES = Remap(*PINE_RAMP)
BARK = Remap(*BARK_RAMP)
PINE = Cutout(pine, *PINE_RAMP)


def build(kit):
    if kit.model == "piplup":
        lo, hi = kit.bbox("head")
        cz = (lo[2] + hi[2]) / 2
        kit.cross("head", (0, hi[1] - 0.2, cz), 5, 7, PINE)                   # a little pine on its head
    elif kit.model == "prinplup":
        kit.reskin(NEEDLES, "crests")
        lo, hi = kit.bbox("head")
        kit.cross("head", (0, hi[1] - 0.2, (lo[2] + hi[2]) / 2 + 1), 5, 8, PINE, turn=20)
    else:
        kit.reskin(BARK, *kit.named("crown"))
        kit.reskin(BARK, *kit.named("chest_spike"))
        for b in ("crown_front", "crown_left", "crown_right"):           # the crown's prongs are pine branches
            lo, hi = kit.bbox(b)
            kit.cross(b, ((lo[0] + hi[0]) / 2, hi[1] - 3, (lo[2] + hi[2]) / 2), 6, 8, PINE)
