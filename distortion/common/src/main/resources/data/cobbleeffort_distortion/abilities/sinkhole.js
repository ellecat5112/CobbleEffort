{
onTryHit(target, source, move) {
      if (target !== source && move.type === "Ground") {
        if (!this.boost({ spa: 1 })) {
          this.add("-immune", target, "[from] ability: Sinkhole");
        }
        return null;
      }
    },
onAnyRedirectTarget(target, source, source2, move) {
      if (move.type !== "Ground" || move.flags["pledgecombo"]) return;
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
            "ability: Sinkhole",
          );
        }
        return this.effectState.target;
      }
    },
"flags": {"breakable":1},
"name": "Sinkhole",
"rating": 3,
"num": -31113
}
