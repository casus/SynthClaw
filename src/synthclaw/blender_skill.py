import subprocess
import os

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(MODULE_DIR, "..", "..", "scripts"))
SCRIPT_PATH = os.path.join(SCRIPTS_DIR, "agent_bridge.py")

def render_procedural_scene(blend_file: str, output_path: str, parameters: dict):
    """
    OpenClaw Skill: Executes Blender in background mode to render a procedural scene.
    
    :param blend_file: Absolute path to the .blend file.
    :param output_path: Where to save the resulting image (e.g., /tmp/render.png).
    :param parameters: A dictionary of node names and float values (e.g., {"Scale": 5.0}).
    """
    # 1. Format parameters for the Blender script (key=value)
    param_args = [f"{k}={v}" for k, v in parameters.items()]
    
    # 2. Build the CLI command
    # -b: background, -P: run python script, -o: output, -f 1: render frame 1
    command = [
        "blender", 
        "-b", blend_file, 
        "-P", SCRIPT_PATH, 
        "-o", output_path, 
        "-f", "1", 
        "--"
    ] + param_args

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return {"status": "success", "output": output_path, "log": result.stdout[-500:]}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}

# Example usage for OpenClaw registration:
# {
#   "name": "render_procedural_scene",
#   "description": "Adjusts procedural nodes and renders a frame in Blender 4.0+",
#   "parameters": { ... }
# }