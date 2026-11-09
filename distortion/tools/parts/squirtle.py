"""Squirtle line (Water -> Grass): plant inspiration, prototaxites (the giant fungi of the Devonian). Banded fungal
trunks rise from the shell, the curled tail is a fern's fiddlehead; Wartortle's fluffy ears and tail turn to lichen;
Blastoise's cannons give way to two towering prototaxite pillars."""
from __future__ import annotations

from _materials import Bands, Cutout, fern, leaf, midrib

LINE = ["squirtle", "wartortle", "blastoise"]
RECOLOUR = {"dst": 88, "dst_shiny": 60, "width": 55, "sat": 0.8, "val": 0.95}   # blue skin -> mossy green

TRUNK = Bands([(198, 172, 130), (226, 208, 170), (170, 140, 102), (236, 222, 190)],
              [(176, 186, 150), (206, 216, 188), (146, 158, 128), (226, 232, 208)], period=2)
FERN = Cutout(fern, [(46, 104, 40), (86, 160, 62), (150, 210, 110)], [(70, 110, 120), (110, 170, 160), (180, 230, 210)])
LICHEN = Cutout(leaf, [(110, 128, 92), (158, 176, 128), (206, 220, 176)], [(120, 120, 150), (170, 170, 200), (220, 220, 240)], veins=midrib)


def pillar(kit, bone, x, y, z, w, h):
    """A prototaxite trunk: banded, with a rounded (slightly wider) top."""
    kit.box(bone, [x - w / 2, y, z - w / 2], [w, h, w], TRUNK)
    kit.box(bone, [x - w / 2, y + h, z - w / 2], [w, 1, w], TRUNK, inflate=0.4)


def build(kit):
    if kit.model == "squirtle":
        lo, hi = kit.bbox("torso")
        z = hi[2]
        pillar(kit, "torso", -2.0, 7, z, 2, 11)
        pillar(kit, "torso", 1.5, 6, z + 0.5, 2, 8)
        pillar(kit, "torso", 3.5, 5, z - 0.5, 1, 6)
        kit.reskin(FERN, "tail", "tail_bend")
    elif kit.model == "wartortle":
        lo, hi = kit.bbox("shell")
        z = hi[2] - 1
        pillar(kit, "shell", -2.5, 10, z, 3, 15)
        pillar(kit, "shell", 2.0, 9, z + 0.5, 2, 11)
        pillar(kit, "shell", 4.5, 7, z - 1, 2, 8)
        kit.reskin(LICHEN, "ear_left", "ear_right")
        kit.reskin(FERN, "tail", "tail_bend")
    else:
        # the cannons give way to two towering trunks, and a stand of smaller ones grows on the shell
        up = kit.upright("shell")
        for side in ("left", "right"):
            lo, hi = kit.wbox(f"shell_cannon_{side}")
            kit.hide(f"cannon_{side}")
            x, z = (lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2
            pillar(kit, up, x, hi[1] - 4, z, 6, 30)
        lo, hi = kit.wbox("shell")
        for x, dz, y, w, h in ((0, -3, 34, 4, 22), (-7, -4, 30, 3, 15), (7, -4, 31, 3, 13), (-3, -2, 24, 2, 10), (4, -2, 22, 2, 9)):
            pillar(kit, up, x, y, hi[2] + dz, w, h)
