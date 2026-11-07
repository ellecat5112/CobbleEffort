"""Automatic rig detection.

Looks at bone names (and positions as a fallback) to work out which bones are
the head, neck, jaw, eyes, legs, arms, wings, tail chains, fins, ears and
"floppy bits" (antennae, leaves, hair...). The result drives the procedural
animation generator and the poser.

Anything detected wrongly can be corrected in pokemon.json under "rig".
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import Geometry
from .util import tokens

# name token -> role. Order matters inside ROLE_TOKENS (first match wins per bone).
ROLE_TOKENS: list[tuple[str, set[str]]] = [
    ("ignore", {"locator", "hitbox", "seat", "ride", "rider", "shadow", "item", "hat", "face"}),
    ("eyelid", {"eyelid", "eyelids", "lid", "lids", "blink"}),
    ("eye", {"eye", "eyes", "pupil", "pupils", "iris"}),
    ("jaw", {"jaw", "mouth", "mandible", "chin", "lowerjaw", "jawlower"}),
    ("ear", {"ear", "ears"}),
    ("head", {"head", "skull", "face"}),
    ("neck", {"neck"}),
    ("wing", {"wing", "wings"}),
    ("fin", {"fin", "fins", "flipper", "flippers"}),
    ("tail", {"tail", "tails"}),
    ("arm", {"arm", "arms", "forearm", "elbow", "hand", "hands", "shoulder", "wrist", "finger", "fingers", "claw"}),
    ("leg", {"leg", "legs", "thigh", "knee", "shin", "calf", "foot", "feet", "paw", "paws", "toe", "toes",
             "hindleg", "foreleg", "hoof", "hooves", "ankle", "heel"}),
    ("floppy", {"antenna", "antennae", "tentacle", "tentacles", "hair", "whisker", "whiskers", "leaf", "leaves",
                "vine", "vines", "ribbon", "ribbons", "tuft", "mane", "feather", "feathers", "petal", "petals",
                "flame", "fire", "frill", "crest", "scarf", "cape", "plume", "stem", "sprout", "bulb", "spike"}),
    ("body", {"body", "torso", "chest", "hip", "hips", "pelvis", "belly", "waist", "spine", "abdomen", "core",
              "trunk", "shell", "main"}),
]

LEFT = {"left", "l", "lft"}
RIGHT = {"right", "r", "rgt", "rt"}
FRONT = {"front", "fore", "f", "fl", "fr", "foreleg", "frontleg", "anterior"}
BACK = {"back", "hind", "rear", "b", "h", "bl", "br", "hl", "hr", "hindleg", "backleg", "posterior"}
LIMB_ROLES = ("leg", "arm", "wing", "fin", "tail", "floppy", "ear", "neck")
ROLE_ALIASES = {"legs": "leg", "arms": "arm", "wings": "wing", "fins": "fin", "tails": "tail", "eyes": "eye",
                "ears": "ear", "eyelids": "eyelid", "necks": "neck", "heads": "head"}


@dataclass
class Limb:
    bones: list[str]           # chain from the attached end outwards
    side: int = 0              # +1 left (+X), -1 right (-X), 0 centre
    front: bool | None = None  # True front, False back, None unknown/centre
    pivot: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

    @property
    def root(self) -> str:
        return self.bones[0]


@dataclass
class Rig:
    root: str
    body: str
    head: str | None = None
    necks: list[str] = field(default_factory=list)
    jaw: str | None = None
    eyes: list[str] = field(default_factory=list)
    eyelids: list[str] = field(default_factory=list)
    ears: list[Limb] = field(default_factory=list)
    legs: list[Limb] = field(default_factory=list)
    arms: list[Limb] = field(default_factory=list)
    wings: list[Limb] = field(default_factory=list)
    fins: list[Limb] = field(default_factory=list)
    tails: list[Limb] = field(default_factory=list)
    floppy: list[Limb] = field(default_factory=list)
    roles: dict[str, str] = field(default_factory=dict)
    height_px: float = 16.0
    width_px: float = 16.0
    length_px: float = 16.0
    min_y: float = 0.0
    centre: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    front_sign: int = -1  # -1: the model faces -Z (Blockbench/Cobblemon default)
    notes: list[str] = field(default_factory=list)

    @property
    def gait(self) -> str:
        n = len(self.legs)
        if n == 0:
            return "slither" if any(len(t.bones) >= 2 for t in self.tails) else "hop"
        if n == 2:
            return "biped"
        if n == 4:
            return "quadruped"
        return "multiped"

    def summary(self) -> list[str]:
        def limbs(ls: list[Limb]) -> str:
            if not ls:
                return "-"
            parts = []
            for l in ls:
                tag = {1: "L", -1: "R", 0: "C"}[l.side]
                if l.front is not None:
                    tag = ("F" if l.front else "B") + tag
                parts.append(f"{'>'.join(l.bones)} [{tag}]")
            return ", ".join(parts)

        return [
            f"root bone     : {self.root}",
            f"body bone     : {self.body}",
            f"head / neck   : {self.head or '-'} / {', '.join(self.necks) or '-'}",
            f"jaw           : {self.jaw or '-'}",
            f"eyes (blink)  : {', '.join(self.eyes) or '-'}",
            f"legs ({self.gait:9}): {limbs(self.legs)}",
            f"arms          : {limbs(self.arms)}",
            f"wings         : {limbs(self.wings)}",
            f"fins          : {limbs(self.fins)}",
            f"tails         : {limbs(self.tails)}",
            f"ears          : {limbs(self.ears)}",
            f"floppy bits   : {limbs(self.floppy)}",
            f"size (px)     : {self.width_px:.1f} wide x {self.height_px:.1f} tall x {self.length_px:.1f} long",
        ]


def classify(name: str) -> str | None:
    toks = tokens(name)
    for role, words in ROLE_TOKENS:
        if any(t in words for t in toks):
            return role
    # fallback for squashed names like 'lefteye' / 'tailtip' / 'frontleg'
    joined = "".join(toks)
    for role, words in ROLE_TOKENS:
        if role == "ignore":
            if "locator" in joined:
                return role
            continue
        if any(len(w) >= 4 and w in joined for w in words):
            return role
    return None


def _side(name: str, pivot: list[float], centre_x: float) -> int:
    toks = set(tokens(name))
    if toks & LEFT:
        return 1
    if toks & RIGHT:
        return -1
    # suffix conventions like legFL / leg_fr
    for t in toks:
        if len(t) == 2 and t[0] in "fbh" and t[1] in "lr":
            return 1 if t[1] == "l" else -1
    dx = float(pivot[0]) - centre_x
    if abs(dx) > 0.5:
        return 1 if dx > 0 else -1
    return 0


def _front(name: str, pivot: list[float], centre_z: float, front_sign: int) -> bool | None:
    toks = set(tokens(name))
    if toks & FRONT:
        return True
    if toks & BACK:
        return False
    return None


def detect_rig(geo: Geometry, overrides: dict | None = None) -> Rig:
    overrides = overrides or {}
    lo, hi = geo.bounds()
    centre = [(lo[i] + hi[i]) / 2 for i in range(3)]
    roots = geo.roots()
    root = roots[0]

    roles: dict[str, str] = {}
    for b in geo.bones:
        r = classify(b["name"])
        if r:
            roles[b["name"]] = r
    # Container bones ('legs', 'arms', 'eyes' groups holding left+right) are not limbs themselves
    kids_of = geo.children()
    for n, r in list(roles.items()):
        if r in LIMB_ROLES or r == "eye":
            same = [k for k in kids_of.get(n, []) if roles.get(k) == r]
            if len(same) >= 2:
                roles[n] = "group"
    # manual overrides: {"head": "skull2", "tails": ["t1","t2"], "ignore": [...]}
    for key, val in overrides.items():
        role = ROLE_ALIASES.get(key, key)
        if role in ("body", "root", "front"):
            continue
        for bone in ([val] if isinstance(val, str) else list(val or [])):
            if geo.bone(bone):
                roles[bone] = role

    # ignore anything under an ignored bone (locators etc.)
    for b in geo.bones:
        if any(roles.get(a) == "ignore" for a in geo.ancestors(b["name"])) and b["name"] not in roles:
            roles[b["name"]] = "ignore"

    rig = Rig(root=root, body=root, roles=roles)
    rig.height_px = hi[1] - lo[1]
    rig.width_px = hi[0] - lo[0]
    rig.length_px = hi[2] - lo[2]
    rig.min_y = lo[1]
    rig.centre = centre

    def pivot(n: str) -> list[float]:
        return [float(x) for x in geo.bone(n).get("pivot", [0, 0, 0])]

    # ---- head: the shallowest bone with the head role
    heads = sorted([n for n, r in roles.items() if r == "head"], key=geo.depth)
    if isinstance(overrides.get("head"), str) and geo.bone(overrides["head"]):
        rig.head = overrides["head"]
    elif heads:
        exact = [h for h in heads if h.lower() == "head"]
        rig.head = exact[0] if exact else heads[0]

    # front direction: head is in front of the body centre
    if rig.head:
        hb = geo.bone_bounds(rig.head)
        hz = ((hb[0][2] + hb[1][2]) / 2) if hb else pivot(rig.head)[2]
        if abs(hz - centre[2]) > 1.0:
            rig.front_sign = -1 if hz < centre[2] else 1
    if overrides.get("front") in ("+z", "z+", "south"):
        rig.front_sign = 1
    elif overrides.get("front") in ("-z", "z-", "north"):
        rig.front_sign = -1

    # ---- body: explicit, else shallowest body-role bone, else root's biggest child
    if isinstance(overrides.get("body"), str) and geo.bone(overrides["body"]):
        rig.body = overrides["body"]
    else:
        bodies = sorted([n for n, r in roles.items() if r == "body"], key=geo.depth)
        if bodies:
            rig.body = bodies[0]
        else:
            kids = geo.children().get(root, [])
            if kids and not geo.bone(root).get("cubes"):
                rig.body = max(kids, key=lambda k: len(geo.descendants(k)))
            else:
                rig.body = root
    if rig.body == rig.head:
        rig.body = root

    rig.necks = sorted([n for n, r in roles.items() if r == "neck"], key=geo.depth)
    jaws = sorted([n for n, r in roles.items() if r == "jaw"], key=geo.depth)
    rig.jaw = jaws[0] if jaws else None
    # eyes: deepest "eye" bones that hold cubes (avoid an empty 'eyes' group if its children exist)
    eye_bones = [n for n, r in roles.items() if r == "eye"]
    leaf_eyes = [n for n in eye_bones if not any(d in eye_bones for d in geo.descendants(n))]
    rig.eyes = sorted(leaf_eyes, key=lambda n: -pivot(n)[0])
    rig.eyelids = [n for n, r in roles.items() if r == "eyelid"]

    # ---- limb chains
    def chains(role: str) -> list[Limb]:
        members = [n for n, r in roles.items() if r == role]
        out = []
        for n in members:
            parent = geo.bone(n).get("parent")
            if parent and roles.get(parent) == role:
                continue  # not a chain start
            chain = [n]
            cur = n
            while True:
                kids = [k for k in geo.children().get(cur, []) if roles.get(k) == role]
                if not kids:
                    break
                cur = kids[0]
                chain.append(cur)
                if len(chain) > 32:
                    break
            p = pivot(n)
            out.append(Limb(bones=chain, side=_side(n, p, centre[0]),
                            front=_front(n, p, centre[2], rig.front_sign), pivot=p))
        return sorted(out, key=lambda l: (rig.front_sign * l.pivot[2], -l.side))

    rig.legs = chains("leg")
    rig.arms = chains("arm")
    rig.wings = chains("wing")
    rig.fins = chains("fin")
    rig.tails = chains("tail")
    rig.ears = chains("ear")
    rig.floppy = chains("floppy")

    # Low-slung "arms" on a 2-legged rig are really front legs (quadrupeds rigged as arm/leg)
    if len(rig.legs) == 2 and len(rig.arms) == 2:
        arm_y = sum(a.pivot[1] for a in rig.arms) / 2
        if arm_y - rig.min_y < 0.45 * rig.height_px:
            for a in rig.arms:
                a.front = True
            for l in rig.legs:
                l.front = False
            rig.legs = rig.arms + rig.legs
            rig.arms = []
            rig.notes.append("Arms are close to the ground: treating them as front legs (quadruped).")

    # Fill in front/back for 4+ legs by position
    if len(rig.legs) >= 4:
        zs = sorted(l.pivot[2] * rig.front_sign for l in rig.legs)
        mid = (zs[0] + zs[-1]) / 2
        for l in rig.legs:
            if l.front is None:
                l.front = (l.pivot[2] * rig.front_sign) < mid

    if not rig.head:
        rig.notes.append("No head bone found (name one 'head' or set rig.head) - head tracking disabled.")
    if not rig.eyes:
        rig.notes.append("No eye bones found - blink animation skipped (name eye cubes' bones 'eye_left'/'eye_right').")
    if not rig.legs and not rig.tails:
        rig.notes.append("No legs or tail found - using a hop cycle for walking.")
    return rig
