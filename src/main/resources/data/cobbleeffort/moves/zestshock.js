{
num: -3038,
accuracy: 100,
basePower: 50,
category: "Special",
name: "Zest Shock",
pp: 15,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
self: {boosts: {spe: 2}},
onAfterMove(pokemon) {
  for (const active of this.getAllActive()) {
    if (active.status === 'slp') active.cureStatus();
  }
},
secondary: null,
target: "normal",
type: "Electric",
desc: "Raises the user's Speed by 2 stages. Every active Pokemon wakes up.",
shortDesc: "Raises the user's Speed by 2. Wakes every active Pokemon.",
contestType: "Cool"
}
