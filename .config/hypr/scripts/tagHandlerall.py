#!/usr/bin/env python3
import json
import subprocess

def tag_all_windows(tag_name,target:bool):
    
    result = subprocess.run(['hyprctl', '-j', 'clients'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error fetching clients")
        return

    clients = json.loads(result.stdout)
    addresses = [c['address'] for c in clients]
    batch_commands = [f" dispatch tagwindow {"+" if target else "-"}{tag_name} address:{addr}" for addr in addresses]
    print(batch_commands)
    full_command = " ; ".join(batch_commands)
    subprocess.run(['hyprctl', '--batch', full_command])
    print(f"Applied tag '{tag_name}' to {len(addresses)} windows.")



import json
import subprocess

def execute(command):
    return subprocess.run(['bash', '-c',command],capture_output=True,text=True)
result = execute('hyprctl -j activewindow | jq -r ".tags"')
print(result.stdout)
array=json.loads(result.stdout)
current_tagset={};
for i in array:
    current_tagset[i]=1 

maxm=pow(2,len(current_tagset))
print(maxm)
alltagarray=["nobar","noborder","noshadow"]
for i in range(0,len(alltagarray)):
    if alltagarray[i] not in current_tagset:
        current_tagset[alltagarray[i]]=0
 
for key in sorted(current_tagset):
    if current_tagset[key] == 1:
        current_tagset[key]=0   
    else:
        current_tagset[key]=1
        break;    
for key in current_tagset:
    if current_tagset[key] == 1:
        tag_all_windows(key,True)
    else:
        tag_all_windows(key,False)
 
