{
onSourceModifyDamage(damage, source, target, move) {
  if (move.type === 'Fire' && target.getMoveHitData(move).typeMod > 0) return this.chainModify(0.5);
},
onDamagingHit(damage, target, source, move) {
  if (move.type !== 'Fire') return;
  let activated = false;
  for (const foe of target.adjacentFoes()) {
    if (!activated) {
      this.add('-ability', target, 'Slow Melt');
      activated = true;
    }
    this.boost({spe: -1}, foe, target, null, true);
  }
},
flags: {breakable: 1},
name: "Slow Melt",
rating: 3,
num: -3032
}
