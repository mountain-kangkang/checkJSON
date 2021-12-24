import json

with open('0601_light_clear_smooth_06000051.json', 'r', encoding='utf-8') as jj:
    jf = json.loads(jj.read())

    for i in range(len(jf["categories"])):
        print(jf["categories"][i]["name"])