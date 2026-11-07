// CobbleEffort is a content-only Cobblemon addon: it contains no Java/Kotlin code,
// just data (cosmetic items, species features) and assets (resolvers, textures).
// One jar works on both Fabric and NeoForge, so we only need to package resources.
plugins {
    base
}

val modId = property("mod_id") as String
val modName = property("mod_name") as String
val modVersion = property("mod_version") as String
val minecraftVersion = property("minecraft_version") as String

version = modVersion
group = "io.github.cobbleeffort"

val expandProps = mapOf(
    "mod_id" to modId,
    "mod_name" to modName,
    "version" to modVersion,
    "minecraft_range_fabric" to property("minecraft_range_fabric"),
    "minecraft_range_neoforge" to property("minecraft_range_neoforge"),
    "cobblemon_range_fabric" to property("cobblemon_range_fabric"),
    "cobblemon_range_neoforge" to property("cobblemon_range_neoforge"),
)

val processResources by tasks.registering(Copy::class) {
    from("src/main/resources")
    into(layout.buildDirectory.dir("resources"))
    inputs.properties(expandProps)
    filesMatching(listOf("fabric.mod.json", "META-INF/neoforge.mods.toml", "pack.mcmeta")) {
        expand(expandProps)
    }
}

val jar by tasks.registering(Jar::class) {
    group = "build"
    description = "Packages the mod jar (Fabric + NeoForge)."
    archiveBaseName.set(modId)
    archiveVersion.set("$modVersion+$minecraftVersion")
    // Intermediate output: the jar is shipped inside a zip (see distZip below).
    destinationDirectory.set(layout.buildDirectory.dir("tmp/jar"))
    from(processResources)
    from("LICENSE") { rename { "LICENSE_$modId" } }
    manifest {
        attributes(
            "Specification-Title" to modName,
            "Implementation-Title" to modName,
            "Implementation-Version" to modVersion,
        )
    }
}

// Every jar we produce is delivered compressed: build/libs/<name>.zip containing <name>.jar.
val distZip by tasks.registering(Zip::class) {
    group = "build"
    description = "Wraps the mod jar in a zip."
    archiveFileName.set(jar.flatMap { it.archiveFileName }.map { it.removeSuffix(".jar") + ".zip" })
    destinationDirectory.set(layout.buildDirectory.dir("libs"))
    from(jar)
}

val validateData by tasks.registering {
    group = "verification"
    description = "Checks that every JSON file parses and every texture a resolver references exists."
    val resDir = file("src/main/resources")
    inputs.dir(resDir)
    doLast {
        val slurper = groovy.json.JsonSlurper()
        var count = 0
        resDir.walkTopDown().filter { it.isFile && it.extension in setOf("json", "mcmeta") }.forEach {
            try { slurper.parse(it) } catch (e: Exception) { throw GradleException("Invalid JSON: ${it.relativeTo(resDir)}: ${e.message}") }
            count++
        }
        val resolvers = resDir.resolve("assets/$modId/bedrock/pokemon/resolvers")
        resolvers.walkTopDown().filter { it.isFile && it.extension == "json" }.forEach { f ->
            @Suppress("UNCHECKED_CAST")
            val json = slurper.parse(f) as Map<String, Any?>
            (json["variations"] as List<Map<String, Any?>>).forEach { v ->
                val tex = v["texture"] as? String ?: return@forEach
                val (ns, path) = tex.split(":", limit = 2)
                if (ns == modId && !resDir.resolve("assets/$ns/$path").isFile) {
                    throw GradleException("${f.name} references missing texture $tex")
                }
            }
        }
        println("validateData: $count JSON files OK, resolver textures present.")
    }
}

tasks.named("check") { dependsOn(validateData) }
tasks.named("assemble") { dependsOn(distZip) }
