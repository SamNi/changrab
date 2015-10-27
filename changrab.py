import os
from os import path
import sys
import json
import re
import time as t
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse

fourch_url_pat = re.compile(r'(https://|http://)?boards.4chan.org/(\w+)/thread/(\d+)')

def parse_4ch_url(url):
    ret = fourch_url_pat.match(url).groups()
    return ret

def _grab_thread_json(board, thread_id):
    path = r'http://a.4cdn.org/%s/thread/%s.json' % (board, thread_id)
    json_response = json.loads( urlopen(path).readall().decode() )
    return json_response


def get_thread_image_paths(url):
    _, board, thread_id = parse_4ch_url(url)
    #path = r'http://a.4cdn.org/%s/thread/%s.json' % (board, thread_id)
    #json_response = json.loads( urlopen(path).readall().decode() )
    response = _grab_thread_json(board, thread_id) 
    posts = response['posts']
    image_paths = []
    for (fname, fext) in [ (p['tim'], p['ext']) for p in posts if 'filename' in p]:
        filepath = r'http://i.4cdn.org/%s/%s%s' % (board, fname, fext)
        image_paths.append(filepath)
    return board, thread_id, image_paths

def grab_url(url):
    board, thread_id, image_paths = get_thread_image_paths(url)
    filecount = 0

    before_t = t.clock()
    for imgpath in image_paths:
        localfname = path.basename(urlparse(imgpath)[2])
        localpath = path.join(os.path.curdir, board, thread_id, localfname)
        os.makedirs(path.dirname(localpath), exist_ok=True)
        sys.stdout.write(imgpath + '\t\t')
        urlretrieve(imgpath, localpath)
        sys.stdout.write('successful\n')
        filecount += 1
    after_t = t.clock()

    tdelta = (after_t - before_t)
    print("Scraped %d image(s) in %f seconds (%f/second)" % (filecount, tdelta, filecount/tdelta))
    sys.stdout.flush()

def main():
    [grab_url(url) for url in sys.argv[1:]]

if __name__ == '__main__':
    sys.exit(main())