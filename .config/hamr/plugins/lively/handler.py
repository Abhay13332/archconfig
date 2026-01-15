#!/usr/bin/env python3
import json
import os
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    step = input_data.get("step", "initial")
    query = input_data.get("query", "").strip()
    
    if step == "initial":
        # Start by asking for the file path
        print(json.dumps({
            "type": "prompt",
            "prompt": {"text": "Enter file path for lively..."},
            "inputMode": "submit"
        }))
        return

    if step == "search":
        if not query:
            # Re-show prompt if query is empty
            print(json.dumps({
                "type": "prompt",
                "prompt": {"text": "Enter file path for lively..."},
                "inputMode": "submit"
            }))
            return
        
        # Expand user path (e.g. ~/path/to/vid.mp4)
        path = os.path.expanduser(query)
        
        # We can check if file exists, but let's just attempt to run if it's not empty
        # or provide feedback if it doesn't exist.
        if not os.path.exists(path):
            print(json.dumps({
                "type": "error",
                "message": f"File not found: {path}"
            }))
            return

        # Execute the lively command
        print(json.dumps({
            "type": "execute",
            "execute": {
                "command": ["lively", path],
                "name": f"Lively: {os.path.basename(path)}",
                "icon": "wallpaper",
                "close": True
            }
        }))
        return

    if step == "action":
        # Handle selection if we were displaying results
        pass

if __name__ == "__main__":
    main()
