"""The Nicodex's own abilities and moves (the user's design: 18 nicotine- and tobacco-inspired Pokémon living in the
Ashtray Wastes). Merged into build.py's CUSTOM_ABILITIES / CUSTOM_MOVES; tested in node against Cobblemon's Showdown.
"""
HAZARDS = "['spikes', 'toxicspikes', 'stealthrock', 'stickyweb', 'gmaxsteelsurge']"

NICO_ABILITIES = {
    "pestdeterrent": {
        "name": "Pest Deterrent",
        "js": """{
onStart(pokemon) {
  let activated = false;
  for (const target of pokemon.adjacentFoes()) {
    if (!target.hasType('Bug')) continue;
    if (!activated) {
      this.add('-ability', pokemon, 'Pest Deterrent', 'boost');
      activated = true;
    }
    if (target.volatiles['substitute']) this.add('-immune', target);
    else this.boost({atk: -1}, target, pokemon, null, true);
  }
},
flags: {},
name: "Pest Deterrent",
rating: 2,
num: -3012
}
""",
        "lang": "Its sticky leaves ooze a mild toxin that Bug Pokémon can't stand: when it enters battle, the Attack of "
                "every opposing Bug-type Pokémon falls.",
    },
    "cloudchaser": {
        "name": "Cloud Chaser",
        "js": """{
onStart(source) {
  this.field.addPseudoWeather('cloudchaser', source);
},
condition: {
  duration: 5,
  onFieldStart(field, source) {
    this.add('-fieldstart', 'ability: Cloud Chaser');
  },
  onBasePowerPriority: 6,
  onBasePower(basePower, attacker, defender, move) {
    if (move.type === 'Electric') return this.chainModify([5325, 4096]);
  },
  onModifyAccuracyPriority: -1,
  onModifyAccuracy(accuracy, target, source, move) {
    if (typeof accuracy !== 'number' || !source || source.hasType('Electric')) return;
    return this.chainModify([3277, 4096]);
  },
  onFieldResidualOrder: 27,
  onFieldResidualSubOrder: 3,
  onFieldEnd() {
    this.add('-fieldend', 'ability: Cloud Chaser');
  }
},
flags: {},
name: "Cloud Chaser",
rating: 3,
num: -3013
}
""",
        "lang": "On entering battle it exhales a thick, sweet-smelling fog that lasts five turns: Electric-type moves "
                "grow 30% stronger in it, and the moves of non-Electric Pokémon lose a fifth of their accuracy.",
        "battle": {"cobblemon.battle.fieldstart.cloudchaser": "A thick, sweet-smelling fog rolled across the field!",
                   "cobblemon.battle.fieldend.cloudchaser": "The fog cleared."},
    },
    "toxingourmet": {
        "name": "Toxin Gourmet",
        "js": """{
onTryHitPriority: 1,
onTryHit(target, source, move) {
  if (target !== source && (move.type === 'Poison' || move.type === 'Grass')) {
    if (!this.heal(target.baseMaxhp / 4)) this.add('-immune', target, '[from] ability: Toxin Gourmet');
    return null;
  }
},
flags: {breakable: 1},
name: "Toxin Gourmet",
rating: 3.5,
num: -3014
}
""",
        "lang": "It feeds on plant toxins: Poison- and Grass-type moves don't harm it, they restore 1/4 of its HP.",
    },
    "resincoat": {
        "name": "Resin Coat",
        "js": """{
onSourceModifyDamage(damage, source, target, move) {
  if (move.flags['contact']) return this.chainModify(0.5);
},
onDamagingHit(damage, target, source, move) {
  if (this.checkMoveMakesContact(move, source, target, true)) {
    this.add('-ability', target, 'Resin Coat');
    this.boost({spe: -1}, source, target, null, true);
  }
},
flags: {breakable: 1},
name: "Resin Coat",
rating: 3.5,
num: -3015
}
""",
        "lang": "Its body is thick with sticky tar: moves that make contact deal half damage, and the attacker comes "
                "away gummed up, its Speed lowered.",
    },
    "lingeringscent": {
        "name": "Lingering Scent",
        "js": """{
onFaint(pokemon) {
  this.field.addPseudoWeather('lingeringscent', pokemon);
},
condition: {
  duration: 4,
  onFieldStart() {
    this.add('-fieldstart', 'ability: Lingering Scent');
  },
  onFieldResidualOrder: 26,
  onFieldResidualSubOrder: 2,
  onFieldResidual() {
    for (const p of this.getAllActive()) {
      if (p.fainted || !p.hp || p.hasType('Ghost')) continue;
      this.damage(p.baseMaxhp / 16, p, null, this.dex.conditions.get('lingeringscent'));
    }
  },
  onFieldEnd() {
    this.add('-fieldend', 'ability: Lingering Scent');
  }
},
flags: {},
name: "Lingering Scent",
rating: 2,
num: -3016
}
""",
        "lang": "Even after it faints, its stale haze hangs over the field for three turns, taking 1/16 of their HP "
                "from every Pokémon that isn't Ghost type at the end of each turn.",
        "battle": {"cobblemon.battle.fieldstart.lingeringscent": "A stale haze lingers over the field...",
                   "cobblemon.battle.fieldend.lingeringscent": "The stale haze finally cleared.",
                   "cobblemon.battle.damage.lingeringscent": "%1$s choked on the stale haze!"},
    },
    "steadyrelease": {
        "name": "Steady Release",
        "js": """{
onResidualOrder: 5,
onResidualSubOrder: 3,
onResidual(pokemon) {
  for (const ally of pokemon.alliesAndSelf()) {
    if (ally.volatiles['confusion']) ally.removeVolatile('confusion');
    let restored = false;
    for (const slot of ally.moveSlots) {
      if (slot.pp < slot.maxpp) {
        slot.pp++;
        restored = true;
      }
    }
    if (restored) this.add('-activate', ally, 'ability: Steady Release');
  }
},
flags: {},
name: "Steady Release",
rating: 2.5,
num: -3017
}
""",
        "lang": "Its steady psychic pulse calms its side: at the end of every turn it and its allies snap out of "
                "confusion and each of their moves regains 1 PP.",
        "battle": {"cobblemon.battle.activate.steadyrelease": "%1$s was steadied by a calm, rhythmic pulse!"},
    },
    "patinapolish": {
        "name": "Patina Polish",
        "js": """{
onDamagingHit(damage, target, source, move) {
  if (move.type === 'Fire' || move.type === 'Poison') this.boost({def: 1, spd: 1}, target, target);
},
flags: {},
name: "Patina Polish",
rating: 3,
num: -3018
}
""",
        "lang": "Heat and smoke only deepen its golden patina: when a Fire- or Poison-type move hits it, its Defense "
                "and Sp. Def rise by one stage.",
    },
    "hooked": {
        "name": "Hooked",
        "js": """{
onDamagingHit(damage, target, source, move) {
  if (source && source !== target && source.hp && this.checkMoveMakesContact(move, source, target)) {
    source.addVolatile('hooked', target);
  }
},
condition: {
  duration: 2,
  onStart(pokemon) {
    this.add('-start', pokemon, 'ability: Hooked');
  },
  onTrapPokemon(pokemon) {
    pokemon.tryTrap();
  },
  onEnd(pokemon) {
    this.add('-end', pokemon, 'ability: Hooked', '[silent]');
  }
},
flags: {},
name: "Hooked",
rating: 3,
num: -3019
}
""",
        "lang": "One taste and they keep coming back: a Pokémon that makes contact with it can't switch out on the "
                "next turn.",
        "battle": {"cobblemon.battle.start.hooked": "%1$s got hooked and can't bring itself to leave!"},
    },
}

