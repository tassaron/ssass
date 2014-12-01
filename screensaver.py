#!/usr/bin/python3
'''
Somewhat Satisfactory Screensaver by tassaron
Nov 28-Dec 1 2014

accepts arguments:
screensaver.py size speed pause
'''

from sys import argv
from tass import *
import os

def rndCoords():
    start = randomNumber(1,Width_-1)
    cols=(start+randomNumber(1,4),start+randomNumber(5,6))
    start = randomNumber(1,Height_-1)
    rows=(start+randomNumber(1,4),start+randomNumber(5,6))
    return cols, rows

def addBorders():
    page.line(row=Height_-1) # bottom row
    page.fill('_')
    page.line(col=0,rows=(1,Height_-1)) # left side
    page.fill('|')
    page.line(col=Width_-1,rows=(1,Height_-1)) # right side
    page.fill('|')
    page.line(row=0,cols=(1,Width_-2))
    page.fill('_') # top minus corners
    page.cell(0,0); page.write(' ')
    page.cell(Width_-1,0); page.write(' ')

def dumptrackertofile(savefile, flickeryThing):
    with open(savefile, 'a', encoding='utf-8') as savefile:
        try:
            print(flickeryThing, file=savefile)
        except IOError:
            print("error saving data :(")
            quit()

def giveMessage():
    global msgNum
    if msgNum==-1:
        page.cell('centre','centre')
        page.write('Tassaron\'s Somewhat Satisfactory Screensaver',\
                   'Prepare to be somewhat satisfied! :O')
    else:
        page.area(rows=(13,Height_-14),cols=(19,Width_-19))
        page.fill() # empty out area between the lines
        page.cell('center','center')
        page.write(messages[msgNum])
    page.line(row=12); page.fill('>')
    page.line(row=Height_-12); page.fill('<')
    page.line(col=18); page.fill('^')
    page.line(col=Width_-18); page.fill('v')

    rndX=randomNumber(1,Width_-2); rndY=randomNumber(1,Height_-2)
    page.cell(rndX,rndY); page.write(':)')
    if msgNum != -1:
        for _ in range(5):
            rndX=randomNumber(1,Width_-2); rndY=randomNumber(1,Height_-2)
            page.cell(rndX,rndY); page.write(':)')
    else:
        # select :) we just printed
        page.line(cols=(rndX,rndX+1),row=rndY)
        for _ in range(25):
            newRndX=randomNumber(1,Width_-2); newRndY=randomNumber(1,Height_-2)
            # move it to new coords
            page.move(x=newRndX,y=newRndY)
            addBorders()
            page.paint()
            if not sleep(delay):
                quit()
            # select :) at new coords
            page.line(cols=(newRndX,newRndX+1),row=newRndY)
    msgNum=randomNumber(0,len(messages)-1)

