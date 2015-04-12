#!/usr/bin/python
from libqtile.command import Client
from dmenu import dmenu
from pprint import pprint
c = Client()
name=[]
win={}
for i in c.windows():
    if i['name'] <> '<no name>':
        id=str.lower("%s - %s"% (c.window[i['id']].inspect()['wm_class'][1], i['name']))
        name.append( id )
        win[ id ] = i['id']
choice = dmenu(name, lines=10, bottom=True).rstrip('\n')
pprint(c.window[win[choice]])
c.window[ win[ choice ]].group.toscreen()
c.window[ win[ choice ]].bring_to_front()
c.window[ win[ choice ]].disable_floating()


