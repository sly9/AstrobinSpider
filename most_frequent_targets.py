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
    
counts = Counter(subjects)
print('aaa')
#print(counts)
#most_common_targets = list(map(lambda x: x[0], x.most_common(4000)))
most_common_targets = {k: v for k, v in counts.items() if not k.startswith('The star')}

#most_common_targets = filter(lambda x: not x.startswith('The star'), counts)

#print('length of most common targets: ',len(most_common_targets))
#print('most_common_targets: ', most_common_targets)

# key is pyongc id, value is (pyongc target)
deduped_targets = {}

failed_list = []
json_list = []
for name in most_common_targets:
    count = most_common_targets[name]
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
        #print('Parsing %s failed' % name)
        failed_list.append(name)

#print(deduped_targets)
#print(failed_list)


### then fill image ids into DSO ids, so that we can refer it back later.

target_dict = {}

for dso in json_list:
    target_dict[dso['id']] = dso

#print(len(target_dict.keys()))
#print(target_dict.keys())

for image_filename in images:
    image = images[image_filename]
    if 'subjects' in image and len(image['subjects'])>0:
        for s in image['subjects']:
            dso = pyongc.get(s)
            #try:
            if dso:
                real_dso = target_dict[dso.id]
                if 'astrobin_filenames' not in real_dso:
                    real_dso['astrobin_filenames'] = []
                real_dso['astrobin_filenames'].append(image_filename)
            #except:
            #    print('Parsing this failed... ')
            #    print(pyongc.printDetails(dso))



with open('parsing_failed_targets.txt','w') as f:
    for t in failed_list:
        f.write('%s\n'%t)
#with open('parsed_subjects.json','w') as f:
#    json.dump(json_list, f)

with open('top_targets.json','w') as f:
    json.dump(target_dict, f)
