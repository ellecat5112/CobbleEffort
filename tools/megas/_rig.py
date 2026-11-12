"""Shared rig for hand-built box models (megas, new Pokémon): Bedrock animations and the Cobblemon poser."""
from __future__ import annotations

import math

from _anim import keys, sin, track


def animations(group, kind, opt, names, legs, piv):
    """The animation group (idle, walk, battle, sleep, cry, moves, faint) from the model's bone names: body, head,
    jaw, tail, cap, mane, skirt, wings, arms, legs (leg*); other bones sway. kind: quadruped, biped or floater."""
    has = set(names)
    A = {}
    bob = 1.0 if kind == "floater" else 0.3

    def legs_walk(period, amp):
        out = {}
        for n, leg in enumerate(sorted(legs)):
            phase = 0.5 * ((n % 2) ^ (("back" in leg) and kind == "quadruped"))
            out[leg] = {"rotation": track(period, lambda t, ph=phase: [amp * sin(t, 1, ph), 0, 0])}
        return out

    known = {"body", "head", "tail", "cap", "mane", "skirt", "wing_left", "wing_right", "arm_left", "arm_right", "jaw"}
    extras = [n for n in names if n not in known and not n.startswith(("leg", "spin", "ring"))]
    spins = [n for n in names if n.startswith("spin")]       # gun drums and the like: turn round z
    rings = [n for n in names if n.startswith("ring")]       # hypnotic rings (a tail curled round it): always turning

    idle = {"body": {"position": track(3, lambda t: [0, -bob * (1 - math.cos(2 * math.pi * t)) / 2 if kind != "floater" else bob * sin(t), 0])}}
    if "head" in has:
        idle["head"] = {"rotation": track(3, lambda t: [2 * sin(t, 1, 0.2), 4 * sin(t, 0.5), 0])}
    if "jaw" in has:
        idle["jaw"] = {"rotation": track(3, lambda t: [3 + 3 * sin(t, 1, 0.1), 0, 0])}
    if "tail" in has:
        idle["tail"] = {"rotation": track(3, lambda t: [0, 8 * sin(t), 0])}
    if "cap" in has:
        idle["cap"] = {"rotation": track(3, lambda t: [1.5 * sin(t, 1, 0.3), 0, 2 * sin(t)])}
    if "mane" in has:
        idle["mane"] = {"rotation": track(3, lambda t: [3 * sin(t, 1, 0.25), 6 * sin(t), 0])}
    if "skirt" in has:
        idle["skirt"] = {"rotation": track(3, lambda t: [4 * sin(t, 1, 0.4), 0, 3 * sin(t)])}
    if "wing_left" in has:
        flap = opt.get("wing_flap", 6)
        idle["wing_left"] = {"rotation": track(3, lambda t: [0, flap * sin(t), 4 * sin(t)])}
        idle["wing_right"] = {"rotation": track(3, lambda t: [0, -flap * sin(t), -4 * sin(t)])}
    for arm, sg in (("arm_left", 1), ("arm_right", -1)):
        if arm in has:
            idle[arm] = {"rotation": track(3, lambda t, s=sg: [4 * sin(t, 1, 0.25), 0, s * 3 * sin(t)])}
    for n, nm in enumerate(extras):
        sgn = 1 if nm.endswith("left") else -1
        idle[nm] = {"rotation": track(3, lambda t, sg=sgn, ph=n * 0.2: [2 * sin(t, 1, ph), 0, 3 * sg * sin(t, 1, ph)])}
    for n in rings:
        idle[n] = {"rotation": track(3, lambda t: [0, 0, -180 * t], steps=24)}
    A["ground_idle"] = {"loop": True, "animation_length": 3.0, "bones": idle}

    walk = {"body": {"position": track(1, lambda t: [0, -0.4 * abs(sin(t)), 0]), "rotation": track(1, lambda t: [0, 0, 1.5 * sin(t)])}}
    if kind == "floater":
        walk = {"body": {"rotation": track(1.5, lambda t: [12, 0, 2 * sin(t)]), "position": track(1.5, lambda t: [0, 0.8 * sin(t, 2), 0])}}
    if "head" in has:
        walk["head"] = {"rotation": track(1, lambda t: [3 * sin(t, 2, 0.25), 0, 0])}
    if "tail" in has:
        walk["tail"] = {"rotation": track(1, lambda t: [0, 12 * sin(t), 0])}
    if "mane" in has:
        walk["mane"] = {"rotation": track(1.5, lambda t: [-10 + 3 * sin(t, 2), 8 * sin(t), 0])}
    if "skirt" in has:
        walk["skirt"] = {"rotation": track(1.5, lambda t: [-12 + 4 * sin(t, 2), 0, 0])}
    if "cap" in has:
        walk["cap"] = {"rotation": track(1, lambda t: [2 * sin(t, 2), 0, 3 * sin(t)])}
    if "wing_left" in has:
        walk["wing_left"] = {"rotation": track(1, lambda t: [0, 10 * sin(t, 2), 14 * sin(t, 2)])}
        walk["wing_right"] = {"rotation": track(1, lambda t: [0, -10 * sin(t, 2), -14 * sin(t, 2)])}
    for arm, ph in (("arm_left", 0.5), ("arm_right", 0.0)):
        if arm in has:
            walk[arm] = {"rotation": track(1, lambda t, p=ph: [18 * sin(t, 1, p), 0, 0])}
    for n, nm in enumerate(extras):
        walk[nm] = {"rotation": track(1, lambda t, ph=n * 0.5: [6 * sin(t, 1, ph), 0, 0])}
    walk.update(legs_walk(1, opt.get("leg_amp", 22)))
    for n in rings:
        walk[n] = {"rotation": track(1.5 if kind == "floater" else 1.0, lambda t: [0, 0, -360 * t], steps=24)}
    A["ground_walk"] = {"loop": True, "animation_length": 1.5 if kind == "floater" else 1.0, "bones": walk}

    battle = {"body": {"position": track(2, lambda t: [0, -0.5 - 0.3 * sin(t) if kind != "floater" else 0.8 * sin(t), 0])}}
    if "head" in has:
        battle["head"] = {"rotation": track(2, lambda t: [8 + 2 * sin(t), 3 * sin(t, 0.5), 0])}
    if "jaw" in has:
        battle["jaw"] = {"rotation": track(2, lambda t: [8 + 4 * sin(t), 0, 0])}
    if "tail" in has:
        battle["tail"] = {"rotation": track(2, lambda t: [-10, 14 * sin(t), 0])}
    if "mane" in has:
        battle["mane"] = {"rotation": track(2, lambda t: [6 * sin(t), 10 * sin(t, 1, 0.3), 0])}
    if "skirt" in has:
        battle["skirt"] = {"rotation": track(2, lambda t: [6 * sin(t, 1, 0.4), 0, 0])}
    if "cap" in has:
        battle["cap"] = {"rotation": track(2, lambda t: [4, 0, 3 * sin(t)])}
    if "wing_left" in has:
        battle["wing_left"] = {"rotation": track(2, lambda t: [0, 18 + 8 * sin(t, 2), 10])}
        battle["wing_right"] = {"rotation": track(2, lambda t: [0, -18 - 8 * sin(t, 2), -10])}
    for arm, sg in (("arm_left", 1), ("arm_right", -1)):
        if arm in has:
            battle[arm] = {"rotation": track(2, lambda t, s=sg: [-25 + 5 * sin(t), 0, s * (8 + 3 * sin(t, 1, 0.3))])}
    for n, nm in enumerate(extras):
        sgn = 1 if nm.endswith("left") else -1
        battle[nm] = {"rotation": track(2, lambda t, sg=sgn: [-6 + 3 * sin(t), 0, sg * (4 + 3 * sin(t, 1, 0.3))])}
    for n in spins:
        battle[n] = {"rotation": track(2, lambda t: [0, 0, 360 * t], steps=24)}
    for n in rings:
        battle[n] = {"rotation": track(2, lambda t: [0, 0, -360 * t], steps=24)}
    A["battle_idle"] = {"loop": True, "animation_length": 2.0, "bones": battle}

    leg_top = max((piv[l][1] for l in legs), default=0)
    rigid = opt.get("rigid_legs", False)
    drop = -1.5 if rigid else -(leg_top - 1) if legs else (-4 if kind == "floater" else -2)
    sleep = {"body": {"position": track(4, lambda t: [0, drop - 0.3 * (1 - math.cos(2 * math.pi * t)) / 2, 0])}}
    for leg in ([] if rigid else legs):
        sleep[leg] = {"position": track(4, lambda t: [0, drop, 0]), "rotation": track(4, lambda t, l=leg: [-75 if "front" in l else 60, 0, 0])}
    if "head" in has:
        sleep["head"] = {"rotation": track(4, lambda t: [16 + 1.5 * sin(t), 0, 0])}
    if "tail" in has:
        sleep["tail"] = {"rotation": track(4, lambda t: [0, 35, 0])}
    if "wing_left" in has:
        sleep["wing_left"] = {"rotation": track(4, lambda t: [0, -30, -8])}
        sleep["wing_right"] = {"rotation": track(4, lambda t: [0, 30, 8])}
    for arm, sg in (("arm_left", 1), ("arm_right", -1)):
        if arm in has:
            sleep[arm] = {"rotation": track(4, lambda t, s=sg: [10, 0, -s * 6])}
    if "mane" in has:
        sleep["mane"] = {"rotation": track(4, lambda t: [10, 0, 0])}
    A["sleep"] = {"loop": True, "animation_length": 4.0, "bones": sleep}

    cry = {"body": {"position": keys([(0, [0, 0, 0]), (0.35, [0, 1, 0]), (1.1, [0, 0.8, 0]), (1.5, [0, 0, 0])])}}
    if "head" in has:
        cry["head"] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [-25, 0, 0]), (0.55, [-22, -8, 0]), (0.75, [-22, 8, 0]), (1.1, [-15, 0, 0]), (1.5, [0, 0, 0])])}
    if "jaw" in has:
        cry["jaw"] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [28, 0, 0]), (1.1, [24, 0, 0]), (1.5, [0, 0, 0])])}
    if "wing_left" in has:
        cry["wing_left"] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [0, 25, 15]), (1.1, [0, 20, 12]), (1.5, [0, 0, 0])])}
        cry["wing_right"] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [0, -25, -15]), (1.1, [0, -20, -12]), (1.5, [0, 0, 0])])}
    for arm, sg in (("arm_left", 1), ("arm_right", -1)):
        if arm in has:
            cry[arm] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [-40, 0, sg * 20]), (1.1, [-35, 0, sg * 18]), (1.5, [0, 0, 0])])}
    if "mane" in has:
        cry["mane"] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [-15, 10, 0]), (1.1, [-10, -10, 0]), (1.5, [0, 0, 0])])}
    A["cry"] = {"animation_length": 1.5, "bones": cry}

    phys = {"body": {"position": keys([(0, [0, 0, 0]), (0.25, [0, 0.4, 2]), (0.45, [0, -0.6, -5]), (0.8, [0, 0, 0])]),
                     "rotation": keys([(0, [0, 0, 0]), (0.25, [-6, 0, 0]), (0.45, [10, 0, 0]), (0.8, [0, 0, 0])])}}
    if "head" in has:
        phys["head"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [-20, 0, 0]), (0.45, [30, 0, 0]), (0.8, [0, 0, 0])])}
    if "jaw" in has:
        phys["jaw"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [30, 0, 0]), (0.45, [0, 0, 0]), (0.8, [0, 0, 0])])}
    if "tail" in has:
        phys["tail"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [0, -30, 0]), (0.45, [0, 40, 0]), (0.8, [0, 0, 0])])}
    if "wing_left" in has:
        phys["wing_left"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [0, 30, 20]), (0.45, [0, -10, -10]), (0.8, [0, 0, 0])])}
        phys["wing_right"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [0, -30, -20]), (0.45, [0, 10, 10]), (0.8, [0, 0, 0])])}
    for arm in ("arm_left", "arm_right"):
        if arm in has:
            phys[arm] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [-70, 0, 0]), (0.45, [30, 0, 0]), (0.8, [0, 0, 0])])}
    for nm in extras:
        phys[nm] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [-20, 0, 0]), (0.45, [15, 0, 0]), (0.8, [0, 0, 0])])}
    for n in spins:
        phys[n] = {"rotation": track(0.8, lambda t: [0, 0, 1440 * t], steps=48)}
    A["physical"] = {"animation_length": 0.8, "bones": phys}

    spec = {"body": {"position": keys([(0, [0, 0, 0]), (0.3, [0, 0.8, 0]), (0.6, [0, 0.8, 0]), (1.0, [0, 0, 0])])}}
    if "head" in has:
        spec["head"] = {"rotation": keys([(0, [0, 0, 0]), (0.3, [-18, 0, 0]), (0.6, [-18, 0, 0]), (1.0, [0, 0, 0])])}
    if "jaw" in has:
        spec["jaw"] = {"rotation": keys([(0, [0, 0, 0]), (0.3, [25, 0, 0]), (0.6, [25, 0, 0]), (1.0, [0, 0, 0])])}
    for w, sgn in (("wing_left", 1), ("wing_right", -1)):
        if w in has:
            spec[w] = {"rotation": keys([(0, [0, 0, 0]), (0.3, [0, 20 * sgn, 20 * sgn]), (0.6, [0, 20 * sgn, 20 * sgn]), (1.0, [0, 0, 0])])}
    for arm, sgn in (("arm_left", 1), ("arm_right", -1)):
        if arm in has:
            spec[arm] = {"rotation": keys([(0, [0, 0, 0]), (0.3, [-60, 0, sgn * 25]), (0.6, [-60, 0, sgn * 25]), (1.0, [0, 0, 0])])}
    if "cap" in has:
        spec["cap"] = {"rotation": keys([(0, [0, 0, 0]), (0.3, [0, 0, 6]), (0.45, [0, 0, -6]), (0.6, [0, 0, 4]), (1.0, [0, 0, 0])])}
    A["special"] = {"animation_length": 1.0, "bones": spec}

    status = {"body": {"position": keys([(0, [0, 0, 0]), (0.5, [0, 0.6, 0]), (1.0, [0, 0, 0])])}}
    if "head" in has:
        status["head"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [0, -14, 0]), (0.5, [0, 14, 0]), (0.75, [0, -6, 0]), (1.0, [0, 0, 0])])}
    A["status"] = {"animation_length": 1.0, "bones": status}

    faint = {"body": {"position": keys([(0, [0, 0, 0]), (2.0, [0, drop, 0])]), "rotation": keys([(0, [0, 0, 0]), (2.0, [8, 0, 10])])}}
    for leg in ([] if rigid else legs):
        faint[leg] = {"position": keys([(0, [0, 0, 0]), (2.0, [0, drop, 0])]),
                      "rotation": keys([(0, [0, 0, 0]), (2.0, [-75 if "front" in leg else 60, 0, 0])])}
    if "head" in has:
        faint["head"] = {"rotation": keys([(0, [0, 0, 0]), (2.0, [28, 0, 0])])}
    A["faint"] = {"loop": "hold_on_last_frame", "animation_length": 2.0, "bones": faint}
    return {"format_version": "1.8.0", "animations": {f"animation.{group}.{k}": v for k, v in A.items()}}


