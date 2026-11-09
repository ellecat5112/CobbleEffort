CobbleEffort: Distortion @VERSION@
==================================

A new battle gimmick for Cobblemon. A Pokemon holding the Distortion Crystal, with its trainer wearing the
Distortion Band, distorts: its types turn into their weaknesses, its moves follow, and its colours invert.

A TEST BUILD. What's in it:
  - The Distortion Band and the Distortion Crystal (one crystal for every Pokemon), in the "Distortion" creative tab.
  - A "Distortion" accessory slot (open your Accessories screen); the band goes there.
  - Distorted forms for Giratina, Dialga, Palkia and Arceus (including the Origin forms and every Arceus plate type)
    and NEW: the Charmander line (Charmander, Charmeleon, Charizard), with inverted types and inverted colours.
  - NEW: the distorted Charmander line's flame tail becomes a mermaid tail: scales and a fluke instead of the flame.
  - Distorting in battle, and from the interaction wheel (the radial menu) outside battle.
  - NEW: abilities follow when they're tied to the Pokemon's type: Blaze becomes Torrent, Solar Power becomes the new
    Storm Power (the same, in rain). Abilities that aren't tied to its type stay.
  - NEW: wild Pokemon and NPC trainers' Pokemon holding the crystal (Arceus: a plate) distort on their first move.

HOW TO DISTORT IN BATTLE
  1. Wear the Distortion Band in the Distortion slot.
  2. Give the Distortion Crystal to Giratina, Dialga, Palkia, Charmander, Charmeleon or Charizard. Arceus doesn't
     need it: it distorts with its plate
     (it can only hold one item, and the plates are its power).
  3. In battle, pick "Fight": a Distort button appears next to the back button. Click it (the move tiles switch to
     the distorted moves), then pick a move.
  4. At the start of the turn, before anyone moves, the Pokemon distorts: new types, new look, every move turns into
     its distorted twin for the rest of the battle. Its ability follows if it's tied to its type.
  Once per battle per trainer. It lasts until the battle ends; then the Pokemon is back to normal.
  Wild and NPC Pokemon holding the crystal distort on their own, once per battle (try /pokespawn charizard
  held_item=cobbleeffort_distortion:distortion_crystal).

HOW TO DISTORT OUTSIDE BATTLE (the interaction wheel)
  Send out your Pokemon and open its interaction wheel (the radial menu, where Mega Showdown's Mega Evolve is).
  With the band on and the crystal held (Arceus: a plate), there's a Distort option: the Pokemon distorts on the
  spot and stays distorted (it's saved). Open the wheel again and pick Revert Distortion to undo it; taking the
  crystal away also reverts it.
  One distorted Pokemon per party at a time, and not while you're battling.
  A Pokemon distorted this way enters battle distorted, with its distorted moves, and that counts as your
  distortion for the battle.

Distorted types (each type becomes its weakness):
  Giratina  Ghost/Dragon  -> Dark/Fairy        Dialga  Steel/Dragon  -> Ground/Fairy
  Palkia    Water/Dragon  -> Grass/Fairy       Arceus  its type      -> that type's weakness
  Charmander, Charmeleon  Fire -> Water        Charizard  Fire/Flying -> Water/Electric
  (Mega and Gigantamax Charizard don't distort.)

Distorted moves: every move becomes the same move in its new type. Where a real move is already the exact
opposite, it's that one (Blast Burn -> Hydro Cannon, Sunny Day -> Rain Dance, Trick -> Switcheroo). Otherwise it's
a new move with the same power, accuracy, PP and effects, named to match: Dragon Claw -> Fairy Claw,
Shadow Force -> Dark Force, Roar of Time -> Radiance of Time, Spacial Rend -> Fairy Rend,
Judgment -> Inverse Judgment (the weakness of Arceus's plate type), Earthquake -> Water Earthquake,
Fire Fang -> Water Fang, Air Slash -> Electric Slash, Fire Spin -> Whirlpool.

You can still give a distorted-looking Pokemon with a command:   /pokegive giratina distorted

INSTALL
  Unzip and put ONE jar in your mods folder: the -fabric jar on Fabric, the -neoforge jar on NeoForge.
  Needs: Cobblemon 1.8.4+, Mega Showdown 1.3.3+, Accessories, Architectury API. Install it on the server too.

PLEASE TEST AND REPORT
  New in this build: does the distorted Charmander line show its mermaid tail (no flame, a fin at the tip)? Does
  Charizard's ability turn into Torrent when it distorts (Solar Power: Storm Power)? Does a wild Charizard holding
  the crystal distort in battle, and does the battle carry on normally after?
  Does the Distort option show in the wheel (band on, crystal held)? Does the Pokemon change look when you pick it,
  and back with Revert Distortion, or when you take the crystal? Does it stay distorted after relogging? Does it
  enter battle distorted with the distorted moves?
  And the battle side, if you didn't get to it last time: the Distort button, the distorted moves on the tiles, the
  look and type change, back to normal after the battle, Arceus with a plate.
  If anything breaks, send the crash report or latest.log.

LICENCE
  CC BY-NC-SA 4.0 (non-commercial). The distorted textures are adaptations of Mega Showdown's (CC BY-NC-SA 4.0,
  by yajatkaul and contributors), recoloured. Code and other assets by ellecat5112 / CobbleEffort.
