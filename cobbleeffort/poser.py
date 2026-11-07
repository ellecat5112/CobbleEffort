"""Build the Cobblemon JSON poser that wires animations to pose types."""

from __future__ import annotations

from .animgen import AnimationSet
from .rig import Rig
from .util import num


def build_poser(group: str, rig: Rig, anims: AnimationSet, *, can_fly: bool, can_swim: bool, floats: bool,
                shoulder: bool, tweaks: dict | None = None) -> dict:
    tweaks = tweaks or {}

    def bed(name: str) -> str:
        return f"q.bedrock('{group}', '{name}')"

    look = [f"q.look('{rig.head}')"] if rig.head else []
    quirks = [f"q.bedrock_quirk('{group}', 'blink')"] if anims.has("blink") else []

    def pose(types: list[str], anim: str, *, battle: bool | None = None, with_look: bool = True,
             extra: dict | None = None) -> dict:
        p: dict = {"poseTypes": types}
        if battle is not None:
            p["isBattle"] = battle
        p["animations"] = (look if with_look else []) + [bed(anim)]
        if quirks and anim != "sleep":
            p["quirks"] = list(quirks)
        if extra:
            p.update(extra)
        return p

    stand_types = ["STAND", "NONE", "PORTRAIT", "PROFILE"]
    walk_types = ["WALK"]
    if shoulder:
        stand_types += ["SHOULDER_LEFT", "SHOULDER_RIGHT"]
    poses: dict[str, dict] = {}

    if floats and not anims.has("ground_idle"):
        stand_anim = "air_idle"
    else:
        stand_anim = "ground_idle"

    air = (can_fly or floats) and anims.has("air_idle")
    water = can_swim and anims.has("water_idle")
    hover_types = ["HOVER"]
    fly_types = ["FLY"]
    if not air:
        stand_types.append("HOVER")
        walk_types.append("FLY")
    if not water:
        # out of its element in water: fliers hover/fly, everyone else idles/walks
        (hover_types if air else stand_types).append("FLOAT")
        (fly_types if air else walk_types).append("SWIM")
    if floats and air:
        # levitators idle in the air even on the ground
        stand_anim = "air_idle"

    poses["standing"] = pose(stand_types, stand_anim, battle=False)
    poses["battle_idle"] = pose(["STAND"], "battle_idle" if anims.has("battle_idle") else stand_anim, battle=True)
    poses["walking"] = pose(walk_types, "air_fly" if (floats and air) else "ground_walk")
    if anims.has("sleep"):
        poses["sleep"] = pose(["SLEEP"], "sleep", with_look=False)
    if air:
        poses["hover"] = pose(hover_types, "air_idle")
        poses["fly"] = pose(fly_types, "air_fly")
        if rig.body and rig.body != rig.root:
            poses["fly"]["animations"].insert(0, f"q.pitch_tilt('{rig.body}')")
    if water:
        poses["float"] = pose(["FLOAT"], "water_idle")
        poses["swim"] = pose(["SWIM"], "water_swim")

    named: dict[str, str] = {}
    if anims.has("cry"):
        named["cry"] = f"q.bedrock_stateful('{group}', 'cry')"
    if anims.has("faint"):
        named["faint"] = f"q.bedrock_primary('{group}', 'faint', q.curve('one'))"
    if anims.has("recoil"):
        named["recoil"] = f"q.bedrock_stateful('{group}', 'recoil')"
    for move in ("physical", "special", "status"):
        if anims.has(move):
            named[move] = f"q.bedrock_primary('{group}', '{move}', q.curve('symmetrical_wide'))"

    # portrait / profile framing: derived from the model's size, overridable
    h_blocks = max(0.25, rig.height_px / 16.0)
    head_y = rig.height_px * 0.75
    portrait_scale = tweaks.get("portrait_scale", num(max(0.5, min(4.0, 1.9 / h_blocks)), 2))
    profile_scale = tweaks.get("profile_scale", num(max(0.25, min(1.2, 0.95 / h_blocks ** 0.5)), 2))
    poser = {
        "portraitScale": portrait_scale,
        "portraitTranslation": tweaks.get("portrait_translation",
                                          [0, num(-(head_y / 16.0) * 0.6 + 0.3, 2), 0]),
        "profileScale": profile_scale,
        "profileTranslation": tweaks.get("profile_translation", [0, num(0.62 + (1.0 - min(h_blocks, 2.0)) * 0.1, 2), 0]),
        "rootBone": rig.root,
        "animations": named,
        "poses": poses,
    }
    return poser
