"""Rowlet line (Grass/Flying -> Fire/Electric, Decidueye Fire/Dark, Hisuian Fire/Psychic): natural disaster, a
firestorm. The leaf bowtie, Dartrix's leaf hair and Decidueye's leaves and hat burn."""
from __future__ import annotations

from _materials import Charred, Flame

LINE = ["rowlet", "dartrix", "decidueye"]
RECOLOUR = {"dst": 20, "dst_shiny": 46, "width": 50}


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    fire = Flame("flames")
    kit.reskin(fire, *kit.named("bowtie", "hair", "head_leaf", "hat"))
    if kit.model.startswith("decidueye"):
        kit.reskin(Charred("flames"), *kit.named("cloak"))                # a scorched cloak, embers at its edges
    head = kit.find("head")
    lo, hi = kit.bbox(head)
    kit.cross(head, ((lo[0] + hi[0]) / 2, hi[1] - 0.5, (lo[2] + hi[2]) / 2), (hi[0] - lo[0]) * 0.5, (hi[1] - lo[1]) * 0.6, fire)
