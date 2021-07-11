#!/bin/env python3

from astropy.coordinates import SkyCoord
import pyongc
import json
from collections import Counter

with open('images.json') as f:
    images = json.load(f)

subjects = []

for i in images:
    image = images[i]
    if 'subjects' in image and len(image['subjects'])>0:
        subjects.extend(image['subjects'])
    
x = Counter(subjects)
#print(x)
#most_common_targets = list(map(lambda x: x[0], x.most_common(4000)))
most_common_targets = list(filter(lambda x: not x[0].startswith('The star'), x.most_common(4000)))

print(most_common_targets)

# key is pyongc id, value is (pyongc target)
deduped_targets = {}

failed_list = []
json_list = []
for t in most_common_targets:
    name = t[0]
    count = t[1]
    print('Solving %s with count %d...' % (name,count))
    if name == 'Other' or name == 'Comet':
        continue
    dso = pyongc.get(name)
    if dso:
        if dso.id in deduped_targets:
            print('%s is already seen before, skip it.' % (name)) 
        else:
            deduped_targets[dso.id] = dso.name
            json_obj = json.loads(dso.to_json())
            json_obj['count'] = count
            json_list.append(json_obj)
    else:
        print('Parsing %s failed' % name)
        failed_list.append(name)

print(deduped_targets)
#print(failed_list)

with open('parsing_failed_targets.txt','w') as f:
    for t in failed_list:
        f.write('%s\n'%t)
with open('parsed_subjects.json','w') as f:
    json.dump(json_list, f)