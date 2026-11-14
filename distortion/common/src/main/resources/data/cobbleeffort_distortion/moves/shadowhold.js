{
num: -4012,
accuracy: 80,
basePower: 0,
category: "Status",
name: "Shadow Hold",
pp: 10,
priority: 0,
flags: {protect: 1, reflectable: 1, mirror: 1},
onHit(target, source, move) {
  return target.addVolatile('trapped', source, move, 'trapper');
},
secondary: null,
target: "allAdjacentFoes",
type: "Shadow",
desc: "Shadowy bonds hold every foe so they can't flee or switch out.",
shortDesc: "Foes can't switch out."
}
