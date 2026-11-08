"""
Converts a simple Cobblemon Kotlin ("inbuilt") poser into Cobblemon's JSON poser format.

Needed when a mod overwrites the model of a Pokémon whose Cobblemon poser is Kotlin code: the cosmetic pins a
vendored copy of Cobblemon's model, and a Kotlin poser can't be pinned under another id, so an equivalent JSON
poser is written instead. Only the constructs these simple models use are understood (portrait/profile framing,
single-bone look, bedrock animations and quirks, biped walk, battle conditions, hidden parts, transform ticks);
anything else is reported and skipped. Cobblemon's code is MPL-2.0, like this project's.
"""
from __future__ import annotations

import re
from pathlib import Path

POSE_SETS = {
    "ALL_POSES": ["STAND", "WALK", "SLEEP", "HOVER", "FLY", "FLOAT", "SWIM", "GLIDE", "SHOULDER_LEFT", "SHOULDER_RIGHT",
                  "PROFILE", "PORTRAIT", "NONE"],
    "FLYING_POSES": ["FLY", "HOVER"], "SWIMMING_POSES": ["SWIM", "FLOAT"], "STANDING_POSES": ["STAND", "WALK"],
    "SHOULDER_POSES": ["SHOULDER_LEFT", "SHOULDER_RIGHT"], "UI_POSES": ["PROFILE", "PORTRAIT"],
    "MOVING_POSES": ["WALK", "SWIM", "FLY"], "STATIONARY_POSES": ["STAND", "FLOAT", "HOVER"],
    "NO_GRAV_POSES": ["FLY", "HOVER", "SWIM"],
}


def find_model_class(kotlin_root: Path, poser_name: str) -> Path | None:
    repo = next(kotlin_root.rglob("VaryingModelRepository.kt"), None)
    if repo is None:
        return None
    m = re.search(r'inbuilt\(\s*"' + re.escape(poser_name) + r'"\s*,\s*::(\w+)\s*\)', repo.read_text())
    return next(kotlin_root.rglob(f"{m.group(1)}.kt"), None) if m else None


def _num(s: str) -> float:
    v = float(s.rstrip("Ff"))
    return int(v) if v == int(v) else v


def _vec(s: str):
    return [_num(x.strip()) for x in s.split(",")]


def _block(text: str, start: int) -> str:
    """The text inside the parentheses that open at text[start - 1]."""
    depth, i = 1, start
    while depth:
        depth += {"(": 1, ")": -1}.get(text[i], 0)
        i += 1
    return text[start:i - 1]


def convert(kt: str) -> tuple[dict, list[str]]:
    warnings = []
    kt = re.sub(r"//[^\n]*", "", kt)                          # commented-out code isn't code
    kt = re.sub(r"/\*.*?\*/", "", kt, flags=re.S)
    parts = {m.group(1): m.group(2) for m in re.finditer(r'val\s+(\w+)\s*=\s*getPart\("([^"]+)"\)', kt)}
    out: dict = {}
    for key in ("portraitScale", "profileScale"):
        m = re.search(key + r"\s*=\s*(-?[\d.]+)F?", kt)
        if m:
            out[key] = _num(m.group(1))
    for key in ("portraitTranslation", "profileTranslation"):
        m = re.search(key + r"\s*=\s*Vec3d?\(([^)]*)\)", kt)
        if m:
            out[key] = _vec(m.group(1))
    m = re.search(r'registerChildWithAllChildren\("([^"]+)"\)', kt)
    out["rootBone"] = m.group(1) if m else None
    quirks = {m.group(1): f"q.bedrock_quirk('{m.group(2)}', '{m.group(3)}')"
              for m in re.finditer(r'val\s+(\w+)\s*=\s*quirk\s*\{\s*bedrockStateful\("([^"]+)",\s*"([^"]+)"\)\s*\}', kt)}
    cries = re.findall(r'bedrockStateful\("([^"]+)",\s*"(cry)"\)', kt)
    if cries:
        out["animations"] = {"cry": f"q.bedrock_stateful('{cries[-1][0]}', 'cry')"}
    out["poses"] = {}
    for m in re.finditer(r"(\w+)\s*=\s*registerPose\(", kt):
        body = _block(kt, m.end())
        pose: dict = {}
        name = re.search(r'poseName\s*=\s*"([^"]+)"', body)
        single = re.search(r"poseType\s*=\s*PoseType\.(\w+)", body)
        many = re.search(r"poseTypes\s*=\s*([\w.\s+]+?)(?:,\n|\n)", body)
        if single:
            pose["poseTypes"] = [single.group(1)]
        elif many:
            types = []
            for token in many.group(1).split("+"):
                token = token.strip().split(".")[-1]
                types += POSE_SETS.get(token, [token])
            pose["poseTypes"] = list(dict.fromkeys(types))
        if "!it.isBattling" in body:
            pose["isBattle"] = False
        elif "it.isBattling" in body:
            pose["isBattle"] = True
        ticks = re.search(r"transformTicks\s*=\s*(\d+)", body)
        if ticks:
            pose["transformTicks"] = int(ticks.group(1))
        q = re.search(r"quirks\s*=\s*arrayOf\(([^)]*)\)", body)
        if q:
            pose["quirks"] = [quirks[n.strip()] for n in q.group(1).split(",") if n.strip() in quirks]
        hidden = re.findall(r"(\w+)\.createTransformation\(\)\.withVisibility\(visibility\s*=\s*false\)", body)
        if hidden:
            pose["transformedParts"] = [{"part": parts.get(h, h), "isVisible": False} for h in hidden]
        anims = []
        a = re.search(r"animations\s*=\s*arrayOf\(", body)
        if a:
            inner = _block(body, a.end())
            for item in re.finditer(r"(\w+)\s*(\(([^()]|\([^()]*\))*\))?", inner):
                fn, args = item.group(1), item.group(2) or "()"
                if fn == "singleBoneLook":
                    anims.append(f"q.look('{parts.get('head', 'head')}')")
                elif fn == "bedrock":
                    g, n = re.findall(r'"([^"]+)"', args)[:2]
                    anims.append(f"q.bedrock('{g}', '{n}')")
                elif fn == "BipedWalkAnimation":
                    period = re.search(r"periodMultiplier\s*=\s*([\d.]+)", args)
                    amp = re.search(r"amplitudeMultiplier\s*=\s*([\d.]+)", args)
                    anims.append(f"q.biped_walk({_num(period.group(1)) if period else 1}, {_num(amp.group(1)) if amp else 1},"
                                 f" '{parts.get('leftLeg', 'leg_left')}', '{parts.get('rightLeg', 'leg_right')}')")
                elif fn == "BimanualSwingAnimation":
                    period = re.search(r"swingPeriodMultiplier\s*=\s*([\d.]+)", args)
                    amp = re.search(r"amplitudeMultiplier\s*=\s*([\d.]+)", args)
                    anims.append(f"q.bimanual_swing({_num(period.group(1)) if period else 1}, {_num(amp.group(1)) if amp else 1},"
                                 f" '{parts.get('leftArm', 'arm_left')}', '{parts.get('rightArm', 'arm_right')}')")
                elif fn not in ("this", "F") and not re.fullmatch(r"[\d.]+F?", fn) and fn not in ("periodMultiplier", "amplitudeMultiplier", "minPitch", "maxPitch"):
                    warnings.append(f"unsupported animation {fn}{args}")
        pose["animations"] = anims
        out["poses"][name.group(1) if name else m.group(1)] = pose
    return out, warnings
