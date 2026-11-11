{
onTryHit(target, source, move) {
      if (target !== source && move.type === "Electric") {
        move.accuracy = true;
        if (!target.addVolatile("flashelectric")) {
          this.add("-immune", target, "[from] ability: Flash Electric");
        }
        return null;
      }
    },
onEnd(pokemon) {
      pokemon.removeVolatile("flashelectric");
    },
"condition": {
"noCopy": true,
onStart(target) {
        this.add("-start", target, "ability: Flash Electric");
      },
"onModifyAtkPriority": 5,
onModifyAtk(atk, attacker, defender, move) {
        if (move.type === "Electric" && attacker.hasAbility("flashelectric")) {
          this.debug("Flash Fire boost");
          return this.chainModify(1.5);
        }
      },
"onModifySpAPriority": 5,
onModifySpA(atk, attacker, defender, move) {
        if (move.type === "Electric" && attacker.hasAbility("flashelectric")) {
          this.debug("Flash Fire boost");
          return this.chainModify(1.5);
        }
      },
onEnd(target) {
        this.add("-end", target, "ability: Flash Electric", "[silent]");
      }
},
"flags": {"breakable":1},
"name": "Flash Electric",
"rating": 3.5,
"num": -31127
}
