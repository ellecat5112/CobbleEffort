{
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
