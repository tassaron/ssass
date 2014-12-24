#!/usr/bin/python3

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#
#                              screensaver.py
#                  The Somewhat Satisfactory Screensaver
#                       an experiment by tassaron
#                       written Nov 28-Dec 14 2014
#
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#
# If you like it, you can make it executable (chmod +x) and access it anywhere
# by adding this function to your .bashrc or .bash_aliases:
'''
screensaver() {
    cd ~/location/of/this/file && ./screensaver.py "$@";
}
'''
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

from ssass import *
import argparse
import os

# lots of stuff in here is inefficient and goofy. I'm not as concerned about this
# as I am about ssass.py. I will probably fix it up eventually

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
        rndX=random.number(1,Width_-2); rndY=random.number(1,Height_-2)
        page.cell(rndX,rndY); page.write(':)')

def addBorders():
    page.row(Height_-1) # bottom row
    page.fill('_')
    page.area(col=0,rows=(1,Height_-1)) # left side
    page.fill('|')
    page.area(col=Width_-1,rows=(1,Height_-1)) # right side
    page.fill('|')
    page.area(row=0,cols=(1,Width_-2))
    page.fill('_') # top minus corners
    page.cell(0,0); page.write(' ')
    page.cell(Width_-1,0); page.write(' ')

def dumptrackertofile(savefile, timestamp):
    playSound('shutdown')
    global tracker
    global flickeryThing
    if tracker > 1000000:
        endDate, endTime = getTimestamp('tuple')
        # try to centre the stuff so it's easy to read
        spaces = 34; spaces -= len(flickeryThing)
        spaces = halfOf(spaces); spaces = spaces*' '
        with open(savefile, 'a', encoding='utf-8') as savefile:
            try:
                print("%s%s%s%s%s %s" % (timestamp, spaces, flickeryThing,\
                      spaces, endTime, endDate), file=savefile)
            except IOError:
                print("error saving data :(")
            quit()

def pickASCIIart():
    global ASCIIart
    diceroll = random.number(0,len(ASCIIart)-1)
    return ASCIIart[diceroll]

def giveMessage():
    global msgNum; global messages
    if msgNum==-1:
        playSound('startup')
        x = halfOf(Width_); y = halfOf(Height_)-1
        page.cell('centre','centre')
        if Debug:
            string =  'Tassaron\'s Somewhat Satisfactory Debug Mode'
            page.write(string, 'Prepare For Your Terminal To Break! :O')
        else:
            string = 'Tassaron\'s Somewhat Satisfactory Screensaver'
            page.write(string, 'Prepare to be somewhat satisfied! :O')
    else:
        x = random.number(20,Width_-21)
        y = random.number(10,Height_-11)
        page.area(rows=(11,Height_-11),cols=(17,Width_-17))
        page.fill() # empty out area between the lines
        page.cell(x,y)
        if random.number(0,4)==4:
            string = messages[msgNum]
        else:
            string=''
            for message in messages:
                if random.number(0,1)==1:
                    message = message.split()
                    string+=message[random.number(0,len(message)-1)]+' '
            if len(string)<20:
                string+='in my mouth'
        page.write(string)
    page.row(y-8); page.fill('>')
    page.row(y+10); page.fill('<')
    page.column(x-len(string)-4); page.fill('^')
    page.column(x+len(string)+4); page.fill('v')
    addBorders()
    page.paint()
    if not sleep(delay):
        quit()

    rndX=random.number(1,Width_-2); rndY=random.number(1,Height_-2)
    page.cell(rndX,rndY); page.write(':)')
    if msgNum != -1:
        spamSmilies(15)
    else:
        # select :) we just printed
        page.area(cols=(rndX,rndX+1),row=rndY)
        for _ in range(25):
            newRndX=random.number(1,Width_-2); newRndY=random.number(1,Height_-2)
            # move it to new coords
            page.move(x=newRndX,y=newRndY)
            addBorders()
            page.paint()
            if not sleep(delay):
                quit()
            if paused:
                pause()
            # select :) at new coords
            page.area(cols=(newRndX,newRndX+1),row=newRndY)
    msgNum=random.number(0,len(messages)-1)
    return string

