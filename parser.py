from sys import argv
from urllib2 import urlopen
import json
from unidecode import unidecode

filename = argv[1]

f = open(filename)

url_query = 'http://en.wikipedia.org/w/api.php?action=query&titles={0}&prop=imageinfo&iiprop=url&format=json&continue'
attribution_query = 'http://en.wikipedia.org/w/api.php?action=query&titles={0}&prop=imageinfo&iiprop=extmetadata&format=json&continue'

for line in f:
    fields = line.split('|')

    name = fields[1].strip()
    english = fields[3].strip()
    image_name = fields[4].strip()

    name = name.decode('utf8')
    name = unidecode(name).encode('ascii')

    print name, english, image_name

    if image_name != '':
        image_request_url = url_query.format(image_name.replace(' ', '%20'))
        attribution_request_url = attribution_query.format(image_name.replace(' ', '%20'))
        print image_request_url
        print attribution_request_url

        file_url = urlopen(image_request_url)
        image_request_url = urlopen(attribution_request_url)

        response = json.loads(file_url.read())
        attribution = json.loads(image_request_url.read())

        image_url = response['query']['pages']['-1']['imageinfo'][0]['url']
        author = attribution['query']['pages']['-1']['imageinfo'][0]['extmetadata']['Artist']['value']
        license = attribution['query']['pages']['-1']['imageinfo'][0]['extmetadata']['LicenseUrl']['value']

        print image_url
        print author
        print license


