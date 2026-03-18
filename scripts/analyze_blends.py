import bpy
import json


def main():
    """
    Analyzes a Blender file and outputs available Value Nodes as JSON.
    """
    value_nodes = {}
    
    # Iterate through all materials
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        
        nodes = mat.node_tree.nodes
        for node in nodes:
            # Look for Value nodes that can be manipulated
            if node.type == 'VALUE':
                node_name = node.name
                current_value = node.outputs[0].default_value
                value_nodes[node_name] = {
                    "value": current_value,
                    "material": mat.name
                }
    
    # Also check for geometry nodes if present
    try:
        if bpy.data.node_groups:
            for group in bpy.data.node_groups:
                for node in group.nodes:
                    if node.type == 'VALUE':
                        node_name = node.name
                        current_value = node.outputs[0].default_value
                        value_nodes[f"{group.name}.{node_name}"] = {
                            "value": current_value,
                            "node_group": group.name
                        }
    except Exception as e:
        print(f"Note: Could not check geometry nodes: {e}")
    
    # Output as JSON for easy parsing
    print(json.dumps(value_nodes, indent=2))
    
    # Also print human-readable summary
    print(f"\n\nFound {len(value_nodes)} manipulatable Value Nodes:")
    for name, info in value_nodes.items():
        if "material" in info:
            print(f"  - {name} (material: {info['material']}) = {info['value']}")
        else:
            print(f"  - {name} (node group: {info['node_group']}) = {info['value']}")


if __name__ == "__main__":
    main()