if __name__=='__main__':
    # because it's fun to see how long I've run this
    savefile = os.getcwd() + '/trackers.dat'

    # start at my fullscreen size
    Width_=150; Height_=41
    speed=13; delay=0; paused=False # recommended :P
    msgNum=-1; messages = ['May the force be with you', 'Eat olives every day',
        'Don\'t forget to clean behind your ears', 'An apple a day is bad for you',
        'Drink more beer, do more dishes', 'who even cares about hamburgers',
        'Nipples are sometimes shaped like stars', 'Why are you reading this?',
        'dicks dicks dicks dicks dicks dicks', 'What will happen will happen',
        'When did you stop thinking of your parents\' house as your own?',
        'don\'t feed the memes', '*anonymous phone call* ;O']

    # if there are arguments...
    if len(argv) > 1:
        try:
            # look for the comma-separated size
            width, height = argv[1].split(',')
            Width_=int(width); Height_=int(height)
        except ValueError:
            # look for a size keyword instead
            if argv[1]=='tv':
                Width_=112; Height_=41
            elif argv[1]=='720':
                Width_=80; Height_=26
            elif argv[1]=='big':
                Width_=150; Height_=41
            elif argv[1]=='old':
                Width_=80; Height_=40
            elif argv[1]=='tall':
                Height_=69
    if len(argv) > 2:
        # controls how often the screen is painted
        try:
            speed = int(argv[2])
            if speed < 1:
                speed=1
        except ValueError:
            if argv[2]=='slow':
                speed=1
            elif argv[2]=='fast':
                speed=2
            elif argv[2]=='faster':
                speed=13
            elif argv[2]=='fastest':
                speed=23
            elif argv[2]=='snail':
                speed=1; delay=200
    if len(argv) > 3:
        if argv[3]=='pause':
            paused=True

    init('Screensaver',width=Width_,height=Height_,forceSize=True,beQuiet=True)

    # random junk to scribble on the screen
    letters = 'abcdefghijklmnopqrstuvwxyzxxxxxBBBBBBBBBBBBABCDEFGHIJKLNOPQSTUVWXYZ'
    numbers = '00000001111111129$%%%@#!@!!@#$^*&--==---=-=********##############'
    words = ['Bri','Hope','zzzzzzz','xyz',':)','olive','fart','tassaron','love',\
            'Jade','Carli','Nate','dicks','butt']

    iters=50
    page = screen()
    giveMessage()

    framesCreated=0
    framesDrawn=0
    tracker=0
    message=0

    while True:
        try:
            i = randomNumber(1,50)
            tracker+=i
            addBorders()

            # make the flickery things :3
            # add one because these are incremented after for convenience
            flickeryThing = str(framesDrawn+1)+'/'+str(framesCreated+1)+'/'+str(tracker)

            # change positions of flickery things every now and then
            if framesDrawn % 30 == 0:
                flickerX = randomNumber(1,Width_-len(flickeryThing))
                tracker+=flickerX
                topBotY = randomChoice([0,Height_-1])
                topBotX = randomChoice([0,Width_-1])
                flickerY = randomNumber(1,Height_-len(flickeryThing))
                tracker+=flickerY

            # add flickery things on borders
            page.cell(flickerX,topBotY);
            page.write(flickeryThing)
            page.cell(topBotX,flickerY)
            page.write(flickeryThing, direction='down')

            speed_=randomNumber(halfOf(speed),speed)
            tracker+=speed_

            if i % speed == 0:
                if framesCreated==0 or framesCreated>29:
                    page.paint()
                    if not sleep(delay):
                        dumptrackertofile(savefile,flickeryThing)
                        quit()
                    if paused:
                        pause()
                    framesDrawn+=1
                    message+=1
            framesCreated+=1
            movebg = " "*(10*len(letters))
            movebg+= letters


            x = randomNumber(0,Width_-1)
            y = randomNumber(0,Height_-1)
            if i == 7 or i == 25:
                # move random area to another random area
                # 1 and -2 to compensate for the borders
                height = [randomNumber(1,Height_-2), randomNumber(1,Height_-2)]
                width  = [randomNumber(1,Width_-2),   randomNumber(1,Width_-2)]
                height.sort(); width.sort()
                # don't let the areas get TOO big
                if height[1]-height[0] > 12:
                    height[1] = height[0]+12
                if width[1]-width[0] > 16:
                    width[1] = width[0]+16
                tracker+=height[0];tracker+=height[1]
                tracker+=width[0];tracker+=width[1]
                tuple(height); tuple(width)
                page.area(rows=(height),cols=(width))
                if i == 7:
                    page.move(x=x,y=y,bg=movebg)
                else:
                    page.move(x=x,y=y)
            elif i == 18 or i == 30:
                # move entire screen in a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                rndX=randomNumber(-6,6); rndY=randomNumber(-6,6)
                if i == 18:
                    page.move(x=rndX, y=rndY,bg=movebg)
                else:
                    page.move(x=rndX, y=rndY)
                tracker+=rndX+rndY
            elif i == 35:
                # draw arrows across somewhere
                row = randomNumber(1,Height_-2)
                tracker+=row
                page.line(row=row)
                direction = randomChoice(['>','<','><'])
                page.fill(direction)
            elif i == 15:
                # draw arrows up and down somewhere
                col = randomNumber(1,Width_-2)
                tracker+=col
                page.line(col=col)
                direction = randomChoice(['v','^','v^'])
                page.fill(direction)
            elif i == 44 or i == 43:
                # fill random area with random letters or numbers
                cols, rows = rndCoords()
                page.area(cols=cols,rows=rows)
                choice = randomChoice([letters,numbers])
                page.fill(choice)
            elif i % 2==0:
                if speed < 15:
                    number = 3
                elif speed > 14 and speed < 51:
                    number = 2
                else:
                    number = 1
                # draw numbers or letters at random positions
                for _ in range(number):
                    choice = randomChoice([letters,numbers])
                    rndIndex = randomNumber(0,len(choice)-1)
                    tracker+=rndIndex
                    rndX=randomNumber(1,Width_-2)
                    rndY=randomNumber(1,Height_-2)
                    page.cell(rndX, rndY)
                    tracker+=rndX+rndY
                    page.write(choice[rndIndex])
            else:
                # draw random portions of words at a random position
                word=''
                for _ in range(2):
                    rndNums=[]
                    for _ in range(2):
                        rndIndex = randomNumber(0,len(words)-1)
                        tracker+=rndIndex
                        rndNums.append(randomNumber(0,len(words[rndIndex])-1))
                    rndNums.sort()
                    for num in rndNums:
                        tracker+=num
                    word += words[rndIndex][rndNums[0]:rndNums[1]]
                page.cell(x,y)
                page.write(word)

            if message == 30:
                message=0
                giveMessage()

        except KeyboardInterrupt:
            dumptrackertofile(savefile,flickeryThing)
            quit()
