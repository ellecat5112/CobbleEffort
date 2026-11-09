"""Turtwig line (Grass -> Fire, Torterra Fire/Water): natural disaster, a volcano. Turtwig's sprout is a flame, Grotle's
bushes are smouldering lava rocks with fire on top, and Torterra's tree is an erupting volcano (every tree variant): a
stepped cone of rock and lava, a molten crater and an eruption plume; its shell spikes are cooling lava."""
from __future__ import annotations

from _materials import Flame, Glow, LavaRock, Rock

LINE = ["turtwig", "grotle", "torterra"]
RECOLOUR = {"dst": 22, "dst_shiny": 46, "width": 55}
UNIFY = True                      # all of Torterra's trees become the one volcano


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    fire, lava = Flame("flames"), LavaRock("flames")
    if kit.model == "turtwig":
        kit.reskin(fire, "twig", "leaf_left", "leaf_right")
    elif kit.model == "grotle":
        kit.reskin(lava, "bush_left", "bush_right")
        for b in ("bush_left", "bush_right"):
            lo, hi = kit.bbox(b)
            kit.cross(b, ((lo[0] + hi[0]) / 2, hi[1] - 0.5, (lo[2] + hi[2]) / 2), 5, 8, fire)
    elif kit.model == "torterra":
        kit.hide("tree", "leaves2", "outerleaves2")
        kit.reskin(lava, *kit.named("spike"))
        cx, cz, y = 6.0, 2.0, 27.0
        rock = Rock()
        for w, h, mat in ((26, 5, rock), (20, 5, rock), (14, 5, lava), (10, 4, lava)):
            kit.box("torso", [cx - w / 2, y, cz - w / 2], [w, h, w], mat)
            y += h
        kit.flat("torso", (cx, y + 0.05, cz), 7, 7, Glow("flames"))          # the molten crater
        kit.cross("torso", (cx, y, cz), 11, 20, fire)                      # the eruption
        kit.cross("torso", (cx - 2, y, cz + 1), 6, 13, Flame("flames", tongues=1.1), turn=40)
        kit.cross("torso", (cx + 2, y, cz - 1), 6, 15, Flame("flames", tongues=1.3), turn=-35)
