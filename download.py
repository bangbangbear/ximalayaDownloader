# coding=utf-8

import urllib2
import json
import re

# album_url = 'http://www.ximalaya.com/7712455/album/6333174'
album_url = 'http://www.ximalaya.com/7712455/album/4474664'
headers = {'User-Agent': 'Safari/537.36'}
resp = urllib2.urlopen(urllib2.Request(album_url, headers=headers))
ids = re.search('sound_ids=\"(.*)\"', resp.read()).group(1).split(',')

for ind, f in enumerate(ids):
    url = 'http://www.ximalaya.com/tracks/{}.json'.format(f)
    resp = urllib2.urlopen(urllib2.Request(url, headers=headers))
    jsondata = resp.read()
    data = json.loads(jsondata)
    output = data['title'] + data['play_path_64'][-4:]
    print output, data['play_path_64']
    with open(output, 'wb') as local:
        local.write(urllib2.urlopen(data['play_path_64']).read())
