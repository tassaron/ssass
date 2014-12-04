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

# lots of stuff in here is inefficient and goofy. I'm not as concerned about this
# as I am about tass.py. I will probably fix it up eventually

def drawHeart(x,y):
    #page.area(cols=cols,rows=rows,shape='heart') I CAN DREAM CAN'T I
    page.cell(x,y)
    page.write( "  _____     _____  ",
                " /     \   /     \ ",
                "/       \ /       \\",
                '|        V        |',
                '|                 |',
                ' \               / ',
                '  \             /  ',
                '   \           /   ',
                '    \         /    ',
                '     \       /     ',
                '      \     /      ',
                '       \   /       ',
                '        \ /        ',
                '         V         ')

def spamSmilies(number):
    for _ in range(number):
        rndX=randomNumber(1,Width_-2); rndY=randomNumber(1,Height_-2)
        global tracker; tracker += rndX+rndY
        page.cell(rndX,rndY); page.write(':)')

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

def dumptrackertofile(savefile, flickeryThing, timestamp):
    if tracker > 1000000:
        endDate, endTime = getTimestamp('tuple')
        # try to centre the stuff so it's easy to read
        spaces = 34; spaces -= len(flickeryThing)
        spaces = halfOf(spaces); spaces = spaces*' '
        with open(savefile, 'a', encoding='utf-8') as savefile:
            try:
                print(timestamp+spaces+flickeryThing+spaces+endTime+' '+endDate, file=savefile)
            except IOError:
                print("error saving data :(")
            quit()

def giveMessage():
    global msgNum
    if msgNum==-1:
        page.cell('centre','centre')
        page.write(' Tassaron\'s Somewhat Satisfactory Screensaver',\
                   'Prepare to be somewhat satisfied! :O')
    else:
        page.area(rows=(11,Height_-11),cols=(17,Width_-17))
        page.fill() # empty out area between the lines
        page.cell('center','center')
        if randomNumber(1,5)==5:
            page.write(messages[msgNum])
        else:
            string=''
            for message in messages:
                if randomNumber(1,3)==3:
                    message = message.split()
                    string+=message[randomNumber(0,len(message)-1)]+' '
            if len(string)<20:
                string+='in my mouth'
            page.write(string)
    page.line(row=10); page.fill('>')
    page.line(row=Height_-10); page.fill('<')
    page.line(col=16); page.fill('^')
    page.line(col=Width_-16); page.fill('v')
    addBorders()
    page.paint()
    if not sleep(delay):
        quit()

    rndX=randomNumber(1,Width_-2); rndY=randomNumber(1,Height_-2)
    page.cell(rndX,rndY); page.write(':)')
    if msgNum != -1:
        spamSmilies(15)
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

