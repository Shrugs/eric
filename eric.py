import urllib
import requests
import re
from PIL import Image
import sys

BASE = 'http://www.emotioneric.com'
LOCATION = './pics/'

REGEX = re.compile('<img width=.+src="/(?P<word>.+).jpg">')

IMAGE_SIZE = 128, 128


def download():
    with open('eric.csv') as f:
        with open('keys.csv', 'w') as csv:
            for line in f:
                line = line.replace('\n', '')
                r = requests.get(BASE + line, headers={
                    'User-Agent': 'My User Agent 1.0',
                }).text

                m = REGEX.search(r)
                if m:
                    k = m.group('word')

                    csv.write(k + '\n')
                    urllib.urlretrieve(BASE + '/' + k + '.jpg', LOCATION + k + '.jpg')


def convert():
    with open('keys.csv') as f:
        for k in f:
            k = k.replace('\n', '')
            infile = './pics/' + k + '.jpg'
            outfile = './emoji/' + k + '.jpg'
            try:
                im = Image.open(infile)
                im.thumbnail(IMAGE_SIZE, Image.ANTIALIAS)
                background = Image.new('RGBA', IMAGE_SIZE, (0, 0, 0, 0))
                background.paste(im, ((IMAGE_SIZE[0] - im.size[0]) / 2, (IMAGE_SIZE[1] - im.size[1]) / 2))
                background.save(outfile, "JPEG")
            except IOError:
                print "cannot create emoji for '%s'" % infile


def upload():
    URL = 'https://hackny.slack.com/customize/emoji'
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'

    with open('keys.csv') as f:
        for k in f:
            k = k.replace('\n', '')

            infile = './emoji/' + k + '.jpg'

            files = {
                'add': '1',
                'crumb': 's-1433397666-59bd257454-test',
                'name': 'eric_' + k,
                'mode': 'data',
                'img': open(infile, 'rb')
            }

            r = requests.post(URL, files=files, headers={
                'User-Agent': USER_AGENT
            })
            print r.text
            break

if len(sys.argv) != 2:
    print "need command"
    exit()

command = sys.argv[1]

if command == 'download':
    download()
elif command == 'convert':
    convert()
elif command == 'upload':
    upload()
