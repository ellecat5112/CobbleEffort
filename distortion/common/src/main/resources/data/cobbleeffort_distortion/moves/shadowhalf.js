{
num: -4017,
accuracy: true,
basePower: 0,
category: "Status",
name: "Shadow Half",
pp: 5,
priority: 0,
flags: {},
onHitField(target, source) {
  for (const p of this.getAllActive()) {
    if (p.hp > 1) this.directDamage(Math.floor(p.hp / 2), p, source);
  }
},
secondary: null,
target: "all",
type: "Shadow",
desc: "A shadowy blast splits the field: every Pok\u00e9mon in battle, the user too, loses half its HP.",
shortDesc: "Every active Pok\u00e9mon loses 1/2 of its HP."
}
