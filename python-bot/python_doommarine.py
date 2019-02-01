#!/usr/bin/env python

import botbasic, time, sys
import botlib
from chvec import *
import math

debugTowards = False


def walkSquare ():
    b.forward (100, 100)
    b.select (["move"])
    b.left (100, 100)
    b.select (["move"])
    b.back (100, 100)
    b.select (["move"])
    b.right (100, 100)
    b.select (["move"])


def runArc (a):
    b.forward (100, 100)
    b.turn (a, 1)
    b.select (["move"])
    b.select (["turn"])


def circle ():
    while True:
        for a in range (0, 360, 45):
            runArc (a+180)
        time.sleep (5)
        for w in range (0, 10):
            print "attempting to change to weapon", w,
            print "dhewm3 returns", b.changeWeapon (w)
            time.sleep (3)

def change ():
    for w in range (0, 10):
            print "attempting to change to weapon", w,
            print "dhewm3 returns", b.changeWeapon (w)
            time.sleep (3)

#fire function
def fire ():
        b.startFiring ()
        time.sleep (1)
        b.reload_weapon ()

def testturn (a):
    b.turn (a, 1)
    b.select (["turn"])

def sqr (x):
    return x * x

def calcDist (d0, d1):
    p0 = b.d2pv (d0)
    p1 = b.d2pv (d1)
    s = subVec (p0, p1)
    return math.sqrt (sqr (s[0]) + sqr (s[1]))

def moveTowards (i):
    b.reset ()
    print "will go and find", i
    print "I'm currently at", b.getpos (me), "and", i, "is at", b.getpos (i)
    """
    if not equVec (b.d2pv (b.getpos (me)), [12, 9]):
        print "failed to find getpos at 12, 9 for python"
    if not equVec (b.d2pv (b.getpos (i)), [40, 3]):
        print "failed to find getpos at 40, 3 for player"
    """
    if debugTowards:
        print "bot is at", b.d2pv (b.getpos (me))
        print "you are at", b.d2pv (b.getpos (you))
    d = b.calcnav (i)
    if debugTowards:
        print "object", i, "is", d, "units away"
    if d is None:
        if debugTowards:
            print "cannot reach", i
        b.turn (90, 1)
        b.select (["turn"])
        b.forward (100, 100)
        b.select (["move"])
    else:
        if debugTowards:
            print "distance according to dijkstra is", d
        b.journey (100, d, i)
        if debugTowards:
            print "finished my journey to", i
            print "  result is that I'm currently at", b.getpos (me), "and", i, "is at", b.getpos (i)
            print "      penguin tower coords I'm at", b.d2pv (b.getpos (me)), "and", i, "is at", b.d2pv (b.getpos (i))



#basic function that allows the bot the find and fire at the player
def huntPlayer (i):
    b.reset ()
    #getting the dist between player and bot
    playerDist = abs(b.getpos (me)[0] - b.getpos (i)[0])
    print "will go and find", i
    print "I'm currently at", b.getpos (me), "and", i, "is at", b.getpos (i)
    """
    if not equVec (b.d2pv (b.getpos (me)), [12, 9]):
        print "failed to find getpos at 12, 9 for python"
    if not equVec (b.d2pv (b.getpos (i)), [40, 3]):
        print "failed to find getpos at 40, 3 for player"
    """
    if playerDist <= 500:
        #b.aim (i)
        b.face (i)
        fire ()
    if debugTowards:
        print "bot is at", b.d2pv (b.getpos (me))
        print "you are at", b.d2pv (b.getpos (you))
    d = b.calcnav (i)
    if debugTowards:
        print "object", i, "is", d, "units away"
    if d is None:
        if debugTowards:
            print "cannot reach", i
        b.turn (90, 1)
        b.select (["turn"])
        b.forward (50, 50)
        b.select (["move"])
    else:
        if debugTowards:
            print "distance according to dijkstra is", d
        b.journey (100, d, i)
        if debugTowards:
            print "finished my journey to", i
            print "  result is that I'm currently at", b.getpos (me), "and", i, "is at", b.getpos (i)
            print "      penguin tower coords I'm at", b.d2pv (b.getpos (me)), "and", i, "is at", b.d2pv (b.getpos (i))



def findAll ():
    for i in b.allobj ():
        print "the location of python bot", me, "is", b.getpos (me)
        if i != me:
            b.aim (i)
           # moveTowards (i)
            time.sleep (3)

def findYou (b):
    for i in b.allobj ():
        if i != b.me ():
            return i


def antiClock (b):
    print "finished west, north, east, south"
    print "west, north, east, south diagonal"
    for v in [[1, 1], [-1, 1], [-1, -1], [1, -1]]:
        print "turning",
        b.turnface (v, 1)
        b.sync ()
        print "waiting"
        time.sleep (10)
        print "next"
        b.reset ()


def clock (b):
    print "finished west, north, east, south"
    print "west, north, east, south diagonal"
    for v in [[1, 1], [1, -1], [-1, -1], [-1, 1]]:
        print "turning",
        b.turnface (v, -1)
        b.sync ()
        print "waiting"
        time.sleep (10)
        print "next"
        b.reset ()

def test_crouch_jump (b):
    b.reset ()
    print "trying to hop"
    b.stepup (-2, 3*12)
    b.select (['move'])
    time.sleep (2)
    b.stepup (100, 4*12)
    b.select (['move'])

doommarine = -2

def execBot (b, useExceptions = True):
    if useExceptions:
        try:
            botMain (b)
        except:
            print "bot was killed, or script terminated"
            return
    else:
        botMain (b)


def botMain (b):
    global me
    print "success!  python doom marine is alive"

    print "trying to get my id...",
    me = b.me ()
    print "yes"
    print "the python marine id is", me
    you = findYou (b)
   # playerDist = abs(b.getpos (me)[0] - b.getpos (you)[0])

    while True:

      #   playerDist = abs(b.getpos (me)[0] - b.getpos (you)[0])
         huntPlayer (you)
      #  moveTowards (you)

       # if playerDist <= 500:
        #     b.face (you)
         #    fire ()

       # b.face (you)
       # change ()
       # fire ()
       # test_crouch_jump (b)
       # circle ()
       # b.reload_weapon ()
       # time.sleep (3)


if len (sys.argv) > 1:
    doommarine = int (sys.argv[1])

b = botlib.bot ("localhost", "python_doommarine %d" % (doommarine))
execBot (b,False)