def main():
    init('Screensaver',width=Width_,height=Height_,forceSize=True,beQuiet=True)
    global page; page = screen()

    iters=50
    giveMessage()

    framesCreated=0
    framesDrawn=0
    lastFrameDrawn=0
    maxFrameDrop=speed*3
    global tracker; tracker=0
    message=0
    nextmessage = randomNumber(60,120)
    movebg= (' '*30) + letters

    while True:
        try:
            i = randomNumber(1,50)
            tracker+=i
            addBorders()

            # make the flickery thing :3
            # add one because these are incremented after for convenience
            flickeryThing= str(framesDrawn+1)+'/'+str(framesCreated+1)+'/'+str(tracker)

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
            page.write(timestamp, direction='down')

            if speed > 1:
                # randomize frame-drops a bit
                halfSpeed = halfOf(speed,rounding='down')
                speed_=randomNumber(speed-halfSpeed,speed+halfSpeed)
                tracker+=speed_
            else:
                speed_ = speed

            if framesCreated==0 or framesCreated % speed_ == 0 \
               or (framesCreated-lastFrameDrawn > maxFrameDrop):
                page.paint()
                if not sleep(delay):
                    dumptrackertofile(savefile,flickeryThing,timestamp)
                    quit()
                if paused:
                    pause()
                framesDrawn+=1
                lastFrameDrawn = framesCreated
                message+=1
            framesCreated+=1


            x = randomNumber(0,Width_-1)
            y = randomNumber(0,Height_-1)
            if i == 7 or i == 24 or i == 31:
                # move random area to another random area
                # 1 and -2 to compensate for the borders
                cols, rows = randomArea(40, 40, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                if i == 33:
                    page.move(x=x,y=y,bg=movebg)
                else:
                    page.move(x=x,y=y)
            elif i == 18 or i == 30:
                # move entire screen in a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                rndX=randomNumber(-6,6); rndY=randomNumber(-6,6)
                page.move(x=rndX, y=rndY)
                tracker+=rndX+rndY
            elif i == 16:
                # draw random rectangle
                cols, rows = randomArea(18, 16, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows); page.fill() # empty the space
                page.line(row=rows[0],cols=cols); page.fill('_')
                page.line(row=rows[1],cols=cols); page.fill('_')
                page.line(col=cols[0],rows=rows); page.fill('|')
                page.line(col=cols[1],rows=rows); page.fill('|')
                page.cell(cols[0],rows[0]); page.write(' ')
                page.cell(cols[1],rows[0]); page.write(' ')
            elif i == 33:
                # draw arrows across somewhere
                row = randomNumber(1,Height_-2)
                tracker+=row
                page.line(row=row)
                direction = randomChoice(['>','<','><'])
                page.fill(direction)
            elif i == 15 or i == 17:
                # draw arrows up and down somewhere
                col = randomNumber(1,Width_-2)
                tracker+=col
                page.line(col=col)
                direction = randomChoice(['v','^','v^'])
                page.fill(direction)
            elif i == 44 or i == 43:
                # fill random area with random letters or numbers
                cols, rows = randomArea(8,6,cols=(1,Width_-2),rows=(1,Height_-2))
                page.area(cols=cols,rows=rows)
                choice = randomChoice([letters,numbers])
                page.fill(choice)
            elif i == 35:
                rndNum = randomNumber(0,10); tracker += rndNum
                if rndNum < 10:
                    spamSmilies(rndNum)
                else:
                    rndX = randomNumber(10,Width_-10); rndY = randomNumber(10,Height_-10)
                    tracker += rndX + rndY
                    drawHeart(rndX,rndY)
            elif i == 2 or i == 10 or i == 22:
                # randomly replace sections of numbers with letters
                # or entire screen of numbers with letters. or vice versa
                rndNum = randomNumber(0,10)
                tracker+=rndNum
                if rndNum < 9:
                    cols, rows = randomArea(10,10)
                    page.area(cols=cols,rows=rows)
                    if rndNum < 5:
                        page.findReplace(numbers,letters)
                    else:
                        page.findReplace(letters,numbers)
                else:
                    page.everything()
                    if rndNum==9:
                        page.findReplace(numbers,letters)
                    else:
                        page.findReplace(letters,numbers)
            elif i % 2==0:
                if speed < 5:
                    number = 3
                elif speed > 4 and speed < 30:
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
                if rndNums[0] != 2:
                    page.write(word)
                else:
                    page.write(word,direction='down')

            if message == nextmessage:
                tracker+=nextmessage
                nextmessage = randomNumber(60,120)
                message=0
                giveMessage()

        except KeyboardInterrupt:
            dumptrackertofile(savefile,flickeryThing,timestamp)
            quit()

if __name__=='__main__':
    # because it's fun to see how long I've run this
    savefile = os.getcwd() + '/trackers.dat'
    date, time = getTimestamp('tuple')
    timestamp = date+' '+time

    # start at my fullscreen size
    Width_=150; Height_=41
    speed=12; delay=0; paused=False # recommended :P
    msgNum=-1; messages = ['may the fonzie be with you', 'eat olives every day',
        'clean behind your ears', 'an apple a day is bad for you probably',
        'drink more beer, do more dishes', 'who even cares about hamburgers',
        'nipples are sometimes shaped like stars', 'why are you reading this?',
        'dicks dicks dicks dicks dicks dicks', 'what will happen will happen',
        'when did you stop thinking of your parents\' house as your own?',
        'don\'t feed the memes', '*anonymous phone call* ;O','yummy yummy cake',
        'don\'t worry, clowns will eat you', 'nine dot nine', 'boobs are cool',
        'hungry hungry hippos strike again','tigers and bears, oh my!',
        'call all your poor nibling siblings', 'your tongue will get stuck',
        'don\'tcha put it in your mouth', 'don\'tcha stuff it in your face',
        'it looks good to eat', 'powerful vacuums suck', 'guess what I\'m thinking',
        'what does cat food tastes like?']

    # random junk to scribble on the screen
    letters = 'abcdefghijklmnopqrstuvwxyzxxxxxBBBBBBBBBBBBABCDEFGHIJKLNOPQSTUVWXYZ'
    numbers = '00000001111111129$%%%@#!@!!@#$^*&--==---=-=********##############'
    words = ['Brianna','sister','beautiful','symmetrical','patterns','olives','farts','tassaron','love love',\
            'Jade Jade','Carliii','Nathanael','dick','dicks','big butts','dancers','cyan','eyeballs','boobs','love love','love love']

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
                Width_=80; Height_=41
            elif argv[1]=='tall':
                Height_=69
            elif argv[1]=='square':
                Width_=32; Height_=32
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
                speed=3
            elif argv[2]=='faster':
                speed=12
            elif argv[2]=='fastest':
                speed=27
            elif argv[2]=='snail':
                speed=1; delay=200
    if len(argv) > 3:
        if argv[3]=='pause':
            paused=True

    while True:
        main()
