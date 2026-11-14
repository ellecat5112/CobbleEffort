{
onBasePowerPriority: 23,
onBasePower(basePower, attacker, defender, move) {
  if (move.type === 'Electric') return this.chainModify(1.5);
},
onAfterMoveSecondarySelf(source, target, move) {
  if (move.type === 'Electric' && move.category !== 'Status' && source.hp) {
    this.damage(source.baseMaxhp / 10, source, source, this.dex.abilities.get('overclockedcoil'));
  }
},
flags: {},
name: "Overclocked Coil",
rating: 3.5,
num: -3051
}
