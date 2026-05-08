#!/usr/bin/env python3
import json
import os
from pathlib import Path
import subprocess
import sys
def execute(command):
    return subprocess.run(['bash', '-c',command],capture_output=True,text=True)
def arg(i:int):
    return sys.argv[i]

def getshadernames():
    path=Path.home()/".config/hypr/shaders"
    
    files = list(os.listdir(path))
    shadername=[f.removesuffix(".glsl") for f in files]
    
    return shadername
    
def shader_file_path():
        xdg_cache = os.environ.get("XDG_CACHE_HOME")
        if xdg_cache:
            cache_base_dir = Path(xdg_cache)/"shader"
        else:
            cache_base_dir = Path.home() / ".cache"/"shader"
        if  not cache_base_dir.exists():
            print("creating",cache_base_dir)
            os.makedirs(cache_base_dir)
        return cache_base_dir/"shader.current"
def writer(path):
      def writefn(text):
        with open(path, 'w', encoding='utf-8') as file:
          file.write(text)
      return writefn
def main():
    shaders=(getshadernames())
    file_loc=shader_file_path()
    write=writer(file_loc)
    
    print(shaders)
    if len(sys.argv) > 1 and arg(1) =='toggle':
        if  execute("hyprshade current").stdout:
            execute("hyprshade toggle")
            execute(f"notify-send \"disabling shader \" \" disable using hyprshade\"")
            write("off")
        else:
            execute("hyprshade auto")
            execute(f"notify-send \"setting shader {execute("hyprshade current").stdout}\" \"setting shader using hyprshade\"")
            write("color_fix")

    elif len(sys.argv) > 1 and arg(1) =='next':
        
        idx=(shaders.index(execute("hyprshade current").stdout.strip()))+1
        idx=(idx)%len(shaders)
        execute(f"hyprshade on {shaders[idx]}")
        write(shaders[idx])
        execute(f"notify-send \"setting shader {shaders[idx]}\" \"setting shader using hyprshade\"")
    else :
        
        with open(file_loc, 'r', encoding='utf-8') as file:
            text_buffer = file.read()
            if(text_buffer!="off"):
                execute(f"hyprshade on {text_buffer}")
            

if __name__=="__main__":
    main()