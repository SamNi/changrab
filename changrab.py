import os
from os import path
import sys
import json
import re
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse


def parse_4ch_url(url):
    pat = re.compile(r'(https://|http://)?boards.4chan.org/(\w+)/thread/(\d+)')
    ret = pat.match(url).groups()
    return ret

def get_thread_image_paths(url):
    _, board, thread_id = parse_4ch_url(url)
    path = r'http://a.4cdn.org/%s/thread/%s.json' % (board, thread_id)
    json_response = json.loads( urlopen(path).readall().decode() )
    posts = json_response['posts']
    image_paths = set([])
    for fname in [ p['tim'] for p in posts if 'filename' in p]:
        filepath = r'http://i.4cdn.org/%s/%s.jpg' % (board, fname)
        image_paths.add(filepath)
    return board, thread_id, image_paths

def main():
    inp_url = sys.argv[1]
    board, thread_id, image_paths = get_thread_image_paths(inp_url)
    filecount = 0
    for imgpath in image_paths:
        try:
            localfname = path.basename(urlparse(imgpath)[2])
            localpath = path.join(os.path.curdir, board, thread_id, localfname)
            os.makedirs(path.dirname(localpath), exist_ok=True)
            sys.stdout.write(imgpath + '\t\t')
            urlretrieve(imgpath, localpath)
            sys.stdout.write('done!\n')
            filecount += 1
        except:
    print("Scraped %d image(s)" % filecount)

if __name__ == '__main__':
    sys.exit(main())