# coding=utf-8

from urllib2 import urlopen, Request
import json
import re
import sys


class XmlyDownloader(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Safari/537.36'}

    def getIDs(self, url):
        resp = urlopen(Request(url, headers=self.headers))
        return re.search('sound_ids=\"(.*)\"', resp.read()).group(1).split(',')

    def getFileInfo(self, ID):
        url = 'http://www.ximalaya.com/tracks/{}.json'.format(ID)
        data = json.loads(urlopen(Request(url, headers=self.headers)).read())
        filename = data['title'] + data['play_path_64'][-4:]
        return filename, data['play_path_64']

    def download_file(self, fname, url):
        resp = urlopen(Request(url, headers=self.headers))
        total = int(resp.info().getheader('Content-Length').strip())
        chunk_size = 102400 # 100KB
        downloaded = 0

        with open(fname, 'wb') as local:
            while True:
                readback = resp.read(chunk_size)
                downloaded += len(readback)
                percent = int(100 * downloaded / total)
                sys.stdout.write('\r[{}{}]'.format('█' * percent, ' ' * (100-percent)))
                sys.stdout.flush()
                if not readback:
                    break
                else:
                    local.write(readback)

        sys.stdout.write('\r{}\r'.format(' '*102)
        sys.stdout.flush()

    def download_album(self, album_url):
        for ID in self.getIDs(album_url):
            file_name, file_url = self.getFileInfo(ID)
            print file_name, file_url
            self.download_file(file_name, file_url)

if __name__ == '__main__':
    album_url = 'http://www.ximalaya.com/7712455/album/4474664'
    xmly = XmlyDownloader()
    xmly.download_album(album_url)
