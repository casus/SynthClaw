import os
import bpy

def configure_compositor_outputs(scene, output_dir, frame_idx):
    """
    Finds all File Output nodes in Compositor and dynamically routes
    their exports to structured subfolders.
    """
    configured_any = False
    if scene.use_nodes and scene.compositing_node_group:
        for node in scene.compositing_node_group.nodes:
            if node.type == 'OUTPUT_FILE':
                orig_dir = getattr(node, "directory", getattr(node, "base_path", ""))
                norm_orig = os.path.normpath(orig_dir)
                norm_output = os.path.normpath(output_dir)
                
                if norm_orig.startswith(norm_output):
                    subfolder = os.path.relpath(norm_orig, norm_output)
                else:
                    try:
                        blend_dir = bpy.path.abspath("//")
                        abs_orig_dir = bpy.path.abspath(orig_dir)
                        rel_path = os.path.relpath(abs_orig_dir, blend_dir)
                        
                        # If the path goes through an output directory, strip the parent/output prefix
                        if "output/" in rel_path:
                            rel_path = rel_path.split("output/", 1)[1]
                        elif "output\\" in rel_path:
                            rel_path = rel_path.split("output\\", 1)[1]
                        elif rel_path.startswith(".."):
                            # Fallback: strip leading dot-dots
                            parts = rel_path.split(os.sep)
                            rel_path = os.path.sep.join([p for p in parts if p != ".."])
                    except Exception:
                        rel_path = "."
                    
                    if rel_path and rel_path != ".":
                        subfolder = rel_path.rstrip("/\\")
                    else:
                        subfolder = node.name.replace(" ", "_").lower()
                
                if hasattr(node, "directory"):
                    node.directory = os.path.join(output_dir, subfolder)
                else:
                    node.base_path = os.path.join(output_dir, subfolder)
                
                # Force PNG output format so masks are saved as PNG (preventing deletion by TIFF cleanup)
                node.format.file_format = 'PNG'
                
                if hasattr(node, "file_output_items"):
                    for item in node.file_output_items:
                        item.name = f"{frame_idx}"
                        if hasattr(item, "format"):
                            item.format.file_format = 'PNG'
                else:
                    for slot in node.file_slots:
                        slot.path = f"{frame_idx}"
                        if hasattr(slot, "format"):
                            slot.format.file_format = 'PNG'
                            
                configured_any = True
                dir_val = node.directory if hasattr(node, "directory") else node.base_path
                print(f"[SynthClaw] Compositor: Routed node '{node.name}' to base path '{dir_val}' path '{frame_idx}' (PNG)")
    return configured_any
