{
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
    for (const c of ['spikes', 'toxicspikes', 'stealthrock', 'stickyweb', 'gmaxsteelsurge']) {
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
