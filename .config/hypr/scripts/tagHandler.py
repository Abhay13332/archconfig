#!/usr/bin/env python3
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
alltagarray=["nobar","noborder"]

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
        execute(f'hyprctl dispatch tagwindow +{key}')
    else:
        execute(f'hyprctl dispatch tagwindow -- -{key}')



        