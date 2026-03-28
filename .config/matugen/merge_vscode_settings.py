#!/usr/bin/env python3
import json
import sys
import os
import re

def strip_jsonc(text):
    # Strip comments
    text = re.sub(r'//.*?\n', '\n', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # Strip trailing commas
    text = re.sub(r',\s*([\]}])', r'\1', text)
    return text

def merge_settings(main_path, override_path):
    with open(main_path, 'r') as f:
        main_content = strip_jsonc(f.read())
        try:
            main_data = json.loads(main_content)
        except json.JSONDecodeError as e:
            print(f"Error parsing {main_path}: {e}")
            return

    with open(override_path, 'r') as f:
        override_content = strip_jsonc(f.read())
        try:
            override_data = json.loads(override_content)
        except json.JSONDecodeError as e:
            print(f"Error parsing {override_path}: {e}")
            return

    # Deep merge
    main_data.update(override_data)
    
    # Specifically for VS Code, merge the subkeys if they exist
    if "workbench.colorCustomizations" in override_data and "workbench.colorCustomizations" in main_data:
        main_data["workbench.colorCustomizations"].update(override_data["workbench.colorCustomizations"])
    
    if "editor.tokenColorCustomizations" in override_data and "editor.tokenColorCustomizations" in main_data:
        # Merge textMateRules if they exist
        if "textMateRules" in override_data["editor.tokenColorCustomizations"] and "textMateRules" in main_data["editor.tokenColorCustomizations"]:
            # This is complex, usually we just want to replace the rules with the new ones
            main_data["editor.tokenColorCustomizations"]["textMateRules"] = override_data["editor.tokenColorCustomizations"]["textMateRules"]
        else:
            main_data["editor.tokenColorCustomizations"].update(override_data["editor.tokenColorCustomizations"])

    with open(main_path, 'w') as f:
        json.dump(main_data, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: merge_settings.py <main_settings.json> <override_settings.json>")
        sys.exit(1)
    merge_settings(sys.argv[1], sys.argv[2])
