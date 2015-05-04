from sys import argv
from urllib2 import urlopen
import json

filename = argv[1]

f = open(filename)

url_query = 'http://en.wikipedia.org/w/api.php?action=query&titles={0}&prop=imageinfo&iiprop=url&format=json&continue'
attribution_query = 'http://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=imageinfo&iiprop=extmetadata&format=json&continue'

for line in f:
    fields = line.split('|')

    name = fields[1].strip()
    english = fields[3].strip()
    image_name = fields[4].strip()

    print name, english, image_name

    if image_name != '':
        request_url = url_query.format(image_name.replace(' ', '%20'))
        print request_url

        file_url = urlopen(request_url)

        response = json.loads(file_url.read())

        image_url = response['query']['pages']['-1']['imageinfo'][0]['url']

        print image_url


