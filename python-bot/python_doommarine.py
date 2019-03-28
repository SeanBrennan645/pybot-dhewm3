#!/usr/bin/env python

import botbasic, time, sys
import botlib
from State import State
from StateMachine import StateMachine
from chvec import *
import math

debugTowards = False

#
# state definition for Wander
# Sean

class Wander(State):
    def run(self):
        print "IN WANDER STATE"
        mapTravel ()
    def next(self):
        you = findYou(b)
        playerDist = abs(b.getpos (me)[0] - b.getpos (you)[0])
        if playerDist <= 500:
            return Machine.attack
        return Machine.wander
#
# state definition for Attack
# Sean

class Attack(State):
    def run(self):
        print "IN ATTACK STATE"
        you = findYou(b)
        huntPlayer (you)
    def next(self):
        #outline for bot to stop attacking onc health function is fixed
        #if b.health() <= 40:
            #return Machine.wander

        return Machine.attack
#
# setting initial state for machine
# Sean

class Machine(StateMachine):
    def __init__(self):
        StateMachine.__init__(self, Machine.wander)

#
# adding created states to machine
# Sean

Machine.wander = Wander()
Machine.attack = Attack()



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
        #b.stopFiring ()
        #b.reload_weapon ()

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
    print "will go and find light"
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
    d = b.calcnav(i)
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


#
# basic function that allows the bot the find and fire at the player
# Sean

def huntPlayer (i):
    b.reset ()
    #count added so bot can reload once it run out of ammo
    count = 0
    #getting the dist between player and bot
    playerDist = abs(b.getpos (me)[0] - b.getpos (i)[0])
    while playerDist <= 300:
        b.aim (i)
        #b.face (i)
        fire ()
        count = count + 1
        if count == 16:
            b.reload_weapon ()
            count = 0
        playerDist = abs(b.getpos (me)[0] - b.getpos (i)[0])
    #print "Trying to stop firing"
    b.reload_weapon ()
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


#
# function to find and travel to a certain ammo postition
# Sean

def ammoTravel (e, r, l):
    b.reset ()
    print "will go and find ammo node"
    if debugTowards:
        print "bot is at", b.d2pv (b.getpos (me))
    d = b.ammoNav(e)
    if debugTowards:
        print "object", e, "is", d, "units away"
    if d is None:
        if debugTowards:
            print "cannot reach", e
        b.turn (90, 1)
        b.select (["turn"])
        b.forward (100, 100)
        b.select (["move"])
    else:
        if debugTowards:
            print "distance according to dijkstra is", d

        b.ammoJourney (100, d, r, l)

#
# function to travel around the entire map
# this version of map travel will stop if the player
# is within a certain range of the bot
# Sean

def mapTravel ():
     hunt = False
     rooms = b.getRooms()
     you = findYou (b)
     for r in range(1, rooms+1):
         if not hunt:
           ammo = b.getRoomAmmo (r)
           print "bot moving around map"
           print "number of ammo in room = ", ammo
           for l in range(ammo):
               dest = b.getAmmo(r, l)
               dest = map (int, dest)
               ammoTravel(dest, r, l)
               playerDist = abs(b.getpos (me)[0] - b.getpos (you)[0])
               if playerDist <=500:
                   hunt = True
               if hunt:
                   break

#
# function to travel around the entire map
# this version of map travel will continuously
# travel around the map
# Sean

def mapTravelTest ():
     hunt = False
     rooms = b.getRooms()
     you = findYou (b)
     for r in range(1, rooms+1):
         if not hunt:
           ammo = b.getRoomAmmo (r)
           print "bot moving around map"
           print "number of ammo in room = ", ammo
           for l in range(ammo):
               dest = b.getAmmo(r, l)
               dest = map (int, dest)
               ammoTravel(dest, r, l)

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
#
# note all commented out functions were simply used during testing
# Sean

def botMain (b):
    global me
    print "success!  python doom marine is alive"

    print "trying to get my id...",
    me = b.me ()
    print "yes"
    print "the python marine id is", me
    you = findYou (b)
    #print "you info is this", you
    #playerDist = abs(b.getpos (me)[0] - b.getpos (you)[0])
    #getting the total number of rooms within the map
    rooms = b.getRooms()
    hunt = False
    Machine().runBot()
    """
    #while True:

       #playerDist = abs(b.getpos (me)[0] - b.getpos (you)[0])
       #huntPlayer (you)
       #moveTowards(you)
       #Machine().runBot()
       #mapTravelTest ()
       print "rooms = ", rooms
       for r in range(1, rooms+1):
           ammo = b.getRoomAmmo (r)
           if not hunt:
               print "bot moving around map"
               print "number of ammo in room = ", ammo
               for l in range(ammo):
                   dest = b.getAmmo(r, l)
                   dest = map (int, dest)
                   ammoTravel(dest, r, l)
                   playerDist = abs(b.getpos (me)[0] - b.getpos (you)[0])
                   if playerDist <=500:
                       hunt = True
                   if hunt:
                       break
       if hunt:
           print "bot successfully broke out of loop and has begun hunt"
           huntPlayer(you)
       """
       # if playerDist <= 500:
        #     b.face (you)
         #    fire ()
       #print "bot health", b.health ()
       #time.sleep (0.3)


if len (sys.argv) > 1:
    doommarine = int (sys.argv[1])

b = botlib.bot ("localhost", "python_doommarine %d" % (doommarine))
execBot (b,False)
