package io.github.cobbleeffort.distortion.mixin;

import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.pokemon.FormData;
import com.cobblemon.mod.common.pokemon.Species;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Mutable;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.ArrayList;
import java.util.List;

/**
 * Mega Showdown's Rotom Catalogue cycles a fixed list of appliances (heat, fan, mow, frost, wash, none). CobbleEffort
 * adds more Rotom forms on the same `appliance` feature (data/cobbleeffort/species_additions/rotom_forms.json), so the
 * first time the Catalogue is used, every other "<x>-appliance" form Rotom has joins the cycle before "none".
 */
@Pseudo
@Mixin(targets = "com.github.yajatkaul.mega_showdown.item.custom.form_change.RotomCatalogue", remap = false)
public abstract class RotomCatalogueMixin {
    @Shadow @Final @Mutable private List<String> form_apply_order;
    @Shadow @Final @Mutable private List<String> form_aspect_apply_order;
    @Shadow @Final @Mutable private List<String> effects_apply_order;
    @Unique private boolean cobbleeffort$extended;

    @Inject(method = "applyToPokemon", at = @At("HEAD"), remap = false)
    private void cobbleeffort$moreForms(CallbackInfoReturnable<?> cir) {
        if (cobbleeffort$extended) return;
        try {
            Species rotom = PokemonSpecies.INSTANCE.getByName("rotom");
            if (rotom == null) return;
            List<String> forms = new ArrayList<>(form_apply_order);
            List<String> props = new ArrayList<>(form_aspect_apply_order);
            List<String> effects = new ArrayList<>(effects_apply_order);
            int at = forms.indexOf("none-appliance");
            if (at < 0) at = forms.size();
            String effect = effects.isEmpty() ? "mega_showdown:rotom_effect" : effects.get(effects.size() - 1);
            for (FormData f : rotom.getForms()) {
                for (String a : f.getAspects()) {
                    if (a.endsWith("-appliance") && !forms.contains(a)) {
                        forms.add(at, a);
                        props.add(at, "appliance=" + a.substring(0, a.length() - "-appliance".length()));
                        effects.add(at, effect);
                        at++;
                    }
                }
            }
            form_apply_order = forms;
            form_aspect_apply_order = props;
            effects_apply_order = effects;
            cobbleeffort$extended = true;
        } catch (Throwable ignored) {
            // never break the Catalogue: it keeps its own cycle
        }
    }
}
