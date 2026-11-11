{
onDamagingHit(damage, target, source, move) {
      if (["Water", "Water"].includes(move.type)) {
        this.boost({ spe: 6 });
      }
    },
"flags": {},
"name": "Water Steam Engine",
"rating": 2,
"num": -31120
}
