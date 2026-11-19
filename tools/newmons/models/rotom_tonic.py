"""Tonic Rotom (Electric/Poison), after the user's Rotom doodle sheet (artist not named): Rotom inside a bottle of
tonic. A round orange bottle with a white cap, a white label band with a black cross, and Rotom's teal lens eyes and a
zig-zag grin; one teal plasma arm flexes its muscle and the other holds up a little dose of medicine.

Front is -z, y is up. 26 units tall; about 0.9 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import face_on, palette, solid
from _route import tone

P = palette({"aura": (90, 230, 190), "aura_light": (210, 255, 240), "iris": (60, 210, 190)})
HEIGHT = 26
SCALE = round(0.9 * 16 / HEIGHT, 3)
HITBOX = [0.8, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an orange tonic bottle with a white cap, a cross on its label and teal plasma arms, one flexing"


def bottle(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and 4.0 <= y <= 7.6:                # the label band with a black cross
        if (abs(x) < 0.6 and 4.6 < y < 7.0) or (abs(y - 5.8) < 0.6 and abs(x) < 1.8):
            return p["black"], None
        return p["white"], None
    return face_on(P, (0, 11, -4.4), eyes=[(-1.8, 0.8, 1.4), (1.8, 0.8, 1.4)], mouth=(0, -1.6, 3.2, 1.0, 5))(
        x, y, z, face=face, variant=variant)


def build() -> Model:
    m = Model("rotom_tonic")
    top = m.bone("rotom_tonic", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 4.4, 4.4, 1, 15, bottle, cut=1.4)                           # the bottle (its face)
    m.round_box(bd, 0, 0, 2.6, 2.6, 15, 17, solid(P, "orange_light"), cut=0.8)        # neck
    m.round_box(bd, 0, 0, 2.8, 2.8, 17, 20, solid(P, "white"), cut=0.9)               # cap
    arm = m.bone("arm_left", bd, (4.4, 10, 0))
    rod(m, arm, (4.4, 9, 0), (8.5, 10, -1), 2.0, solid(P, "aura", glow=True), extend=0.4)      # the flexing arm
    rod(m, arm, (8.5, 10, -1), (8.0, 15.5, -1.5), 2.0, solid(P, "aura", glow=True), extend=0.4)
    m.round_box(arm, 8.0, -1.5, 1.5, 1.5, 15.5, 18, solid(P, "aura_light", glow=True), cut=0.6)
    arm2 = m.bone("arm_right", bd, (-4.4, 10, 0))
    rod(m, arm2, (-4.4, 9, 0), (-8.5, 12, -2), 1.6, solid(P, "aura", glow=True), extend=0.4)  # holding up a dose
    m.box(arm2, -9.5, 12, -2.8, -8, 17, -1.4, solid(P, "aura_light"))
    m.box(arm2, -9.3, 16.8, -2.6, -8.2, 18, -1.6, solid(P, "grey"))
    return m
