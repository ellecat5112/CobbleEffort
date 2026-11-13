{
onTryHitPriority: 1,
onTryHit(target, source, move) {
  if (!source || source === target || source.side === target.side || !source.hasType('Bug')) return;
  this.add('-activate', target, 'ability: Hive Mind');
  if (move.category !== 'Status') {
    const own = source.side.active.filter(p => p && !p.fainted && p.hp > 0);
    const victim = own.length ? this.sample(own) : source;
    const damage = this.actions.getDamage(source, victim, move);
    if (typeof damage === 'number' && damage > 0) this.damage(damage, victim, target, this.effect);
  }
  return null;
},
flags: {breakable: 1},
name: "Hive Mind",
rating: 3.5,
num: -3007
}
