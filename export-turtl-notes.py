import base64
import json
import os

def findboard(id):
    for board in data['boards']:
        if id == board['id']:
            return board['title']
    return ''

def clean(text):
    return "".join(c if c.isalnum() else " " for c in text)


f = open('turtl-backup.json', encoding='utf-8')
data = json.load(f)

if not os.path.isdir('turtl'):
    os.mkdir('turtl')

for folder in data['boards']:
    path = os.path.join('turtl', folder['title'])
    if not os.path.isdir(path):
        os.mkdir(path)

untitledcounter = 1

for note in data['notes']:

    type = note['type']
    title = note['title']
    if title == '':
        title = 'untitled' + str(untitledcounter)
        untitledcounter += 1

    print(title)

    if type == 'text':
        filename = clean(title) + '.md'
        with open(os.path.join('turtl', findboard(note['board_id']), filename), 'wb') as n:
            n.write(note['text'].encode('utf-8'))
            n.close()

    if type == 'image' or type == 'file':
        file = note['file']
        filename = file['name']
        for fileref in data['files']:
            if fileref['id'] == note['id']:
                b64 = fileref['data']
                with open(os.path.join('turtl', findboard(note['board_id']), filename), 'wb') as n:
                    n.write(base64.decodebytes(b64.encode('utf-8')))
                    n.close()

    if type == 'link':
        url = note['url']
        text = url + '\r\n' + note['text']
        filename = clean(title) + '.md'
        with open(os.path.join('turtl', findboard(note['board_id']), filename), 'wb') as n:
            n.write(text.encode('utf-8'))
            n.close()

f.close()