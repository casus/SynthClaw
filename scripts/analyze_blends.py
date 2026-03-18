import bpy
import json
import sys

def extract_features():
    scene = bpy.context.scene
    
    # Render Engine
    engine = scene.render.engine
    
    # Compute samples and bounces based on engine
    if engine == 'CYCLES':
        samples = scene.cycles.samples
        bounces = scene.cycles.max_bounces
        diffuse_bounces = scene.cycles.diffuse_bounces
        glossy_bounces = scene.cycles.glossy_bounces
        transmission_bounces = scene.cycles.transmission_bounces
    elif engine in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
        samples = scene.eevee.taa_render_samples
        bounces = "N/A (EEVEE)"
        diffuse_bounces = "N/A"
        glossy_bounces = "N/A"
        transmission_bounces = "N/A"
    else:
        samples = "Unknown"
        bounces = "Unknown"
        diffuse_bounces = "Unknown"
        glossy_bounces = "Unknown"
        transmission_bounces = "Unknown"

    # Resolution settings
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    res_perc = scene.render.resolution_percentage
    
    # Extract exposed parameter nodes (which affect procedural textures)
    value_nodes = {}
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        for node in mat.node_tree.nodes:
            if node.type == 'VALUE' and node.name:
                value_nodes[f"{mat.name}::{node.name}"] = node.outputs[0].default_value

    data = {
        "render_engine": engine,
        "resolution": f"{res_x}x{res_y} @ {res_perc}%",
        "samples": samples,
        "light_bounces": {
            "max": bounces,
            "diffuse": diffuse_bounces,
            "glossy": glossy_bounces,
            "transmission": transmission_bounces
        },
        "value_nodes": value_nodes
    }

    # Print out pure JSON between recognizable markers
    print("---ANALYSIS_START---")
    print(json.dumps(data, indent=2))
    print("---ANALYSIS_END---")

if __name__ == "__main__":
    extract_features()
