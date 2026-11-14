{
num: -4016,
accuracy: true,
basePower: 0,
category: "Status",
name: "Shadow Shed",
pp: 10,
priority: 0,
flags: {},
onHitField(target, source) {
  let removed = false;
  for (const side of this.sides) {
    for (const c of ['reflect', 'lightscreen', 'auroraveil', 'safeguard', 'mist']) {
      if (side.removeSideCondition(c)) removed = true;
    }
  }
  this.add('-activate', source, 'move: Shadow Shed');
  return removed || undefined;
},
secondary: null,
target: "all",
type: "Shadow",
desc: "The user sheds shadow over the field, shattering Reflect, Light Screen, Aurora Veil, Safeguard and Mist on both sides.",
shortDesc: "Removes screens, Safeguard and Mist from both sides."
}
