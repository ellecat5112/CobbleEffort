{
onDamagingHit(damage, target, source, move) {
  if (move.type === 'Fire' || move.type === 'Poison') this.boost({def: 1, spd: 1}, target, target);
},
flags: {},
name: "Patina Polish",
rating: 3,
num: -3018
}
