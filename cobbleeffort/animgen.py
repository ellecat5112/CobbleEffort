"""Procedural animation generator.

From a detected Rig this builds a full Cobblemon animation set:

  looping (Molang, seamless):  ground_idle, ground_walk, battle_idle, sleep,
                               air_idle, air_fly, water_idle, water_swim
  one-shot (keyframes):        blink, cry, physical, special, status, recoil, faint

Axis conventions (verified against Cobblemon's own Bedrock assets):
  * models face -Z; left side is +X
  * +X rotation tips forward-pointing parts DOWN (jaw opens, head nods down)
    and swings downward-pointing parts (legs) BACKWARD
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .rig import Limb, Rig
from .util import fmt, num

ALIASES = {
    "idle": "ground_idle", "stand": "ground_idle", "standing": "ground_idle",
    "walk": "ground_walk", "walking": "ground_walk", "run": "ground_walk", "move": "ground_walk",
    "battle": "battle_idle", "fight": "battle_idle",
    "fly": "air_fly", "flying": "air_fly", "hover": "air_idle", "air": "air_idle",
    "swim": "water_swim", "swimming": "water_swim", "float": "water_idle",
    "attack": "physical", "melee": "physical", "hurt": "recoil", "hit": "recoil", "damage": "recoil",
    "death": "faint", "die": "faint", "dead": "faint", "roar": "cry", "rest": "sleep",
}

CHANNEL_REST = {"rotation": 0.0, "position": 0.0, "scale": 1.0}


@dataclass
class Settings:
    energy: float = 1.0   # amplitude multiplier
    speed: float = 1.0    # tempo multiplier
    can_fly: bool = False
    can_swim: bool = False
    floats: bool = False  # levitating, legless "flyer" (ghosts etc.)


# ================================================================ builders


class LoopAnim:
    """A looping animation made of sine terms, emitted as Molang expressions."""

    def __init__(self, length: float):
        self.length = length
        # (bone, channel) -> per-axis [base, [terms]]
        self.tracks: dict[tuple[str, str], list[list]] = {}

    def add(self, bone: str | None, channel: str, axis: int, amp: float = 0.0, k: float = 1, phase: float = 0.0,
            base: float = 0.0, kind: str = "sin") -> None:
        if not bone:
            return
        key = (bone, channel)
        if key not in self.tracks:
            rest = CHANNEL_REST[channel]
            self.tracks[key] = [[rest, []], [rest, []], [rest, []]]
        ax = self.tracks[key][axis]
        ax[0] += base
        if abs(amp) > 1e-6:
            ax[1].append((amp, k, phase, kind))

    def rot(self, bone, axis, amp=0.0, k=1, phase=0.0, base=0.0, kind="sin"):
        self.add(bone, "rotation", axis, amp, k, phase, base, kind)

    def pos(self, bone, axis, amp=0.0, k=1, phase=0.0, base=0.0, kind="sin"):
        self.add(bone, "position", axis, amp, k, phase, base, kind)

    def _expr(self, base: float, terms: list) -> float | str:
        parts = []
        if abs(base) > 1e-6 or not terms:
            parts.append(fmt(base, 2))
        for amp, k, phase, kind in terms:
            speed = 360.0 * k / self.length
            inner = f"q.anim_time*{fmt(speed, 3)}"
            if abs(phase % 360) > 1e-6:
                inner += f"+{fmt(phase % 360, 1)}"
            wave = f"math.sin({inner})"
            if kind == "abs":
                wave = f"math.abs({wave})"
            parts.append(f"{wave}*{fmt(amp, 2)}")
        if len(parts) == 1 and not terms:
            return num(base, 2)
        return "+".join(parts).replace("+-", "-")

    def to_json(self) -> dict:
        bones: dict[str, dict] = {}
        for (bone, ch), axes in self.tracks.items():
            vals = [self._expr(b, t) for b, t in axes]
            rest = CHANNEL_REST[ch]
            if all(isinstance(v, (int, float)) and abs(v - rest) < 1e-6 for v in vals):
                continue
            bones.setdefault(bone, {})[ch] = vals
        return {"loop": True, "animation_length": num(self.length, 4), "bones": bones}


def _time_key(t: float) -> str:
    s = f"{t:.4f}".rstrip("0")
    return s + "0" if s.endswith(".") else s


class KeyAnim:
    """A one-shot animation from keyframes (catmull-rom smoothed)."""

    def __init__(self, length: float, hold: bool = False):
        self.length = length
        self.hold = hold
        self.tracks: dict[tuple[str, str], dict[float, list[float]]] = {}

    def key(self, bone: str | None, channel: str, t: float, xyz: list[float]) -> None:
        if not bone:
            return
        tr = self.tracks.setdefault((bone, channel), {})
        if t in tr:
            tr[t] = [a + b for a, b in zip(tr[t], xyz)] if channel != "scale" else [a * b for a, b in zip(tr[t], xyz)]
        else:
            tr[t] = list(xyz)

    def frames(self, bone: str | None, channel: str, frames: list[tuple[float, list[float]]]) -> None:
        for t, v in frames:
            self.key(bone, channel, t, v)

    def to_json(self) -> dict:
        bones: dict[str, dict] = {}
        for (bone, ch), tr in self.tracks.items():
            rest = [CHANNEL_REST[ch]] * 3
            tr = dict(tr)
            tr.setdefault(0.0, rest)
            if not self.hold:
                tr.setdefault(self.length, rest)
            out = {}
            for t in sorted(tr):
                v = [num(x, 2) for x in tr[t]]
                out[_time_key(t)] = {"post": v, "lerp_mode": "catmullrom"} if 0 < t < self.length else v
            bones.setdefault(bone, {})[ch] = out
        data: dict = {"animation_length": num(self.length, 4), "bones": bones}
        if self.hold:
            data["loop"] = "hold_on_last_frame"
        return data


# ================================================================ helpers


def _size_factor(rig: Rig) -> float:
    return max(0.4, min(3.0, rig.height_px / 20.0))


def _leg_phases(rig: Rig) -> dict[str, float]:
    """Phase offset (degrees) per leg root, giving a natural gait."""
    legs = rig.legs
    phases: dict[str, float] = {}
    if len(legs) == 2:
        a, b = legs
        if a.side == b.side:  # odd naming; just alternate
            phases[a.root], phases[b.root] = 0, 180
        else:
            for l in legs:
                phases[l.root] = 0 if l.side >= 0 else 180
    elif len(legs) == 4:
        # trot: front-left with back-right, front-right with back-left
        for l in legs:
            front = l.front if l.front is not None else True
            left = l.side >= 0
            phases[l.root] = 0 if (front == left) else 180
    else:
        # multiped / odd: alternating tripod by rank along the body and side
        for side in (1, -1, 0):
            same = [l for l in legs if l.side == side]
            same.sort(key=lambda l: rig.front_sign * l.pivot[2])
            for i, l in enumerate(same):
                phases[l.root] = ((i % 2) * 180 + (0 if side >= 0 else 180)) % 360
    return phases


def _arm_phase(rig: Rig, arm: Limb, leg_phases: dict[str, float]) -> float:
    same_side = [l for l in rig.legs if l.side == arm.side and arm.side != 0]
    if same_side:
        return (leg_phases[same_side[0].root] + 180) % 360
    return 0 if arm.side >= 0 else 180


def _wave_chain(anim: LoopAnim, chain: Limb, axis: int, amp: float, grow: float, k: float, lag: float,
                phase: float = 0.0, side_mult: bool = False) -> None:
    for i, bone in enumerate(chain.bones):
        a = (amp + grow * i) * (chain.side if side_mult and chain.side else 1)
        anim.rot(bone, axis, a, k, phase - lag * i)


def _head_bones(rig: Rig) -> list[str]:
    return [b for b in rig.necks + ([rig.head] if rig.head else []) if b]


def _ground_lift_for_side_fall(rig: Rig, geo_root_pivot: list[float]) -> float:
    half_w = rig.width_px / 2
    pivot_h = geo_root_pivot[1] - rig.min_y
    return max(0.0, half_w - pivot_h)


# ================================================================ animations


def ground_idle(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    a = LoopAnim(3.0 / s.speed)
    a.rot(rig.body, 0, 1.2 * E, 1, 0)
    a.pos(rig.body, 1, 0.25 * S * E, 1, 0)
    for i, b in enumerate(_head_bones(rig)):
        a.rot(b, 0, -1.0 * E, 1, 40 + 20 * i)
        if b == rig.head:
            a.rot(b, 2, 1.5 * E, 1, 90)
    for arm in rig.arms:
        a.rot(arm.root, 2, -arm.side * 2.5 * E, 1, 0)
        a.rot(arm.root, 0, 2.0 * E, 1, 30)
        for seg in arm.bones[1:]:
            a.rot(seg, 0, -3.0 * E, 1, 60)
    for t in rig.tails:
        _wave_chain(a, t, 1, 5 * E, 2.5 * E, 1, 35)
        _wave_chain(a, t, 0, 1.5 * E, 0.5 * E, 2, 35)
    for e in rig.ears:
        _wave_chain(a, e, 2, 3 * E, 1 * E, 1, 30, 90, side_mult=True)
    for w in rig.wings:
        a.rot(w.root, 2, w.side * 2.5 * E, 1, 0)
    for f in rig.fins:
        _wave_chain(a, f, 1, 6 * E, 2 * E, 2, 40, side_mult=True)
    for fl in rig.floppy:
        _wave_chain(a, fl, 0, 3 * E, 1.5 * E, 1, 45)
        _wave_chain(a, fl, 2, 2 * E, 1 * E, 1, 45, 90)
    return a.to_json()


def ground_walk(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    gait = rig.gait
    length = {"biped": 1.0, "quadruped": 0.9, "multiped": 0.8, "hop": 0.8, "slither": 1.2}[gait] / s.speed
    a = LoopAnim(length)
    phases = _leg_phases(rig)
    amp = {"biped": 28, "quadruped": 24, "multiped": 18}.get(gait, 0) * E
    for leg in rig.legs:
        p = phases.get(leg.root, 0)
        a.rot(leg.root, 0, amp, 1, p)
        segs = leg.bones[1:]
        for j, seg in enumerate(segs):
            if j == len(segs) - 1 and len(segs) >= 1:
                a.rot(seg, 0, -0.55 * amp, 1, p)            # keep the foot roughly flat
            else:
                a.rot(seg, 0, 0.35 * amp, 1, p - 70)        # knee bend lags the swing
    for arm in rig.arms:
        p = _arm_phase(rig, arm, phases)
        a.rot(arm.root, 0, 0.8 * max(amp, 20 * E), 1, p)
        for seg in arm.bones[1:]:
            a.rot(seg, 0, 0.2 * max(amp, 20 * E), 1, p - 60, base=-8)
    if gait == "hop":
        a.pos(rig.root, 1, 2.5 * S * E, 0.5, 0, kind="abs")
        a.rot(rig.body, 0, 4 * E, 1, 90)
    elif gait == "slither":
        a.rot(rig.body, 1, 6 * E, 1, 60)
    else:
        a.pos(rig.body, 1, 0.5 * S * E, 2, 90)
        a.rot(rig.body, 2, 2.0 * E, 1, 0)
        if gait == "biped":
            a.rot(rig.body, 1, 3.0 * E, 1, 0)
            a.rot(rig.body, 0, 0, base=3 * E)
    for b in _head_bones(rig):
        a.rot(b, 0, -1.5 * E, 2, 90)
        a.rot(b, 2, -1.5 * E, 1, 0)
    big = gait == "slither"
    for t in rig.tails:
        _wave_chain(a, t, 1, (14 if big else 8) * E, (6 if big else 3) * E, 1, 55 if big else 40)
        _wave_chain(a, t, 0, 2 * E, 0.5 * E, 2, 40)
    for e in rig.ears:
        _wave_chain(a, e, 0, 4 * E, 1 * E, 2, 30, 120)
    for w in rig.wings:
        a.rot(w.root, 2, w.side * 5 * E, 2, 0)
    for f in rig.fins:
        _wave_chain(a, f, 1, 8 * E, 2 * E, 2, 40, side_mult=True)
    for fl in rig.floppy:
        _wave_chain(a, fl, 0, 5 * E, 3 * E, 2, 60)
    return a.to_json()


def battle_idle(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    a = LoopAnim(1.5 / s.speed)
    a.rot(rig.body, 0, 2.0 * E, 1, 0, base=4 * E)
    a.pos(rig.body, 1, 0.35 * S * E, 1, 0)
    hb = _head_bones(rig)
    for i, b in enumerate(hb):
        a.rot(b, 0, -1.5 * E, 1, 40 + 20 * i, base=-4 * E / max(1, len(hb)))
    for arm in rig.arms:
        a.rot(arm.root, 0, 4 * E, 1, 30, base=-25 * E)
        a.rot(arm.root, 2, -arm.side * 3 * E, 1, 0, base=-arm.side * 8 * E)
        for seg in arm.bones[1:]:
            a.rot(seg, 0, -5 * E, 1, 60, base=-20 * E)
    phases = _leg_phases(rig)
    for leg in rig.legs:  # gentle weight shifting
        a.rot(leg.root, 0, 1.5 * E, 1, phases.get(leg.root, 0))
    for t in rig.tails:
        _wave_chain(a, t, 1, 9 * E, 3 * E, 1, 40)
        _wave_chain(a, t, 0, 3 * E, 1 * E, 1, 40, 90)
    for e in rig.ears:
        _wave_chain(a, e, 0, 3 * E, 1 * E, 1, 30, 0)
    for w in rig.wings:
        a.rot(w.root, 2, w.side * 6 * E, 1, 0, base=w.side * 10 * E)
    for f in rig.fins:
        _wave_chain(a, f, 1, 10 * E, 3 * E, 2, 40, side_mult=True)
    for fl in rig.floppy:
        _wave_chain(a, fl, 0, 5 * E, 2 * E, 1, 50)
    return a.to_json()


def sleep(rig: Rig, s: Settings, root_pivot: list[float]) -> dict:
    E = s.energy
    a = LoopAnim(4.0 / s.speed)
    if rig.legs:
        hip = sum(l.pivot[1] for l in rig.legs) / len(rig.legs) - rig.min_y
        a.pos(rig.root, 1, 0, base=-0.8 * hip)
        biped = rig.gait == "biped"
        for leg in rig.legs:
            front = True if biped else (leg.front if leg.front is not None else True)
            a.rot(leg.root, 0, 0, base=-75 if front else 75)
    a.rot(rig.body, 0, 1.0 * E, 1, 0)
    a.pos(rig.body, 1, 0.2 * E, 1, 0)
    for b in _head_bones(rig):
        a.rot(b, 0, 1.0 * E, 1, 60, base=12)
    for arm in rig.arms:
        a.rot(arm.root, 0, 0, base=-25)
        a.rot(arm.root, 2, 0, base=-arm.side * 5)
    for t in rig.tails:
        for i, b in enumerate(t.bones):
            a.rot(b, 1, 1.5 * E, 1, -30 * i, base=18 + 4 * i)
    for e in rig.ears:
        a.rot(e.root, 0, 0, base=20)
    for w in rig.wings:
        a.rot(w.root, 2, 0, base=-w.side * 4)
    for fl in rig.floppy:
        a.rot(fl.root, 0, 1 * E, 1, 0, base=10)
    for eye in rig.eyes:
        a.add(eye, "scale", 1, 0, base=-0.9)  # 1 - 0.9 = 0.1 -> closed
    return a.to_json()


def air_idle(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    if not rig.wings:  # levitating
        a = LoopAnim(2.5 / s.speed)
        a.pos(rig.root, 1, 1.2 * S * E, 1, 0)
        a.rot(rig.body, 0, 2 * E, 1, 60)
        for arm in rig.arms:
            a.rot(arm.root, 2, -arm.side * 5 * E, 1, 30, base=-arm.side * 10)
        for leg in rig.legs:
            a.rot(leg.root, 0, 3 * E, 1, 90, base=10)
        for t in rig.tails:
            _wave_chain(a, t, 0, 6 * E, 3 * E, 1, 45)
        for fl in rig.floppy:
            _wave_chain(a, fl, 0, 6 * E, 3 * E, 1, 50)
        for b in _head_bones(rig):
            a.rot(b, 0, -1.5 * E, 1, 90)
        return a.to_json()
    a = LoopAnim(1.0 / s.speed)
    for w in rig.wings:
        for i, b in enumerate(w.bones):
            a.rot(b, 2, w.side * (30 if i == 0 else 15) * E, 1, -40 * i)
    a.pos(rig.root, 1, 1.0 * S * E, 1, 270)
    a.rot(rig.body, 0, 2 * E, 1, 270)
    for leg in rig.legs:
        a.rot(leg.root, 0, 3 * E, 1, 0, base=15)
    for t in rig.tails:
        _wave_chain(a, t, 0, 4 * E, 2 * E, 1, 40)
    for b in _head_bones(rig):
        a.rot(b, 0, -2 * E, 1, 300)
    for fl in rig.floppy:
        _wave_chain(a, fl, 0, 5 * E, 2 * E, 1, 50, 180)
    return a.to_json()


def air_fly(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    if not rig.wings:
        a = LoopAnim(1.5 / s.speed)
        a.pos(rig.root, 1, 1.0 * S * E, 1, 0)
        a.rot(rig.body, 0, 2 * E, 1, 0, base=12)
        for arm in rig.arms:
            a.rot(arm.root, 0, 3 * E, 1, 90, base=30)
        for leg in rig.legs:
            a.rot(leg.root, 0, 3 * E, 1, 90, base=35)
        for t in rig.tails:
            _wave_chain(a, t, 1, 10 * E, 4 * E, 1, 50)
        for fl in rig.floppy:
            _wave_chain(a, fl, 0, 8 * E, 3 * E, 1, 60, 0)
        for b in _head_bones(rig):
            a.rot(b, 0, 0, base=-8)
        return a.to_json()
    a = LoopAnim(0.6 / s.speed)
    for w in rig.wings:
        for i, b in enumerate(w.bones):
            a.rot(b, 2, w.side * (45 if i == 0 else 20) * E, 1, -50 * i)
    a.pos(rig.root, 1, 1.5 * S * E, 1, 270)
    for leg in rig.legs:
        a.rot(leg.root, 0, 0, base=45)
    for arm in rig.arms:
        a.rot(arm.root, 0, 0, base=30)
    for t in rig.tails:
        _wave_chain(a, t, 0, 5 * E, 2 * E, 1, 40)
    for b in _head_bones(rig):
        a.rot(b, 0, -1.5 * E, 1, 300, base=-5)
    for fl in rig.floppy:
        _wave_chain(a, fl, 0, 8 * E, 3 * E, 1, 60, 180)
    return a.to_json()


def water_idle(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    a = LoopAnim(2.0 / s.speed)
    a.pos(rig.body, 1, 0.6 * S * E, 1, 0)
    a.rot(rig.body, 2, 3 * E, 1, 90)
    for f in rig.fins:
        _wave_chain(a, f, 2, 12 * E, 4 * E, 2, 40, side_mult=True)
    for t in rig.tails:
        _wave_chain(a, t, 1, 8 * E, 4 * E, 1, 50)
    phases = _leg_phases(rig)
    for leg in rig.legs:
        a.rot(leg.root, 0, 20 * E, 1, phases.get(leg.root, 0))
    for arm in rig.arms:
        a.rot(arm.root, 0, 20 * E, 1, _arm_phase(rig, arm, phases))
    for w in rig.wings:
        a.rot(w.root, 2, w.side * 8 * E, 1, 0)
    for fl in rig.floppy:
        _wave_chain(a, fl, 0, 6 * E, 3 * E, 1, 50)
    return a.to_json()


def water_swim(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    a = LoopAnim(1.0 / s.speed)
    a.rot(rig.body, 1, 6 * E, 1, 90)
    a.pos(rig.body, 1, 0.4 * S * E, 2, 0)
    for t in rig.tails:
        _wave_chain(a, t, 1, 15 * E, 6 * E, 1, 60)
    for f in rig.fins:
        _wave_chain(a, f, 2, 25 * E, 6 * E, 1, 50, side_mult=True)
    phases = _leg_phases(rig)
    for leg in rig.legs:
        a.rot(leg.root, 0, 35 * E, 1, phases.get(leg.root, 0))
    for arm in rig.arms:
        a.rot(arm.root, 0, 40 * E, 1, _arm_phase(rig, arm, phases))
    for w in rig.wings:
        a.rot(w.root, 2, w.side * 20 * E, 1, 0)
    for fl in rig.floppy:
        _wave_chain(a, fl, 0, 8 * E, 4 * E, 1, 60)
    return a.to_json()


# ------------------------------------------------------------- one-shots


def blink(rig: Rig, s: Settings) -> dict:
    a = KeyAnim(0.1667)
    for eye in rig.eyes:
        a.frames(eye, "scale", [(0.0, [1, 1, 1]), (0.0833, [1, 0.1, 1]), (0.1667, [1, 1, 1])])
    return a.to_json()


def cry(rig: Rig, s: Settings) -> dict:
    E = s.energy
    a = KeyAnim(1.25 / s.speed)
    T = lambda t: t / s.speed  # noqa: E731
    up = [(T(0.25), [-16 * E, 0, 0]), (T(0.8), [-16 * E, 0, 0])]
    for b in _head_bones(rig):
        a.frames(b, "rotation", up)
    a.frames(rig.jaw, "rotation", [(T(0.25), [25 * E, 0, 0]), (T(0.8), [25 * E, 0, 0]), (T(1.0), [0, 0, 0])])
    a.frames(rig.body, "rotation", [(T(0.25), [-6 * E, 0, 0]), (T(0.8), [-6 * E, 0, 0])])
    for arm in rig.arms:
        a.frames(arm.root, "rotation", [(T(0.25), [-40 * E, 0, -arm.side * 15 * E]), (T(0.8), [-40 * E, 0, -arm.side * 15 * E])])
    for w in rig.wings:
        a.frames(w.root, "rotation", [(T(0.25), [0, 0, w.side * 30 * E]), (T(0.8), [0, 0, w.side * 30 * E])])
    for t in rig.tails:
        for i, b in enumerate(t.bones):
            amp = (12 + 4 * i) * E
            a.frames(b, "rotation", [(T(0.25), [0, amp, 0]), (T(0.5), [0, -amp, 0]), (T(0.75), [0, amp, 0])])
    for e in rig.ears:
        a.frames(e.root, "rotation", [(T(0.25), [-15 * E, 0, 0]), (T(0.8), [-15 * E, 0, 0])])
    return a.to_json()


def physical(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    a = KeyAnim(0.8 / s.speed)
    T = lambda t: t / s.speed  # noqa: E731
    d = 2.0 * S * E * rig.front_sign
    a.frames(rig.root, "position", [(T(0.2), [0, 0, -0.5 * d]), (T(0.4), [0, 0, 1.5 * d])])
    a.frames(rig.body, "rotation", [(T(0.2), [-8 * E, 0, 0]), (T(0.4), [15 * E, 0, 0])])
    for b in _head_bones(rig):
        a.frames(b, "rotation", [(T(0.2), [-5 * E, 0, 0]), (T(0.4), [8 * E, 0, 0])])
    a.frames(rig.jaw, "rotation", [(T(0.3), [25 * E, 0, 0]), (T(0.45), [0, 0, 0])])
    for arm in rig.arms:
        a.frames(arm.root, "rotation", [(T(0.2), [40 * E, 0, 0]), (T(0.4), [-70 * E, 0, 0])])
    for leg in rig.legs:
        if leg.front:
            a.frames(leg.root, "rotation", [(T(0.2), [10 * E, 0, 0]), (T(0.4), [-25 * E, 0, 0])])
    for w in rig.wings:
        a.frames(w.root, "rotation", [(T(0.2), [0, 0, w.side * 40 * E]), (T(0.4), [0, 0, -w.side * 20 * E])])
    for t in rig.tails:
        a.frames(t.root, "rotation", [(T(0.2), [0, -15 * E, 0]), (T(0.4), [0, 20 * E, 0])])
    return a.to_json()


def special(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    a = KeyAnim(1.0 / s.speed)
    T = lambda t: t / s.speed  # noqa: E731
    hold = lambda v: [(T(0.3), v), (T(0.65), v)]  # noqa: E731
    a.frames(rig.body, "rotation", hold([-10 * E, 0, 0]))
    a.frames(rig.root, "position", hold([0, 1.0 * S * E, 0]))
    for b in _head_bones(rig):
        a.frames(b, "rotation", hold([-12 * E, 0, 0]))
    a.frames(rig.jaw, "rotation", hold([30 * E, 0, 0]))
    for arm in rig.arms:
        a.frames(arm.root, "rotation", hold([-80 * E, 0, -arm.side * 10 * E]))
    for w in rig.wings:
        a.frames(w.root, "rotation", hold([0, 0, w.side * 45 * E]))
    for t in rig.tails:
        a.frames(t.root, "rotation", hold([-15 * E, 0, 0]))
    for e in rig.ears:
        a.frames(e.root, "rotation", hold([-10 * E, 0, 0]))
    for fl in rig.floppy:
        a.frames(fl.root, "rotation", hold([-12 * E, 0, 0]))
    return a.to_json()


def status(rig: Rig, s: Settings) -> dict:
    E = s.energy
    a = KeyAnim(1.0 / s.speed)
    T = lambda t: t / s.speed  # noqa: E731
    wig = [(T(0.2), 1), (T(0.4), -1), (T(0.6), 1), (T(0.8), -1)]
    a.frames(rig.body, "rotation", [(t, [0, 10 * E * v, 4 * E * v]) for t, v in wig])
    if rig.head:
        a.frames(rig.head, "rotation", [(t, [0, 0, -8 * E * v]) for t, v in wig])
    for t_ in rig.tails:
        a.frames(t_.root, "rotation", [(t, [0, 18 * E * v, 0]) for t, v in wig])
    for arm in rig.arms:
        a.frames(arm.root, "rotation", [(T(0.3), [-20 * E, 0, -arm.side * 25 * E]), (T(0.7), [-20 * E, 0, -arm.side * 25 * E])])
    for w in rig.wings:
        a.frames(w.root, "rotation", [(T(0.3), [0, 0, w.side * 25 * E]), (T(0.7), [0, 0, w.side * 25 * E])])
    return a.to_json()


def recoil(rig: Rig, s: Settings) -> dict:
    E, S = s.energy, _size_factor(rig)
    a = KeyAnim(0.5)
    a.frames(rig.root, "position", [(0.1, [0, 0, -2.0 * S * E * rig.front_sign])])
    a.frames(rig.body, "rotation", [(0.1, [-12 * E, 0, 0])])
    for b in _head_bones(rig):
        a.frames(b, "rotation", [(0.1, [-8 * E, 0, 0])])
    for eye in rig.eyes:
        a.frames(eye, "scale", [(0.05, [1, 0.1, 1]), (0.3, [1, 0.1, 1])])
    for t in rig.tails:
        a.frames(t.root, "rotation", [(0.1, [-15 * E, 0, 0])])
    return a.to_json()


def faint(rig: Rig, s: Settings, root_pivot: list[float]) -> dict:
    a = KeyAnim(1.0, hold=True)
    lift = _ground_lift_for_side_fall(rig, root_pivot)
    a.frames(rig.root, "rotation", [(0.15, [0, 0, -5]), (0.6, [0, 0, 90]), (1.0, [0, 0, 90])])
    a.frames(rig.root, "position", [(0.6, [0, lift, 0]), (1.0, [0, lift, 0])])
    for b in _head_bones(rig):
        a.frames(b, "rotation", [(0.6, [15, 0, 0]), (1.0, [15, 0, 0])])
    for eye in rig.eyes:
        a.frames(eye, "scale", [(0.5, [1, 0.1, 1]), (1.0, [1, 0.1, 1])])
    for t in rig.tails:
        a.frames(t.root, "rotation", [(0.6, [10, 0, 0]), (1.0, [10, 0, 0])])
    return a.to_json()


# ================================================================ entry


@dataclass
class AnimationSet:
    group: str
    animations: dict[str, dict] = field(default_factory=dict)  # short name -> json
    generated: list[str] = field(default_factory=list)
    supplied: list[str] = field(default_factory=list)

    def has(self, short: str) -> bool:
        return short in self.animations

    def to_file(self) -> dict:
        return {
            "format_version": "1.8.0",
            "animations": {f"animation.{self.group}.{k}": v for k, v in self.animations.items()},
        }


def short_name(full: str) -> str:
    name = full.split(".")[-1] if full.startswith("animation.") else full
    name = name.strip().lower().replace(" ", "_").replace("-", "_")
    return ALIASES.get(name, name)


def generate(rig: Rig, group: str, settings: Settings, root_pivot: list[float],
             supplied: dict[str, dict] | None = None, skip: list[str] | None = None) -> AnimationSet:
    out = AnimationSet(group=group)
    for full, data in (supplied or {}).items():
        sn = short_name(full)
        out.animations[sn] = data
        out.supplied.append(sn)

    wanted: dict[str, callable] = {
        "ground_idle": lambda: ground_idle(rig, settings),
        "ground_walk": lambda: ground_walk(rig, settings),
        "battle_idle": lambda: battle_idle(rig, settings),
        "sleep": lambda: sleep(rig, settings, root_pivot),
        "cry": lambda: cry(rig, settings),
        "physical": lambda: physical(rig, settings),
        "special": lambda: special(rig, settings),
        "status": lambda: status(rig, settings),
        "recoil": lambda: recoil(rig, settings),
        "faint": lambda: faint(rig, settings, root_pivot),
    }
    if rig.eyes:
        wanted["blink"] = lambda: blink(rig, settings)
    if settings.can_fly or settings.floats:
        wanted["air_idle"] = lambda: air_idle(rig, settings)
        wanted["air_fly"] = lambda: air_fly(rig, settings)
    if settings.can_swim:
        wanted["water_idle"] = lambda: water_idle(rig, settings)
        wanted["water_swim"] = lambda: water_swim(rig, settings)
    for name, fn in wanted.items():
        if name in out.animations or name in (skip or []):
            continue
        out.animations[name] = fn()
        out.generated.append(name)
    return out
