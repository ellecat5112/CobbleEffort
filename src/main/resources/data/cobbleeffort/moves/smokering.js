{
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
