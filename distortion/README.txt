CobbleEffort: Distortion @VERSION@
==================================

A new battle gimmick for Cobblemon. A Pokemon holding the Distortion Crystal, with its trainer wearing the
Distortion Band, distorts: its types turn into their weaknesses, its moves follow, and its colours invert.

THIS IS PHASE 2 (a test build). What's in it:
  - The Distortion Band and the Distortion Crystal (one crystal for every Pokemon), in the "Distortion" creative tab.
  - A "Distortion" accessory slot (open your Accessories screen); the band goes there.
  - Distorted forms for Giratina, Dialga, Palkia and Arceus, including the Origin forms and every Arceus plate type,
    with inverted types and inverted colours.
  - NEW: distorting in battle.

HOW TO DISTORT IN BATTLE
  1. Wear the Distortion Band in the Distortion slot.
  2. Give the Distortion Crystal to Giratina, Dialga or Palkia. Arceus doesn't need it: it distorts with its plate
     (it can only hold one item, and the plates are its power).
  3. In battle, pick "Fight": a Distort button appears next to the back button. Click it (the move tiles switch to
     the distorted moves), then pick a move.
  4. At the start of the turn, before anyone moves, the Pokemon distorts: new types, new look, every move turns into
     its distorted twin for the rest of the battle. Its ability stays.
  Once per battle per trainer. It lasts until the battle ends; then the Pokemon is back to normal.
  Wild and NPC Pokemon holding the crystal can't distort on their own (yet).

Distorted types (each type becomes its weakness):
  Giratina  Ghost/Dragon  -> Dark/Fairy        Dialga  Steel/Dragon  -> Ground/Fairy
  Palkia    Water/Dragon  -> Grass/Fairy       Arceus  its type      -> that type's weakness

Distorted moves: every move becomes the same move in its new type. Where a real move is already the exact
opposite, it's that one (Blast Burn -> Hydro Cannon, Sunny Day -> Rain Dance, Trick -> Switcheroo). Otherwise it's
a new move with the same power, accuracy, PP and effects, named to match: Dragon Claw -> Fairy Claw,
Shadow Force -> Dark Force, Roar of Time -> Radiance of Time, Spacial Rend -> Fairy Rend,
Judgment -> Inverse Judgment (the weakness of Arceus's plate type), Earthquake -> Water Earthquake.

You can still give a distorted-looking Pokemon with a command:   /pokegive giratina distorted

INSTALL
  Unzip and put ONE jar in your mods folder: the -fabric jar on Fabric, the -neoforge jar on NeoForge.
  Needs: Cobblemon 1.8.4+, Mega Showdown 1.3.3+, Accessories, Architectury API. Install it on the server too.

PLEASE TEST AND REPORT
  Does the Distort button show (band on, crystal held)? Do the tiles show the distorted moves when it's on? Does
  the Pokemon change look and types when it distorts, and use the distorted move? Is it back to normal after the
  battle? Does Arceus distort with a plate?
  If anything breaks, send the crash report or latest.log.

LICENCE
  CC BY-NC-SA 4.0 (non-commercial). The distorted textures are adaptations of Mega Showdown's (CC BY-NC-SA 4.0,
  by yajatkaul and contributors), recoloured. Code and other assets by ellecat5112 / CobbleEffort.
