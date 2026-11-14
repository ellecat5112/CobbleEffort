{
onResidualOrder: 5,
onResidualSubOrder: 3,
onResidual(pokemon) {
  for (const ally of pokemon.alliesAndSelf()) {
    if (ally.volatiles['confusion']) ally.removeVolatile('confusion');
    let restored = false;
    for (const slot of ally.moveSlots) {
      if (slot.pp < slot.maxpp) {
        slot.pp++;
        restored = true;
      }
    }
    if (restored) this.add('-activate', ally, 'ability: Steady Release');
  }
},
flags: {},
name: "Steady Release",
rating: 2.5,
num: -3017
}
