package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.CobblemonEntities;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.AABB;

/** Primary Village's guards: Elecmon (uncatchable, persistent) that keep watch round the cradles. */
final class Guards {
    static final String TAG = "cobbleeffort_digital_guard";
    static final int RADIUS = 24, MAX = 2;

    private Guards() {
    }

    static void ensure(ServerLevel level, BlockPos pos) {
        if (PokemonSpecies.INSTANCE.getByIdentifier(ResourceLocation.fromNamespaceAndPath("cobbleeffort", "elecmon")) == null) return;
        int have = level.getEntitiesOfClass(PokemonEntity.class, new AABB(pos).inflate(RADIUS), e -> e.getTags().contains(TAG)).size();
        if (have >= MAX || level.getNearestPlayer(pos.getX(), pos.getY(), pos.getZ(), 64, false) == null) return;
        Pokemon p = PokemonProperties.Companion.parse("cobbleeffort:elecmon level=18 uncatchable").create();
        PokemonEntity e = new PokemonEntity(level, p, CobblemonEntities.POKEMON);
        int x = pos.getX() + level.getRandom().nextInt(9) - 4, z = pos.getZ() + level.getRandom().nextInt(9) - 4;
        int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
        net.minecraft.world.entity.Mob mob = e;
        mob.moveTo(x + 0.5, y, z + 0.5, level.getRandom().nextFloat() * 360F, 0F);
        mob.setPersistenceRequired();
        mob.addTag(TAG);
        mob.setCustomName(Component.translatable(Digital.MOD_ID + ".guard.name").withStyle(ChatFormatting.YELLOW));
        level.addFreshEntity(mob);
    }
}
