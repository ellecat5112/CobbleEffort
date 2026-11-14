{
onDamagingHit(damage, target, source, move) {
  if (!this.checkMoveMakesContact(move, source, target) || !this.randomChance(3, 10)) return;
  if (this.random(2)) source.trySetStatus('psn', target);
  else source.addVolatile('confusion', target);
},
flags: {},
name: "Alkaloid Sap",
rating: 2,
num: -3048
}
