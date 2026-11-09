({
  name: "Raging Boltite",
  spritenum: 0,
  megaStone: { "Raging Bolt": "Raging Bolt-Mega" },
  itemUser: ["Raging Bolt"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9109,
  gen: 9,
  isNonstandard: "Past",
})
