import json
import pprint

with open('BLACKLIST.json') as file:
    blacklist = json.load(file)


for title in blacklist:
    print(title)
    for name in blacklist[title]:
        print('    ' + name)
        for tag in blacklist[title][name]:
            print('        ' + tag + ' = ' + str(blacklist[title][name][tag]))
            
