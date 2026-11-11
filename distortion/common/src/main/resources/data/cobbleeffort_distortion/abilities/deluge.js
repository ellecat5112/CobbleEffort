{
onStart(source) {
      for (const action of this.queue) {
        if (
          action.choice === "runPrimal" &&
          action.pokemon === source &&
          source.species.id === "groudon"
        )
          return;
        if (action.choice !== "runSwitch" && action.choice !== "runPrimal")
          break;
      }
      this.field.setWeather("raindance");
    },
"flags": {},
"name": "Deluge",
"rating": 4,
"num": -31151
}
