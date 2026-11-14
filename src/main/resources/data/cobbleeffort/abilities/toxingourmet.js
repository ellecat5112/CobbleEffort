{
onTryHitPriority: 1,
onTryHit(target, source, move) {
  if (target !== source && (move.type === 'Poison' || move.type === 'Grass')) {
    if (!this.heal(target.baseMaxhp / 4)) this.add('-immune', target, '[from] ability: Toxin Gourmet');
    return null;
  }
},
flags: {breakable: 1},
name: "Toxin Gourmet",
rating: 3.5,
num: -3014
}
