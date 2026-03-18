import bpy
import sys

def main():
    # Everything after "--" in the CLI is passed to sys.argv
    try:
        args = sys.argv[sys.argv.index("--") + 1:]
    except ValueError:
        print("No parameters provided via CLI.")
        return

    # Parse key=value pairs
    params = {}
    for a in args:
        if '=' in a:
            k, v = a.split('=')
            params[k] = float(v)

    # We iterate through all materials to find matching 'Value' nodes
    # This makes the agent "find" the controls automatically
    for mat in bpy.data.materials:
        if not mat.use_nodes: continue
        
        nodes = mat.node_tree.nodes
        for key, val in params.items():
            # In Blender 4.0+, we check the node's custom name
            if key in nodes and nodes[key].type == 'VALUE':
                nodes[key].outputs[0].default_value = val
                print(f"Agent updated Node '{key}' to {val}")

    # Ensure Cycles is used for high-quality procedural output
    bpy.context.scene.render.engine = 'CYCLES'
    # Optional: If running on a server without GPU, uncomment below:
    # bpy.context.scene.cycles.device = 'CPU'

if __name__ == "__main__":
    main()