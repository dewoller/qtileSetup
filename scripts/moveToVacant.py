#!/usr/bin/python

import sys
from libqtile.command import Client
c = Client()
def getEmptyGroup():
    grps=c.groups()
    for i in grps:
        if grps[i]['windows'] == []:
            return i
    return -1



def sendToVacantScreen( scn):
    # send current window to next vacant window, focus that window 
    # on screen scn
    g = getEmptyGroup()
    if (g>=0):
        c.window.togroup( g )
        c.group[g].toscreen(scn)
    
sendToVacantScreen( int(sys.argv[1]))

