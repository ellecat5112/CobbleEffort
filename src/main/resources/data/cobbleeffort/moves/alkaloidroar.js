{
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
