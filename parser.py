from sys import argv
from urllib2 import urlopen
import json
from unidecode import unidecode
from models import *

filename = argv[1]

f = open(filename)

url_query = 'http://en.wikipedia.org/w/api.php?action=query&titles={0}&prop=imageinfo&iiprop=url&format=json&continue'
attribution_query = 'http://en.wikipedia.org/w/api.php?action=query&titles={0}&prop=imageinfo&iiprop=extmetadata&format=json&continue'

image_path = 'app/images/asanas/'
s = create_session()

for line in f:
    fields = line.split('|')

    name = fields[1].strip()
    english = fields[3].strip()
    image_name = fields[4].strip()

    # Sure.
    name = name.decode('utf8')
    name = unidecode(name).encode('ascii')
    name = name.decode('ascii')
    name = unidecode(name).encode('utf8')

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

        try:
            image_url = response['query']['pages']['-1']['imageinfo'][0]['url']

            description_url = response['query']['pages']['-1']['imageinfo'][0]['descriptionurl']
            author = attribution['query']['pages']['-1']['imageinfo'][0]['extmetadata']['Artist']['value']
            license = attribution['query']['pages']['-1']['imageinfo'][0]['extmetadata']['LicenseUrl']['value']

            image = urlopen(image_url)
            image_name = name.replace(' ', '')
            file_extenstion = image_url.split('.')[-1]

            full_image_path = image_path + image_name + '.' + file_extenstion
            f = open(full_image_path, 'wb')
            f.write(image.read())
            f.close()

            image_url_path = full_image_path.replace('app/', '')

            p = Pose(
                name = name,
                simplename = english,
            )

            s.add(p)

            pi = PoseImage(
                url = image_url_path,
                author = author,
                license = license,
                further_attribution = description_url,
                pose = p,
            )

            s.add(pi)

        except KeyError:
            #dunno what to do here...
            print "BAD KEY"

        print image_url
        print author
        print license

s.commit()

