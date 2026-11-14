{
num: -3040,
accuracy: 90,
basePower: 0,
category: "Status",
name: "Green Muse",
pp: 10,
priority: 0,
flags: {protect: 1, reflectable: 1, mirror: 1, metronome: 1},
onHit(target, source) {
  const confused = target.addVolatile('confusion', source);
  const lowered = this.boost({spd: -1}, target, source);
  return !!(confused || lowered);
},
self: {boosts: {spa: 1}},
secondary: null,
target: "normal",
type: "Psychic",
desc: "Confuses the target and lowers its Special Defense by 1 stage. Raises the user's Special Attack by 1 stage.",
shortDesc: "Confuses target, -1 SpD to it, +1 SpA to the user.",
contestType: "Beautiful"
}
