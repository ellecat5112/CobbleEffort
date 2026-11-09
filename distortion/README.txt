CobbleEffort: Distortion @VERSION@
==================================

A new battle gimmick for Cobblemon. A Pokemon holding the Distortion Crystal of its type, with its trainer wearing
the Distortion Band, distorts: its types turn into their weaknesses, its ability and moves follow, and its colours
invert.

THIS IS PHASE 1 (a test build). What's in it:
  - The Distortion Band and 18 Distortion Crystals (one per type), in the "Distortion" creative tab.
  - A new "Distortion" accessory slot (open your Accessories screen); the band goes there.
  - Distorted forms for Giratina, Dialga, Palkia and Arceus, including the Origin forms and every Arceus plate type,
    with inverted types and inverted colours. Not yet triggered in battle: that's phase 2. For now, give one with a
    command:   /pokegive giratina distorted     (or dialga / palkia / arceus)

Distorted types (each type becomes its weakness):
  Giratina  Ghost/Dragon  -> Dark/Fairy        Dialga  Steel/Dragon  -> Ground/Fairy
  Palkia    Water/Dragon  -> Grass/Fairy       Arceus  its type      -> that type's weakness

INSTALL
  Unzip and put ONE jar in your mods folder: the -fabric jar on Fabric, the -neoforge jar on NeoForge.
  Needs: Cobblemon 1.8.4+, Mega Showdown 1.3.3+, Accessories, Architectury API. Install it on the server too.

PLEASE TEST AND REPORT
  Does the game start? Do the items show in the creative tab with their icons? Does the band go in the Distortion
  slot? Do /pokegive ... distorted Pokemon show the inverted colours, and do their summaries show the new types?
  If anything breaks, send the crash report or latest.log.

LICENCE
  CC BY-NC-SA 4.0 (non-commercial). The distorted textures are adaptations of Mega Showdown's (CC BY-NC-SA 4.0,
  by yajatkaul and contributors), recoloured. Code and other assets by ellecat5112 / CobbleEffort.
