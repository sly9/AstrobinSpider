#!/bin/env python3

import json
import requests
import time
from os import path


top_nomiation_list_url = 'https://www.astrobin.com/api/v1/toppicknomination/?api_key=aa2a70c0dd02cffeaa4e475eee1f4cbf6ef37cb6&api_secret=939d21c3c67dc7b4abd9ec69bc873f71bdb00242&limit=500&offset=%d&format=json'

offset = 0

def crawl(url):
    print('Going to crawl %s' % url)
    top_nomiation_list = requests.get(url).json()
    
    image_meta_list = top_nomiation_list['objects']
    for image_meta in image_meta_list:
        try:
            hash = image_meta['image'].split('/')[-1]
            craw_image(image_meta)
        except:
            print('crawling %s failed' % hash)
    print('Crawling %s finished' % url)
    if 'meta' in top_nomiation_list and 'next' in top_nomiation_list['meta']:
        return 'https://www.astrobin.com'+top_nomiation_list['meta']['next']
    return None

def craw_image(image_meta):
    hash = image_meta['image'].split('/')[-1]
    if path.exists('image_data/%s.json' % hash):
        print('No need to download %s again, we got it already' % hash)
        return
    time.sleep(10)
    print('Downloading meta for hash: %s' % hash)
    details = requests.get('https://www.astrobin.com/api/v1/image/%s?api_key=aa2a70c0dd02cffeaa4e475eee1f4cbf6ef37cb6&api_secret=939d21c3c67dc7b4abd9ec69bc873f71bdb00242&format=json' % hash).json()
    with open('image_data/%s.json' % hash, 'w', encoding='utf-8') as f:
        json.dump(details, f, ensure_ascii=False, indent=4)


    
if __name__ == '__main__':
    url = top_nomiation_list_url % offset
    while True:
        url = crawl(url)
        if not url:
            print('Nothing more to crawl...')
            exit()
    