NICO_MOVES = {
    "cherryflick": {
        "base": "quickattack", "num": -3020, "name": "Cherry Flick", "type": "Fire", "category": "Physical",
        "basePower": 40, "accuracy": 100, "pp": 30, "priority": 1,
        "flags": {"contact": 1, "protect": 1, "mirror": 1, "metronome": 1},
        "secondary": {"chance": 30, "status": "brn"}, "contestType": "Cool",
        "desc": "Usually goes first. 30% chance to burn the target.", "shortDesc": "Usually goes first. 30% burn.",
        "lang": "The user flicks the glowing tip of its snout at the target faster than it can react, scattering hot "
                "ash. Usually goes first, and may leave a burn.",
    },
    "bubblefilter": {
        "name": "Bubble Filter",
        "js": """{
num: -3021,
accuracy: 100,
basePower: 70,
category: "Special",
name: "Bubble Filter",
pp: 15,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
onAfterHit(target, pokemon, move) {
  if (!pokemon.hp) return;
  for (const c of %HAZARDS%) {
    if (pokemon.side.removeSideCondition(c)) {
      this.add('-sideend', pokemon.side, this.dex.conditions.get(c).name, '[from] move: Bubble Filter', '[of] ' + pokemon);
    }
  }
  for (const ally of pokemon.side.pokemon) ally.cureStatus();
},
onAfterSubDamage(damage, target, pokemon, move) {
  if (!pokemon.hp) return;
  for (const c of %HAZARDS%) {
    if (pokemon.side.removeSideCondition(c)) {
      this.add('-sideend', pokemon.side, this.dex.conditions.get(c).name, '[from] move: Bubble Filter', '[of] ' + pokemon);
    }
  }
  for (const ally of pokemon.side.pokemon) ally.cureStatus();
},
secondary: {chance: 30, status: 'brn'},
target: "normal",
type: "Water",
desc: "Clears hazards from the user's side and cures the status of every Pokemon in its party. 30% chance to burn the target.",
shortDesc: "Clears own hazards, cures party status. 30% burn.",
contestType: "Beautiful"
}
""".replace("%HAZARDS%", HAZARDS),
        "lang": "The user draws the air on its side through its bubbling water, filtering away hazards and curing "
                "its party's status conditions, and blasts the target with scalding steam that may burn it.",
    },
    "frostbitedrag": {
        "base": "icefang", "num": -3022, "name": "Frostbite Drag", "type": "Ice", "category": "Physical",
        "basePower": 80, "accuracy": 100, "pp": 15, "priority": -3, "infiltrates": True,
        "flags": {"contact": 1, "bite": 1, "mirror": 1, "metronome": 1}, "secondary": None, "contestType": "Tough",
        "desc": "Moves late in the turn. Ignores Protect, substitutes and the target's screens.",
        "shortDesc": "Moves late. Bypasses Protect, Substitute and screens.",
        "lang": "A numbing menthol bite: the target doesn't feel it until the turn is ending, and nothing it hides "
                "behind, Protect, a substitute or a screen, can stop it.",
    },
    "spittoonslug": {
        "name": "Spittoon Slug",
        "js": """{
num: -3023,
accuracy: 100,
basePower: 75,
category: "Physical",
name: "Spittoon Slug",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1, bullet: 1},
onBasePower(basePower, source, target, move) {
  if (target.item) return this.chainModify(1.5);
},
secondary: null,
target: "normal",
type: "Fighting",
desc: "Power is multiplied by 1.5 if the target is holding an item.",
shortDesc: "1.5x damage if the target holds an item.",
contestType: "Tough"
}
""",
        "lang": "The user spits a slug of concentrated dark juice with bullet-like force. It hits harder if the target "
                "is holding an item.",
    },
    "smother": {
        "base": "sandtomb", "num": -3024, "name": "Smother", "type": "Ground", "category": "Physical",
        "basePower": 60, "accuracy": 90, "pp": 15,
        "flags": {"protect": 1, "mirror": 1, "metronome": 1}, "secondary": {"chance": 20, "status": "brn"},
        "contestType": "Tough",
        "desc": "Traps the target for 4-5 turns, hurting it every turn. 20% chance to burn the target.",
        "shortDesc": "Traps and damages for 4-5 turns. 20% burn.",
        "lang": "The user buries the target in hot ash, trapping it and hurting it every turn for four or five turns. "
                "It may also leave a burn.",
        "battle": {"cobblemon.battle.activate.smother": "%1$s was buried in hot ash!",
                   "cobblemon.battle.damage.smother": "%1$s is hurt by the smothering ash!",
                   "cobblemon.battle.end.smother": "%1$s dug itself out of the ash!"},
    },
    "smokering": {
        "name": "Smoke Ring",
        "js": """{
num: -3025,
accuracy: 100,
basePower: 70,
category: "Special",
name: "Smoke Ring",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
secondary: {
  chance: 100,
  onHit(target, source, move) {
    if (source.isActive) target.addVolatile('trapped', source, move, 'trapper');
  },
  boosts: {spd: -1}
},
target: "normal",
type: "Ghost",
desc: "Prevents the target from switching out and lowers its Sp. Def by 1.",
shortDesc: "Traps the target. Lowers its Sp. Def by 1.",
contestType: "Cool"
}
""",
        "lang": "The user blows a glowing ring of ghost-fire around the target, trapping it so it can't switch out "
                "and lowering its Sp. Def.",
    },
    "liptingle": {
        "name": "Lip Tingle",
        "js": """{
num: -3026,
accuracy: true,
basePower: 0,
category: "Status",
name: "Lip Tingle",
pp: 10,
priority: 0,
flags: {snatch: 1, metronome: 1},
boosts: {spe: 2, spa: 2},
onHit(pokemon) {
  pokemon.addVolatile('liptingle');
},
condition: {
  duration: 2,
  onEnd(pokemon) {
    if (!pokemon.hp) return;
    this.add('-activate', pokemon, 'move: Lip Tingle');
    this.boost({spe: -1, spa: -1}, pokemon, pokemon);
  }
},
secondary: null,
target: "self",
type: "Fairy",
desc: "Raises the user's Speed and Sp. Atk by 2 stages; at the end of the next turn they fall by 1 stage each.",
shortDesc: "+2 Spe/SpA; -1 Spe/SpA at the end of next turn.",
contestType: "Cute"
}
""",
        "lang": "An icy minty jolt sharply raises the user's Speed and Sp. Atk, but at the end of the next turn the "
                "buzz fades and both fall by one stage.",
        "battle": {"cobblemon.battle.activate.liptingle": "%1$s's minty buzz wore off..."},
    },
    "flintsnap": {
        "base": "flashcannon", "num": -3027, "name": "Flint Snap", "type": "Steel", "category": "Special",
        "basePower": 70, "accuracy": True, "pp": 15,
        "flags": {"protect": 1, "mirror": 1, "metronome": 1}, "secondary": {"chance": 50, "status": "brn"},
        "contestType": "Cool",
        "desc": "This move does not check accuracy. 50% chance to burn the target.",
        "shortDesc": "Never misses. 50% chance to burn.",
        "lang": "The user snaps its lid open and strikes its flint wheel, throwing a windproof spark that never misses "
                "and often leaves a burn.",
    },
    "sneezefit": {
        "name": "Sneeze Fit",
        "js": """{
num: -3028,
accuracy: 90,
basePower: 60,
category: "Special",
name: "Sneeze Fit",
pp: 10,
priority: -6,
flags: {protect: 1, mirror: 1, metronome: 1, noassist: 1, failcopycat: 1},
forceSwitch: true,
onAfterHit(target, pokemon) {
  for (const side of [pokemon.side, target.side]) {
    for (const c of %HAZARDS%) {
      if (side.removeSideCondition(c)) {
        this.add('-sideend', side, this.dex.conditions.get(c).name, '[from] move: Sneeze Fit', '[of] ' + pokemon);
      }
    }
  }
},
secondary: null,
target: "normal",
type: "Normal",
desc: "Forces the target to switch to a random ally and clears entry hazards from both sides. Goes last.",
shortDesc: "Forces the target out; clears all hazards. Goes last.",
contestType: "Cute"
}
""".replace("%HAZARDS%", HAZARDS),
        "lang": "The user lets out a violent sneeze of aromatic dust that blows the target out of battle and sweeps "
                "entry hazards off both sides. It goes last.",
    },
    "alkaloidroar": {
        "name": "Alkaloid Roar",
        "js": """{
num: -3029,
accuracy: 100,
basePower: 85,
category: "Special",
name: "Alkaloid Roar",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, sound: 1, bypasssub: 1, metronome: 1},
secondary: {
  chance: 30,
  onHit(target, source) {
    const status = target.getStat('def', true, true) >= target.getStat('spd', true, true) ? 'par' : 'psn';
    target.trySetStatus(status, source);
  }
},
target: "normal",
type: "Dragon",
desc: "Hits through substitutes. 30% chance to paralyze the target if its Defense is the higher of its two defenses, or to poison it otherwise.",
shortDesc: "Bypasses Substitute. 30% par (Def >= SpD) or psn.",
contestType: "Tough"
}
""",
        "lang": "The user lets out a ringing roar laced with alkaloids that cuts through substitutes. It may paralyze "
                "a Pokémon with sturdy Defense, or poison one that relies on its Sp. Def.",
    },
}
