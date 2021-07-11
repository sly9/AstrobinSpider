#!/bin/env python3
import json
from collections import Counter

def load_images():
    with open('images.json') as f:
        images_json = json.load(f)

    subject_list = []

    for k in images_json:
        image = images_json[k]
        if 'subjects' in image and len(image['subjects'])>0:
            subject_list.extend(image['subjects'])    

    counts = Counter(subject_list)
    print(counts)

    print(counts.most_common(10))

def common_name_resolver(common_name):
    '''
    Parameter: 
        common_name, a string, like 'Heart nebula'
    Return:
        A canonical name in NGC / IC / SH / B catalog
    '''
    if not hasattr(common_name_resolver, 'names'):
        common_name_resolver.names = {}
        with open('database/names.dat.txt') as f:
            for line in f.readlines():
                name = line[:35].strip().upper()
                value = line[37:41].strip().upper()
                if value.startswith('I'):
                    value = 'IC ' + value[1:]
                else:
                    value = 'NGC ' + value
                if name not in common_name_resolver.names:
                    common_name_resolver.names[name] = value    
    standard_common_name = common_name.strip().upper()
    if standard_common_name in common_name_resolver.names:
        return common_name_resolver.names[standard_common_name]
    return None

if __name__ == '__main__':
    load_images()