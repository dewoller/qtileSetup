#!/usr/bin/python
from libqtile.command import Client
from dmenu import dmenu
from pprint import pprint
import unicodedata
import os
import re
bad = re.compile("^excel.exe - ")
good = re.compile(".*microsoft excel")

c = Client()
names=[]
win={}
for window in c.windows():
    if window['name'] <> '<no name>':
        id=unicodedata.normalize("NFKD", unicode.lower(unicode("%s - %s"% (c.window[window['id']].inspect()['wm_class'][1], window['name'])))).encode('ascii', 'ignore')
        if (bad.match( id ) and not good.match( id )):
            continue
        names.append( re.sub( r"'", "", id ))
        win[ id ] = window['id']

choice =  os.popen(  "echo '"+"\n".join(names)+ "'| /usr/bin/dmenu -b -l 10").read().rstrip("\n")
#choice = dmenu(names, lines=10, bottom=True).rstrip('\n')
pprint(c.window[win[choice]])
c.window[ win[ choice ]].group.toscreen()
c.window[ win[ choice ]].bring_to_front()
c.window[ win[ choice ]].disable_floating()



