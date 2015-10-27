import os
from os import path
import sys
import json
import re
import time as t
import sqlite3 as sql
import logging as lg 

from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse

db_fname = 'changrab.db'

fourch_url_pat = re.compile(r'(https://|http://)?boards.4chan.org/(\w+)/thread/(\d+)')
lg.basicConfig(filename='changrab.log', level=lg.DEBUG)

def _init_db(fname = db_fname):
    if path.exists(path.join(os.curdir, fname)):
        lg.log(lg.INFO, "%s already exists" % fname)

def parse_4ch_url(url):
    return fourch_url_pat.match(url).groups()

def grab_thread_json(board, thread_id, protocol='http'):
    path = r'%s://a.4cdn.org/%s/thread/%s.json' % (protocol, board, thread_id)
    return json.loads( urlopen(path).readall().decode() )

def get_thread_image_paths(js_obj, board, thread_id):
    posts = js_obj['posts']
    image_paths = []
    for (fname, fext) in [ (p['tim'], p['ext']) for p in posts if 'filename' in p]:
        filepath = r'http://i.4cdn.org/%s/%s%s' % (board, fname, fext)
        image_paths.append(filepath)
    return image_paths

def grab_url(url):
    _, board, thread_id = parse_4ch_url(url)
    js_obj = grab_thread_json(board, thread_id)
    image_paths = get_thread_image_paths(js_obj, board, thread_id)

    # Archive raw json (may be useful later)
    arch_dir = path.join(os.curdir, board)
    arch_fname = '%s.json' % thread_id
    os.makedirs(path.join(os.curdir, board), exist_ok=True)
    json.dump(js_obj, open(path.join(arch_dir, arch_fname), "w"))

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