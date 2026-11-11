{
onTryHit(target, source, move) {
      if (target !== source && move.type === "Water") {
        move.accuracy = true;
        if (!target.addVolatile("flashflood")) {
          this.add("-immune", target, "[from] ability: Flash Flood");
        }
        return null;
      }
    },
onEnd(pokemon) {
      pokemon.removeVolatile("flashflood");
    },
"condition": {
"noCopy": true,
onStart(target) {
        this.add("-start", target, "ability: Flash Flood");
      },
"onModifyAtkPriority": 5,
onModifyAtk(atk, attacker, defender, move) {
        if (move.type === "Water" && attacker.hasAbility("flashflood")) {
          this.debug("Flash Fire boost");
          return this.chainModify(1.5);
        }
      },
"onModifySpAPriority": 5,
onModifySpA(atk, attacker, defender, move) {
        if (move.type === "Water" && attacker.hasAbility("flashflood")) {
          this.debug("Flash Fire boost");
          return this.chainModify(1.5);
        }
      },
onEnd(target) {
        this.add("-end", target, "ability: Flash Flood", "[silent]");
      }
},
"flags": {"breakable":1},
"name": "Flash Flood",
"rating": 3.5,
"num": -31108
}
