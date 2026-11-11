{
onTryHit(target, source, move) {
      if (target !== source && move.type === "Grass") {
        if (!this.boost({ spa: 1 })) {
          this.add("-immune", target, "[from] ability: Verdant Drain");
        }
        return null;
      }
    },
onAnyRedirectTarget(target, source, source2, move) {
      if (move.type !== "Grass" || move.flags["pledgecombo"]) return;
      const redirectTarget = ["randomNormal", "adjacentFoe"].includes(
        move.target,
      )
        ? "normal"
        : move.target;
      if (this.validTarget(this.effectState.target, source, redirectTarget)) {
        if (move.smartTarget) move.smartTarget = false;
        if (this.effectState.target !== target) {
          this.add(
            "-activate",
            this.effectState.target,
            "ability: Verdant Drain",
          );
        }
        return this.effectState.target;
      }
    },
"flags": {"breakable":1},
"name": "Verdant Drain",
"rating": 3,
"num": -31140
}
