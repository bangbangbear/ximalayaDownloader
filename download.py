# coding=utf-8

from urllib2 import urlopen, Request
import json
import re


class XmlyDownloader(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Safari/537.36'}

    def getIDs(self, url):
        resp = urlopen(Request(url, headers=self.headers))
        return re.search('sound_ids=\"(.*)\"', resp.read()).group(1).split(',')

    def download_file(self, ID):
        url = 'http://www.ximalaya.com/tracks/{}.json'.format(ID)
        resp = urlopen(Request(url, headers=self.headers))
        data = json.loads(resp.read())
        output = data['title'] + data['play_path_64'][-4:]
        print output, data['play_path_64']
        with open(output, 'wb') as local:
            local.write(urlopen(data['play_path_64']).read())

    def download_album(self, album_url):
        for ID in self.getIDs(album_url):
            self.download_file(ID)


if __name__ == '__main__':
    album_url = 'http://www.ximalaya.com/7712455/album/4474664'
    xmly = XmlyDownloader()
    xmly.download_album(album_url)