def poser(group, root, height, scale, names):
    """A poser for the group: standing/battle/walking/sleeping poses and the move animations."""
    g = group
    b = lambda a: f"q.bedrock('{g}', '{a}')"
    look = ["q.look('head')"] if "head" in names else []
    stand_types = ["STAND", "NONE", "FLOAT", "HOVER", "PORTRAIT", "PROFILE"]
    h = height * scale / 16
    return {
        "portraitScale": round(1.6 / max(1.0, h), 2), "portraitTranslation": [0, round(h * 0.55, 2), 0],
        "profileScale": round(0.95 / max(1.0, h), 2), "profileTranslation": [0, round(h * 0.25, 2), 0],
        "rootBone": root,
        "animations": {
            "cry": f"q.bedrock_stateful('{g}', 'cry')",
            "physical": f"q.bedrock_primary('{g}', 'physical', q.curve('symmetrical_wide'))",
            "special": f"q.bedrock_primary('{g}', 'special', q.curve('symmetrical_wide'))",
            "status": f"q.bedrock_primary('{g}', 'status', q.curve('symmetrical_wide'))",
            "faint": f"q.bedrock_primary('{g}', 'faint', q.curve('one'))",
        },
        "poses": {
            "battle_standing": {"poseTypes": ["STAND", "FLOAT", "HOVER"], "isBattle": True, "transformTicks": 10,
                                "animations": look + [b("battle_idle")]},
            "standing": {"poseTypes": stand_types, "isBattle": False, "transformTicks": 10, "animations": look + [b("ground_idle")]},
            "walking": {"poseTypes": ["WALK", "SWIM", "FLY"], "transformTicks": 10, "animations": look + [b("ground_walk")]},
            "sleeping": {"poseTypes": ["SLEEP"], "transformTicks": 20, "animations": [b("sleep")]},
        },
    }
