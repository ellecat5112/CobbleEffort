package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.CobblemonEntities;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.event.EventResult;
import dev.architectury.event.events.common.InteractionEvent;
import dev.architectury.event.events.common.TickEvent;
import io.github.cobbleeffort.digital.Attributes.Attribute;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.trading.ItemCost;
import net.minecraft.world.item.trading.Merchant;
import net.minecraft.world.item.trading.MerchantOffer;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.AABB;

import java.util.List;

/**
 * The black market: now and then a shady Vademon or Etemon turns up near a player in the dark (at night, underground
 * or in the Dark Area) and stays ten minutes. Use it to trade: Dark Spores, "stolen" Digitama, Virus Chips, Chrome
 * Digizoid and glitch cards for emeralds or Virus Fragments.
 */
final class BlackMarket {
    static final String TAG = "cobbleeffort_digital_merchant";
    static final List<String> SPECIES = List.of("vademon", "etemon");
    /** One check per player every 20 seconds: this chance while they're somewhere dark. */
    static final int CHANCE = 240;
    static final long STAY_TICKS = 20L * 60 * 10;

    private BlackMarket() {
    }

    static void init() {
        TickEvent.SERVER_POST.register(server -> {
            if (server.getTickCount() % 400 != 0) return;
            for (ServerPlayer p : server.getPlayerList().getPlayers()) {
                try {
                    tick(p);
                } catch (Throwable t) {
                    Digital.LOG.error("Black market tick failed", t);
                }
            }
        });
        InteractionEvent.INTERACT_ENTITY.register((player, entity, hand) -> {
            if (!(entity instanceof PokemonEntity e) || !e.getTags().contains(TAG)) return EventResult.pass();
            if (!player.level().isClientSide && !e.isBattling()) new Shop(player).openTradingScreen(player,
                    Component.translatable(Digital.MOD_ID + ".merchant.name", e.getPokemon().getSpecies().getTranslatedName()), 1);
            return EventResult.interruptTrue();
        });
    }

    static boolean dark(ServerPlayer p) {
        ServerLevel level = p.serverLevel();
        BlockPos pos = p.blockPosition();
        boolean darkArea = level.getBiome(pos).unwrapKey().map(k -> k.location().getPath().equals("dark_area")).orElse(false);
        return darkArea || level.isNight() || (!level.canSeeSky(pos) && pos.getY() < 40);
    }

    static void tick(ServerPlayer p) {
        ServerLevel level = p.serverLevel();
        for (PokemonEntity e : level.getEntitiesOfClass(PokemonEntity.class, new AABB(p.blockPosition()).inflate(96), x -> x.getTags().contains(TAG))) {
            long born = e.getPokemon().getPersistentData().getLong(TAG);
            if (level.getGameTime() - born > STAY_TICKS || born == 0) e.discard();
            else return;                                          // one about already
        }
        if (!dark(p) || level.getRandom().nextInt(CHANCE) != 0) return;
        String id = SPECIES.get(level.getRandom().nextInt(SPECIES.size()));
        if (PokemonSpecies.INSTANCE.getByIdentifier(ResourceLocation.fromNamespaceAndPath("cobbleeffort", id)) == null) return;
        Pokemon pk = PokemonProperties.Companion.parse("cobbleeffort:" + id + " level=30 uncatchable").create();
        pk.getPersistentData().putLong(TAG, level.getGameTime());
        PokemonEntity e = new PokemonEntity(level, pk, CobblemonEntities.POKEMON);
        double a = level.getRandom().nextDouble() * Math.PI * 2;
        int x = (int) (p.getX() + Math.cos(a) * 6), z = (int) (p.getZ() + Math.sin(a) * 6);
        int y = p.blockPosition().getY();
        if (level.canSeeSky(p.blockPosition())) y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
        net.minecraft.world.entity.Mob mob = e;
        mob.moveTo(x + 0.5, y, z + 0.5, level.getRandom().nextFloat() * 360F, 0F);
        mob.setPersistenceRequired();
        mob.addTag(TAG);
        mob.setCustomName(Component.translatable(Digital.MOD_ID + ".merchant.name", pk.getSpecies().getTranslatedName()).withStyle(ChatFormatting.DARK_PURPLE));
        mob.setCustomNameVisible(true);
        level.addFreshEntity(mob);
        p.displayClientMessage(Component.translatable(Digital.MOD_ID + ".merchant.appears").withStyle(ChatFormatting.DARK_PURPLE), true);
    }

    /** The shady merchant's wares (a fresh stock each time you open it). */
    static final class Shop implements Merchant {
        private Player trader;
        private final MerchantOffers offers = new MerchantOffers();

        Shop(Player player) {
            ItemCost virus = new ItemCost(Digital.FRAGMENTS.get(Attribute.VIRUS).get(), 12);
            offers.add(new MerchantOffer(new ItemCost(Items.EMERALD, 8), new ItemStack(Digital.DARK_SPORE.get()), 3, 0, 0.05F));
            offers.add(new MerchantOffer(virus, new ItemStack(Digital.DARK_SPORE.get()), 3, 0, 0.05F));
            offers.add(new MerchantOffer(new ItemCost(Items.EMERALD, 10), new ItemStack(Digital.DIGITAMA.get()), 2, 0, 0.05F));
            offers.add(new MerchantOffer(new ItemCost(Items.EMERALD, 6), new ItemStack(Digital.CHIPS.get(Attribute.VIRUS).get()), 4, 0, 0.05F));
            offers.add(new MerchantOffer(new ItemCost(Digital.FRAGMENTS.get(Attribute.VIRUS).get(), 16), new ItemStack(Digital.CHROME_INGOT.get()), 4, 0, 0.05F));
            offers.add(new MerchantOffer(new ItemCost(Items.EMERALD, 5), new ItemStack(Digital.CARD_ITEMS.get("dot_virus").get(), 2), 4, 0, 0.05F));
            offers.add(new MerchantOffer(new ItemCost(Items.EMERALD, 5), new ItemStack(Digital.CARD_ITEMS.get("bug_card").get(), 2), 4, 0, 0.05F));
            offers.add(new MerchantOffer(new ItemCost(Items.EMERALD, 24), new ItemStack(Digital.DIGIEGG_COURAGE.get()), 1, 0, 0.05F));
        }

        @Override
        public void setTradingPlayer(Player player) {
            trader = player;
        }

        @Override
        public Player getTradingPlayer() {
            return trader;
        }

        @Override
        public MerchantOffers getOffers() {
            return offers;
        }

        @Override
        public void overrideOffers(MerchantOffers o) {
        }

        @Override
        public void notifyTrade(MerchantOffer offer) {
            offer.increaseUses();
        }

        @Override
        public void notifyTradeUpdated(ItemStack stack) {
        }

        @Override
        public int getVillagerXp() {
            return 0;
        }

        @Override
        public void overrideXp(int xp) {
        }

        @Override
        public boolean showProgressBar() {
            return false;
        }

        @Override
        public SoundEvent getNotifyTradeSound() {
            return SoundEvents.WANDERING_TRADER_YES;
        }

        @Override
        public boolean isClientSide() {
            return false;
        }
    }
}
