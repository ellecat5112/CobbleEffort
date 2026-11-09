({
  name: "Sandy Shockite",
  spritenum: 0,
  megaStone: { "Sandy Shocks": "Sandy Shocks-Mega" },
  itemUser: ["Sandy Shocks"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9105,
  gen: 9,
  isNonstandard: "Past",
})
