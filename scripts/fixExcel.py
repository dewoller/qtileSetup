#!/usr/bin/python
from libqtile.command import Client
c = Client()
for i in c.windows():
    if (i['name'].startswith('Microsoft Excel -' )) :
        c.window[ i['id'] ].group.toscreen()
        c.window[ i['id'] ].bring_to_front()
        c.window[ i['id'] ].disable_floating()

