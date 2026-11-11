package io.github.cobbleeffort.kanto;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.battles.BattleFaintedEvent;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import com.mojang.datafixers.util.Pair;
import dev.architectury.event.events.common.LifecycleEvent;
import io.github.cobbleeffort.kanto.mixin.StructureTemplatePoolAccessor;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.levelgen.structure.pools.StructurePoolElement;
import net.minecraft.world.level.levelgen.structure.pools.StructureTemplatePool;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/** The add-on's hooks into Cobblemon and Minecraft: Essence of Olde drops, Gen 1-only Kanto, the lab in villages. */
public final class KantoEvents {
    /** One Gen 1 Pokémon defeated in battle: this chance of Essence of Olde. */
    static final double ESSENCE_CHANCE = 0.05;
    /** The lab's weight among each village's houses (a plains village's houses weigh about 200 in all). */
    static final int LAB_WEIGHT = 3;
    private static final String[] VILLAGES = {"plains", "desert", "savanna", "snowy", "taiga"};
    private static final Random RANDOM = new Random();

    private KantoEvents() {
    }

    public static void init() {
        CobblemonEvents.BATTLE_FAINTED.subscribe(Priority.NORMAL, event -> {
            MinecraftServer server = com.cobblemon.mod.common.util.DistributionUtilsKt.server();
            Runnable drop = () -> {
                try {
                    essence(event);
                } catch (Throwable t) {
                    Kanto.LOG.error("Essence of Olde drop failed", t);
                }
            };
            if (server != null) server.execute(drop);
            else drop.run();
        });
        CobblemonEvents.ENTITY_SPAWN.subscribe(Priority.NORMAL, event -> {
            try {
                if (event.getEntity() instanceof PokemonEntity pokemon && pokemon.level().dimension() == Kanto.KANTO) onlyGen1(pokemon);
            } catch (Throwable t) {
                Kanto.LOG.error("Kanto spawn check failed", t);
            }
        });
        LifecycleEvent.SERVER_BEFORE_START.register(KantoEvents::labInVillages);
    }

    static boolean gen1(Species species) {
        return species.getNationalPokedexNumber() >= 1 && species.getNationalPokedexNumber() <= 151;
    }

    private static void essence(BattleFaintedEvent event) {
        BattlePokemon killed = event.getKilled();
        if (!gen1(killed.getOriginalPokemon().getSpecies())) return;
        for (BattleActor actor : event.getBattle().getActors()) {
            if (!(actor instanceof PlayerBattleActor player) || actor.getSide() == killed.getActor().getSide()) continue;
            ServerPlayer entity = player.getEntity();
            if (entity == null || entity.getRandom().nextDouble() >= ESSENCE_CHANCE) continue;
            ItemStack stack = new ItemStack(Kanto.ESSENCE.get());
            PokemonEntity at = killed.getEntity();
            if (at != null && at.level() == entity.level()) {
                ItemEntity drop = new ItemEntity(at.level(), at.getX(), at.getY() + 0.5, at.getZ(), stack);
                drop.setDefaultPickUpDelay();
                at.level().addFreshEntity(drop);
            } else if (!entity.getInventory().add(stack)) {
                entity.drop(stack, false);
            }
            entity.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".essence.dropped",
                    killed.getOriginalPokemon().getSpecies().getTranslatedName()), true);
        }
    }

    /**
     * Only Gen 1 Pokémon live in Kanto: any other species about to spawn there becomes a Gen 1 Pokémon (not legendary
     * or mythical) sharing its primary type, at the same level, so Kanto stays as lively as the overworld.
     */
    private static void onlyGen1(PokemonEntity entity) {
        Pokemon pokemon = entity.getPokemon();
        if (gen1(pokemon.getSpecies())) return;
        List<Species> same = new ArrayList<>(), any = new ArrayList<>();
        for (Species s : PokemonSpecies.getImplemented()) {
            if (!gen1(s) || s.getLabels().contains("legendary") || s.getLabels().contains("mythical")) continue;
            any.add(s);
            if (s.getPrimaryType() == pokemon.getSpecies().getPrimaryType()) same.add(s);
        }
        List<Species> pool = same.isEmpty() ? any : same;
        if (pool.isEmpty()) return;
        Species pick = pool.get(RANDOM.nextInt(pool.size()));
        Pokemon replacement = PokemonProperties.Companion.parse(pick.getResourceIdentifier().getPath() + " level=" + pokemon.getLevel()).create();
        entity.setPokemon(replacement);
    }

    /** The lab joins every village's houses (a rare pick), before the world generates. */
    private static void labInVillages(MinecraftServer server) {
        try {
            Registry<StructureTemplatePool> pools = server.registryAccess().registryOrThrow(Registries.TEMPLATE_POOL);
            for (String village : VILLAGES) {
                StructureTemplatePool pool = pools.get(ResourceLocation.withDefaultNamespace("village/" + village + "/houses"));
                if (pool == null) continue;
                StructurePoolElement lab = StructurePoolElement.single(Kanto.MOD_ID + ":village/gen1_lab")
                        .apply(StructureTemplatePool.Projection.RIGID);
                StructureTemplatePoolAccessor access = (StructureTemplatePoolAccessor) pool;
                for (int i = 0; i < LAB_WEIGHT; i++) access.cobbleeffortKanto$templates().add(lab);
                List<Pair<StructurePoolElement, Integer>> raw = new ArrayList<>(access.cobbleeffortKanto$rawTemplates());
                raw.add(Pair.of(lab, LAB_WEIGHT));
                access.cobbleeffortKanto$setRawTemplates(raw);
            }
        } catch (Throwable t) {
            Kanto.LOG.error("Couldn't add the lab to villages", t);
        }
    }
}
