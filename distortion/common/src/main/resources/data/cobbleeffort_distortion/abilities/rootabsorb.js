{
onTryHit(target, source, move) {
      if (target !== source && move.type === "Grass") {
        if (!this.heal(target.baseMaxhp / 4)) {
          this.add("-immune", target, "[from] ability: Root Absorb");
        }
        return null;
      }
    },
"flags": {"breakable":1},
"name": "Root Absorb",
"rating": 3.5,
"num": -31106
}
