import json
from collections import defaultdict

d_openings = open("../tsv/d.tsv", "r")
qg = open("../tsv/filteredQG.tsv", "w")
jsonOut = open("../hierarchyQG.json", "w")

variations = {}
for line in d_openings:
    firstWord = line.split(" ")[0]
    if firstWord == "Slav" or firstWord == "Semi-Slav":
        line = "Queen's Gambit Declined: " + line
    if "Queen's Gambit" in line:
        # invariant: ECO + U+0009 + name + U+0009 + AN
        separated = line.split("	")
        variations[separated[1]] = separated[2]
    
for entry in variations:
    qg.write(entry + " " + variations[entry])

hierarchy = {}
# transfer to dictionary
for name in variations.keys():
    path = name.replace(': ', ', ')
    path = path.replace(' Declined', ', Declined')
    path = path.replace(' Accepted', ', Accepted').split(', ')

    current = hierarchy
    for sub in path:
        if sub not in current:
            current[sub] = {}
        current = current[sub]

# format json according to d3 tidy tree
def reformat(hierarchy):
    ans = []
    
    for entry in hierarchy.keys():
        res = defaultdict(list)
        res["name"] = entry
        children = hierarchy[entry]
        if len(children) != 0:
            res["children"] = reformat(children)
        ans.append(res)
    
    return ans

jsonOut.write(json.dumps(reformat(hierarchy)[0], indent=2, separators=(',', ': ')))