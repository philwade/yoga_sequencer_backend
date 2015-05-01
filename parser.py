from sys import argv

filename = argv[1]

f = open(filename)

url_query = 'http://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=imageinfo&iiprop=url&format=json&continue'
attribution_query = 'http://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=imageinfo&iiprop=extmetadata&format=json&continue'

for line in f:
    fields = line.split('|')

    name = fields[1]
    english = fields[3]
    image_name = fields[4]

    print name, english, image_name
