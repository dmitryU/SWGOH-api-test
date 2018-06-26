import requests
import lxml.html

GUILD_URL = 'https://swgoh.gg/g/34508/darklightcrew/zetas/';

response = requests.get(GUILD_URL)

#with open('zetas.html', 'w') as f:
#    f.write(response.text)
#with open('zetas.html', 'r') as f:
#    root = lxml.html.fromstring(f.read())

root = lxml.html.fromstring(response.text)
cells = root.cssselect('table tbody td:first-child')
names = [cell.attrib['data-sort-value'] for cell in cells]

print(''.join(name + '\n' for name in names))

#cells = root.cssselect('table tbody td')
#for cell in cells:
#  print("Cell: %s" % cell.text_content())

#with open('zetas.csv', 'w') as f:
#    f.write(''.join(name + '\n' for name in names))