def getTime():
    global currentTime
    date, time = getTimestamp('tuple')
    currentTime = '%s|%s' % (date, time)
    clock = threading.Timer(60.0,getTime)
    clock.start()

def play(totalScreens, screenID=0):
    global tracker; global bigTracker
    global recycled; global flickeryThing
    tracker=0; bigTracker=0; recycled=0
    rndNumI=0; smallRndNumI=0; rndNum=0; smallRndNum=0
    DebugMessage=':)'

    global brainEnabled
    if brainEnabled:
        brain = getBrain()

    global currentTime
    getTheTime = threading.Thread(target=getTime,daemon=True)
    getTheTime.start()

    # give introductory message
    giveMessage()

    # screen statistics
    framesCreated=0
    framesDrawn=0
    framesDrawnAtLastScreenChange=0
    lastFrameDrawn=0
    maxFrameDrop=speed*3
    message=0
    nextmessage = random.number(60,120)
    impress=0
    # default time for a certain animation to play
    # measured in framesDrawn (thus unaffected by speed)
    longevity = 250

    # bouncy ASCII art!
    ASCIIart = pickASCIIart()
    widthOfObject = len(ASCIIart[0])
    ASCIIx = halfOf(Width_ - widthOfObject)
    ASCIIy = halfOf(Height_-1)
    ASCIIdirection = random.choice(['ne','nw','se','sw'])
    rightBorder = Width_-1; leftBorder = 1
    bottomBorder = Height_-1; topBorder = 1
    ASCIIbg = ' '*4 + '*'

    while True:

        i = random.number(1,30)
        addBorders()

        # draw message from giveMessage() for several frames
        if impress > 0:
            page.cell('centre','centre')
            page.write(string)
            impress -= 1

        # make the flickery things :3
        if brainEnabled:
            tracker, bigTracker, recycled, rndNumI, smallRndNumI, rndNum, smallRndNum, DebugMessage = brain.getTrackers()
        # add one because these are incremented after for convenience
        frameTracker = 'screenid_%s__drawn_%s__created_%s____recycled_%s__sum_%s__total_%s' % (str(screenID),
                str(framesDrawn+1), str(framesCreated+1), str(recycled), str(bigTracker), str(tracker))
        flickeryThing= 'rnd#i_%s__rnd#_%s____srnd#i_%s__srnd#_%s__' % (str(rndNumI),
                str(rndNum), str(smallRndNumI), str(smallRndNum))
        if Width_ > 80:
            flickeryThing += "__%s" % DebugMessage

        # change positions of flickery things every now and then
        if framesDrawn % 30 == 0:
            topFlickerX = random.number(0,Width_-len(flickeryThing))
            bottomFlickerX = random.number(0,Width_-len(frameTracker))
            leftFlickerY = random.number(0,Height_-len(timestamp))
            rightFlickerY = random.number(0,Height_-len(currentTime))

        # the flickery thing!
        page.cell(topFlickerX,0)
        page.write(flickeryThing)
        # frameTracker
        page.cell(bottomFlickerX,Height_-1)
        page.write(frameTracker)
        # time started
        page.cell(0,leftFlickerY)
        page.write(timestamp, direction='down')
        # current time
        page.cell(Width_-1,rightFlickerY)
        page.write(currentTime,direction='down')

        # draw the frame!
        if framesCreated==0 or framesCreated % speed == 0 \
           or (framesCreated-lastFrameDrawn > maxFrameDrop):
            page.paint()
            if not sleep(delay):
                dumptrackertofile(savefile,timestamp)
                quit()
            if paused:
                pause()
            framesDrawn+=1
            lastFrameDrawn = framesCreated
            message+=1
        framesCreated+=1

        if random.number(0,longevity) == 0:
            screenID += 1
            if screenID > totalScreens:
                screenID = 0

        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
        #   SCREENID 0
        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

        if screenID==0:
            longevity = 250
            x = random.number(1,Width_-2)
            y = random.number(1,Height_-2)
            if i == 1 or i == 11 or i == 21:
                # move random area to another random area
                # 1 and -2 to compensate for the borders
                movebg= (' '*30) + letters
                cols, rows = random.area(10, 10, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                x = random.number(1, Width_-2); y = random.number(1, Height_-2)
                if random.number(1,20) < 20:
                    page.move(x=x,y=y,bg=movebg)
                else:
                    page.move(x=x,y=y)
            elif i == 2 or i == 12:
                # move entire screen in a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                rndX=random.number(-6,6)
                rndY=random.number(-6,6)
                page.move(x=rndX, y=rndY)
            elif i == 3:
                # draw random rectangle
                cols, rows = random.area(8, 6, cols=(1,Width_-2), rows=(1, Height_-2))
                # empty the space out
                page.area(cols=cols,rows=rows); page.fill()
                page.area(row=rows[0],cols=cols); page.fill('_')
                page.area(row=rows[1],cols=cols); page.fill('_')
                page.area(col=cols[0],rows=rows); page.fill('|')
                page.area(col=cols[1],rows=rows); page.fill('|')
                page.cell(cols[0],rows[0]); page.write(' ')
                page.cell(cols[1],rows[0]); page.write(' ')
            elif i == 4:
                # draw arrows across somewhere
                row = random.number(1,Height_-2)
                page.row(row)
                direction = random.choice(['>','<','><'])
                page.fill(direction)
            elif i == 5 or i == 13:
                # draw arrows up and down somewhere
                col = random.number(1,Width_-2)
                page.column(col)
                direction = random.choice(['v','^','v^'])
                page.fill(direction)
            elif i==6 or i==14:
                # write random word from a message at random position
                page.cell(x,y)
                msg = messages[random.number(0,len(messages)-1)]
                msg = msg.split()
                page.write(msg[random.number(0,len(msg)-1)])
            elif i == 7 and random.number(0,99) > 90 and framesDrawn > 240:
                if brainEnabled:
                    # sometimes put random numbers in order
                    if random.number(0,1)==1:
                        brain.reorderThoughts()
                    else:
                        brain.reorderThoughts('backward')
            elif i == 8 or i == 14:
                # fill random area with random letters or numbers
                cols, rows = random.area(10, 10, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                choice = random.choice([letters,numbers])
                page.fill(choice)
            elif i == 9:
                # skew everything a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                page.skew(random.choice(['left', 'right']))
            elif i == 10:
                screenID = 4
            elif i == 15:
                rndNum = random.number(0,10)
                if rndNum < 10:
                    spamSmilies(6)
                else:
                    rndX = random.number(0,Width_-20)+10
                    rndY = random.number(0,Height_-20)+10
                    drawHeart(rndX,rndY)
            elif i == 16 or i == 26 or i == 18:
                # randomly replace sections of numbers with letters
                # or entire screen of numbers with letters. or vice versa
                rndNum = random.number(0,10)
                cols, rows = random.area(20, 20, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                if rndNum < 5:
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
                    choice = random.choice([letters, numbers])
                    rndIndex = random.number(0,len(choice)-2)
                    rndX=random.number(1,Width_-2)
                    rndY=random.number(1,Height_-2)
                    page.cell(rndX, rndY)
                    page.write(choice[rndIndex])
            else:
                # draw random portions of words at a random position
                word=''
                for _ in range(2):
                    rndNums=[]
                    for _ in range(2):
                        rndIndex = random.number(0,len(words)-1)
                        rndNums.append(random.number(1,len(words[rndIndex])-1))
                    rndNums.sort()
                    word += words[rndIndex][rndNums[0]:rndNums[1]]
                page.cell(x,y)
                if rndNums[0] != 2:
                    page.write(word)
                else:
                    page.write(word,direction='down')

        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
        #   SCREENID 1
        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

        elif screenID==1:
            longevity=100
            x = random.number(1, Width_-2)
            y = random.number(1, Height_-2)
            if i == 16 or i == 21 or i==25 or i==26:
                # fill random area with random letters or numbers
                cols, rows = random.area(10, 10, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                choice = random.choice([letters,numbers])
                page.fill(choice)
            elif i == 17 or i == 19:
                # skew everything a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                page.skew(random.choice(['left', 'right']))
            elif i == 18 or i == 1 or i == 2 or i == 7 or i == 8:
                # move entire screen left
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                rndX=random.number(-10,-1)
                page.move(x=rndX, y=1)
            elif i==22 or i==23 or i==24 or i==3:
                # write random word from a message at random position
                page.cell(x,y)
                msg = messages[random.number(0,len(messages)-1)]
                msg = msg.split()
                page.write(msg[random.number(0,len(msg)-1)])
            elif i==9 or i==10:
                screenID=0
            # draw random rectangle
            cols, rows = random.area(24, 18, cols=(1,Width_-2), rows=(1, Height_-2))
            page.area(cols=cols,rows=rows)
            if i % 4 != 0:
                page.fill() # empty the space
            page.area(row=rows[0],cols=cols); page.fill('_')
            page.area(row=rows[1],cols=cols); page.fill('_')
            page.area(col=cols[0],rows=rows); page.fill('|')
            page.area(col=cols[1],rows=rows); page.fill('|')
            page.cell(cols[0],rows[0]); page.write(' ')
            page.cell(cols[1],rows[0]); page.write(' ')

        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
        #   SCREENID 2
        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

        elif screenID==2:
            longevity=50
            x=random.number(1,Width_-2)
            y=random.number(1,Height_-2)
            i=random.number(1,15)
            if i==1 or i==5 or i==6:
                # fill random area with random letters or numbers
                cols, rows = random.area(10, 10, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                choice = random.choice([letters,numbers])
                page.fill(choice)
            elif i==2:
                # move random area to another area with fills
                cols, rows = random.area(20, 18, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                page.move(x=x,y=y,bg=numbers)
            elif i==3:
                # move entire screen somewhere, with fills
                page.area(cols=(1,Width_-2),rows=(1,Height_-2))
                page.move(x=x,y=y,bg=letters)
            elif i==13:
                drawHeart(x,y)
            elif i==4:
                # randomly replace sections of numbers with letters
                # or entire screen of numbers with letters. or vice versa
                rndNum = random.number(0,10)
                cols, rows = random.area(20, 20, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                if rndNum < 5:
                    page.findReplace(numbers,letters)
                else:
                    page.findReplace(letters,numbers)
            elif i==7 or i==8 or i==9:
                # draw random rectangle
                cols, rows = random.area(8, 6, cols=(1,Width_-2), rows=(1, Height_-2))
                # empty the space out
                page.area(cols=cols,rows=rows); page.fill()
                page.area(row=rows[0],cols=cols); page.fill('_')
                page.area(row=rows[1],cols=cols); page.fill('_')
                page.area(col=cols[0],rows=rows); page.fill('|')
                page.area(col=cols[1],rows=rows); page.fill('|')
                page.cell(cols[0],rows[0]); page.write(' ')
                page.cell(cols[1],rows[0]); page.write(' ')
            elif i==10:
                screenID=3
            elif i==11 or i==12:
                # skew everything a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                page.skew(random.choice(['left', 'right']))
            elif i>13:
                screenID=3

        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
        #   SCREENID 3
        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

        elif screenID==3:
            longevity = 100
            x = random.number(1,Width_-2)
            y = random.number(1,Height_-2)

            try:
                if scroller > 0:
                    page.area(cols=(1,Width_-2),rows=(1,Height_-2))
                    page.move(x=0,y=scroller)
                    scroller-=1
            except UnboundLocalError:
                scroller=0

            if i == 1 or i == 11 or i == 21:
                # move random area to another random area
                # 1 and -2 to compensate for the borders
                movebg= (' '*30) + letters + numbers
                cols, rows = random.area(20, 20, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                if random.number(1,20) < 20:
                    page.move(x=x,y=y,bg=movebg)
                else:
                    page.move(x=x,y=y)
            elif i == 3 or i == 13 or i == 23 or i == 30:
                ch = range(random.number(1,3))
                for _ in ch:
                    # draw random rectangle
                    cols, rows = random.area(8, 6, cols=(1,Width_-2), rows=(1, Height_-2))
                    # empty the space out
                    page.area(cols=cols,rows=rows); page.fill()
                    page.area(row=rows[0],cols=cols); page.fill('_')
                    page.area(row=rows[1],cols=cols); page.fill('_')
                    page.area(col=cols[0],rows=rows); page.fill('|')
                    page.area(col=cols[1],rows=rows); page.fill('|')
                    page.cell(cols[0],rows[0]); page.write(' ')
                    page.cell(cols[1],rows[0]); page.write(' ')
            elif i == 20:
                # draw ~ across somewhere
                row = random.number(1,Height_-2)
                page.row(row)
                direction = random.choice(['~','-~-~','()'])
                page.fill(direction)
            elif i == 15:
                scroller=10
            elif i==4 or i==14 or i==24 or i==28 or i==29:
                # write random word from a message at random position
                page.cell(x,y)
                msg = messages[random.number(0,len(messages)-1)]
                msg = msg.split()
                page.write(msg[random.number(0,len(msg)-1)])
            elif i == 5 or i == 25:
                # fill random area with random letters or numbers
                cols, rows = random.area(10, 10, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                choice = random.choice([letters,numbers])
                page.fill(choice)
            elif i == 13 or i == 25 or i==26 or i==27:
                # skew everything a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                page.skew(random.choice(['left', 'right']))
            elif i == 3:
                drawHeart(x,y)
            elif i == 2 or i == 10 or i == 22:
                page.area(cols=(1,Width_-2),rows=(1,Height_-2))
                if random.number(0,1) == 1:
                    page.findReplace(numbers,letters)
                else:
                    page.findReplace(letters,numbers)
            elif i==6:
                screenID=1
            else:
                for _ in range(random.number(5,15)):
                    x = random.number(1,Width_-2)
                    y = random.number(1,Height_-2)
                    page.cell(x,y)
                    page.write(random.choice(['~','-','-~-','~*~*']))

        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
        #   SCREENID 4
        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

        elif screenID==4:
            longevity = 20
            x = halfOf(Width_); y = halfOf(Height_)
            if i == 1 or i == 11:
                # move entire screen in a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                rndX=random.number(0,13)-6
                rndY=random.number(0,13)-6
                page.move(x=rndX, y=rndY)
            elif i == 2 or i == 12:
                screenID=0
            elif i == 3 or i == 13:
                screenID=2
            elif i == 4 or i == 14:
                screenID=3
            else:
                x = halfOf(Width_); y = halfOf(Height_)
                rndX = random.number(1,Width_-2)
                choice = random.number(0,3)
                page.line((x, y), (rndX, random.choice([1,Height_-2])))
                if choice == 0 :
                    page.fill(letters)
                elif choice == 1:
                    page.fill(numbers)
                elif choice == 2:
                    if random.number(0,40) > 0:
                        word='' # random portion of a word
                        for _ in range(2):
                            rndNums=[]
                            for _ in range(2):
                                rndIndex = random.number(0,len(words)-1)
                                rndNums.append(random.number(0,\
                                                len(words[rndIndex])-1))
                            rndNums.sort()
                            word.join(words[rndIndex][rndNums[0]:rndNums[1]])
                        page.fill(word)
                    else:
                        page.fill(words)
                elif choice == 3:
                    msg = messages[random.number(0,len(messages)-1)]
                    msg = msg.split()
                    page.fill(msg[random.number(0,len(msg)-1)])

        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
        #   EVERY SCREENID
        #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

        if message == nextmessage:
            string = giveMessage()
            impress = 60
            nextmessage = random.number(30,60)
            message=0

        # draw and select bouncing ASCII art
        page.cell(ASCIIx,ASCIIy)
        page.write(ASCIIart[0],ASCIIart[1],ASCIIart[2])
        page.area(cols=(ASCIIx, ASCIIx+widthOfObject), rows=(ASCIIy, ASCIIy+2))

        oldDirection = ASCIIdirection
        # determine bounce and direction
        if ASCIIdirection == 'ne': # up right
            if ASCIIx+widthOfObject+1 >= rightBorder and ASCIIy >= topBorder:
                ASCIIdirection = 'nw'
            elif ASCIIx+widthOfObject+1 >= rightBorder and ASCIIy <= topBorder:
                ASCIIdirection = 'sw'
            elif ASCIIx+widthOfObject+1 <= rightBorder and ASCIIy <= topBorder:
                ASCIIdirection = 'se'
        elif ASCIIdirection == 'se': # down right
            if ASCIIx+widthOfObject+1 >= rightBorder and ASCIIy+3 <= bottomBorder:
                ASCIIdirection = 'sw'
            elif ASCIIx+widthOfObject+1 >= rightBorder and ASCIIy+3 >= bottomBorder:
                ASCIIdirection = 'nw'
            elif ASCIIx+widthOfObject+1 <= rightBorder and ASCIIy+3 >= bottomBorder:
                ASCIIdirection = 'ne'
        elif ASCIIdirection == 'nw': # up left
            if ASCIIx-1 >= leftBorder and ASCIIy <= topBorder:
                ASCIIdirection = 'sw'
            elif ASCIIx-1 <= leftBorder and ASCIIy >= topBorder:
                ASCIIdirection = 'ne'
            elif ASCIIx-1 <= leftBorder and ASCIIy <= topBorder:
                ASCIIdirection = 'se'
        elif ASCIIdirection == 'sw': # down left
            if ASCIIx-1 >= leftBorder and ASCIIy+3 >= bottomBorder:
                ASCIIdirection = 'nw'
            elif ASCIIx-1 <= leftBorder and ASCIIy+3 >= bottomBorder:
                ASCIIdirection = 'ne'
            elif ASCIIx-1 <= leftBorder and ASCIIy+3 <= bottomBorder:
                ASCIIdirection = 'se'

        if oldDirection != ASCIIdirection:
            ch = random.choice(['bang1','bang2','bang3'])
            playSound(ch)

        # change ASCIIx and ASCIIy
        if ASCIIdirection == 'ne': # up right
            ASCIIx+=1; ASCIIy-=1
        elif ASCIIdirection == 'nw': # up left
            ASCIIx-=1; ASCIIy-=1
        elif ASCIIdirection == 'se': # down right
            ASCIIx+=1; ASCIIy+=1
        elif ASCIIdirection == 'sw': # down left
            ASCIIx-=1; ASCIIy+=1

        # move bouncing ASCII art
        page.move(x=ASCIIx,y=ASCIIy,bg=ASCIIbg)
        if random.number(0,999) > 975:
            ASCIIart = pickASCIIart()
            widthOfObject = len(ASCIIart[0])

if __name__=='__main__':
    # because it's fun to see how long I've run this
    savefile = os.getcwd() + '/trackers.dat'
    date, time = getTimestamp('tuple')
    timestamp = '%s|%s' % (date, time)

    # parse command line arguments
    fancyline = '#-~-~-~-~-~-~--~-~-~-~-~-~-#'
    parser = argparse.ArgumentParser(prog='screensaver', description=fancyline,
                        epilog=fancyline)
    parser.add_argument('-speed', choices=['snail','slow','normal','fast','faster',
                        'fastest'], help='# of frames to calculate on \
                        average between frames\n', default='normal')
    parser.add_argument('-size', choices=['classic','medium','big','square','720','tv',
                        'tall'], default='big')
    parser.add_argument('--pause', help='wait for a keypress after every frame',
                        action='store_true')
    parser.add_argument('--debug', help='displays certain technical details',
                        action='store_true')
    parser.add_argument('--wasteful', help='do not recycle numbers',
                        action='store_true')
    parser.add_argument('--quiet', help='don\'t play sound effects',
                        action='store_true')
    arg = vars(parser.parse_args()) # return arguments as a dictionary

    # -speed
    delay=0
    if arg['speed']=='snail':
        speed=1; delay=250
    elif arg['speed']=='slow':
        speed=1
    elif arg['speed']=='normal':
        speed=3
    elif arg['speed']=='fast':
        speed=6
    elif arg['speed']=='faster':
        speed=9
    elif arg['speed']=='fastest':
        speed=12
    # -size
    if arg['size']=='classic':
        Width_=80; Height_=41
    elif arg['size']=='big':
        Width_ = 150
        if currentOS()=='nt':
            Height_=54
        else:
            Height_=41
    elif arg['size']=='medium':
        Width_=108
        Height_=32
    elif arg['size']=='square':
        Width_=32; Height_=32
    elif arg['size']=='720':
        Width_=80; Height_=26
    elif arg['size']=='tv':
        Width_=112; Height_=41
    elif arg['size']=='tall':
        Width_=80; Height_=69
    # --pause
    if arg['pause']:
        paused=True
    else:
        paused=False
    global Debug
    if arg['debug']:
        debug(True,'area','screen','cell','line')
        Debug=True
    else:
        debug(False, 'area', 'screen', 'cell','line')
        Debug=False

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
        'what does cat food tastes like?','Harper\'s Little Room','Tarasius is watching',
        'patterns patterns patterns patterns','shuffling the future']

    # random junk to scribble on the screen
    letters = 'abcdefghijklmnopqrstuvwxyzxxxxxBBBBBBBBBBBBABCDEFGHIJKLNOPQSTUVWXYZ'
    numbers = '371371371371222$%%%@#!@!!@#$&&&&????$$$****#######'
    words=[ 'Brianna','sister','beautiful','symmetrical','patterns','olives',
            'farts','tassaron','love love','Jade Jade','Carliii','Nathanael',
            'dick','dicks','big butts','dancers','cyan','eyeballs','boobs',
            'love love','love love','treadmills','screensaver','funky','laundry',
            'hairballs','kittens','asteroids','dinosaurs','magic','frighten',
            'Tarasius','kittens']

    ASCIIart = [
        ["|     +--+ \\    / +-----",
        "|    |    | \\  /  |_____",
        "|____ \\__/   \\/   |_____"],
        [" __ __  /\\   __ __",
        "(_ (_  /__\\ (_ (_ ",
        "__)__)/    \\ _)__) "],
        ["|   |  +--+  ___  +-----",
        "+---+ |    | |__) |____",
        "|   |  \__/  |    |_____"],
        ["|\  |  /\  _____ +-----",
        "| \ | /__\   |   |_____",
        "|  \|/    \  |   |_____"],
        [" --+-- /\\   +---  +----",
        "   |  /__\\  |   \\ |____",
        "\\__/ /    \\ |___/ |____"],
        [" +--  /\\    __       ___" ,
        "/    /__\\  |__) |     |",
        "\\___/    \\ |  \\ |___ _|_"],
        [" __   __  /\\   +-- __",
        "|__) |__ /__\\ /   |__",
        "|    |__/    \\\\__ |__"],
        ["  /  \\ /\\_____    .  __    ",
        " / \\/ V__\\ | |__| | |__ | |",
        "/     /\\  \\| |  |_|_\\__ \\_/"],
        [" +--  _____.  __ ",
        "/   | | |  | |__ ",
        "\\__ \\_/ |  | |__ "],
        ["+-- ___ +--| / __ ",
        "|  | | /   |( (   ",
        "|__/_|_\\__ | \\ _) "],
        [" ___  __  ___   /\\   |\\  | |\\  |   /\\  ",
        "|___) | )  |   /__\\  | \\ | | \\ |  /__\\ ",
        "|___) | \\ _|_ /    \\ |  \\| |  \\| /    \\"],
    ]

    global brainEnabled
    brainEnabled = False if arg['wasteful'] else True
    soundOn = True if arg['quiet'] else False

    if not brainEnabled:
        # don't recycle :'c
        init(title='Screensaver',width=Width_,height=Height_,forceSize=True,
             beQuiet=True, sound=soundOn)
    else:
        # be smart :o)
        init(title='Screensaver',width=Width_,height=Height_,forceSize=True,
             beQuiet=True, brain=True,memory=300,sound=soundOn)
    global page; page = Screen()

    try:
        play(4)
    except KeyboardInterrupt:
        dumptrackertofile(savefile,timestamp)
        quit()

