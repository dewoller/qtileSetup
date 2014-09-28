#!/usr/bin/python

import sys
from libqtile.command import Client
c = Client()
def getEmptyGroup():
    grps=c.groups()
    for i in grps:
        if grps[i]['windows'] == []:
            return i


def sendToVacantScreen( scn):
    # send current window to next vacant window, focus that window 
    # on screen scn
    g = getEmptyGroup()
    c.window.togroup( g )
    c.group[g].toscreen(scn)
    
print sys.argv
sendToVacantScreen( int(sys.argv[1]))

