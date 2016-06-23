#!/usr/bin/python
from libqtile.command import Client
from inspect import getmembers
from pprint import pprint
from var_dump import var_dump
c = Client()
for i in c.windows():
#    var_dump(i)
    if (i['name'].startswith('Microsoft Excel' )) :
        c.window[ i['id'] ].group.toscreen()
        c.window[ i['id'] ].bring_to_front()
        c.window[ i['id'] ].disable_floating()

