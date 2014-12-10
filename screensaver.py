#!/usr/bin/python3
'''
Somewhat Satisfactory Screensaver by tassaron
Nov 28-Dec 1 2014
'''

from ssass import *
import argparse
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

def giveMessage():
    global msgNum; global messages
    if msgNum==-1:
        page.cell('centre','centre')
        if Debug:
            page.write(' Tassaron\'s Somewhat Satisfactory Debug Mode',\
                    'Prepare For Your Terminal To Break! :O')
        else:
            page.write(' Tassaron\'s Somewhat Satisfactory Screensaver',\
                   'Prepare to be somewhat satisfied! :O')
    else:
        page.area(rows=(11,Height_-11),cols=(17,Width_-17))
        page.fill() # empty out area between the lines
        page.cell('center','center')
        if randomNumber(0,4)==4:
            page.write(messages[msgNum])
        else:
            string=''
            for message in messages:
                if randomNumber(0,50)>20:
                    message = message.split()
                    string+=message[randomNumber(0,len(message)-1)]+' '
            if len(string)<20:
                string+='in my mouth'
            page.write(string)
    page.row(10); page.fill('>')
    page.row(Height_-10); page.fill('<')
    page.column(16); page.fill('^')
    page.column(Width_-16); page.fill('v')
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
        page.area(cols=(rndX,rndX+1),row=rndY)
        for _ in range(25):
            newRndX=randomNumber(1,Width_-2); newRndY=randomNumber(1,Height_-2)
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
    msgNum=randomNumber(0,len(messages)-1)

def getTime():
    global currentTime
    date, time = getTimestamp('tuple')
    currentTime = '%s %s' % (date, time)
    clock = threading.Timer(60.0,getTime)
    clock.start()

def play(totalScreens, screenID=0):
    global tracker; global bigTracker
    global recycled; global flickeryThing

    global currentTime
    getTheTime = threading.Thread(target=getTime,daemon=True)
    getTheTime.start()

    # give introductory message
    giveMessage()

    # screen statistics
    framesCreated=0
    framesDrawn=0
    lastFrameDrawn=0
    maxFrameDrop=speed*3
    message=0
    nextmessage = randomNumber(60,120)
    # default time for a certain animation to play
    # measured in framesDrawn (thus unaffected by speed)
    longevity = 250

    while True:

        i = randomNumber(1,60)
        addBorders()

        # make the flickery things :3
        tracker, bigTracker, recycled = getTrackers()
        # add one because these are incremented after for convenience
        frameTracker = 'drawn_%s___created_%s' % (str(framesDrawn+1),
                        str(framesCreated+1))
        flickeryThing= 'recycled_%s___sum_%s___total_%s' % (str(recycled),
                        str(bigTracker), str(tracker))

        # change positions of flickery things every now and then
        if framesDrawn % 30 == 0:
            topFlickerX = randomNumber(0,Width_-len(flickeryThing))
            bottomFlickerX = randomNumber(0,Width_-len(frameTracker))
            leftFlickerY = randomNumber(0,Height_-len(timestamp))
            rightFlickerY = randomNumber(0,Height_-len(currentTime))

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

        if speed > 1:
            # randomize frame-drops a bit
            halfSpeed = halfOf(speed,rounding='down')
            # fetch number b/t half-of-speed and speed+half
            speed_ = randomNumber(0,speed)
            speed_ += halfSpeed
        else:
            speed_ = speed

        if framesCreated==0 or framesCreated % speed_ == 0 \
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

        if framesDrawn % longevity == 1:
            if screenID == totalScreens:
                screenID = 0
            else:
                screenID += 1

        if screenID==0:
            longevity = 250
            x = randomNumber(1,Width_-2)
            y = randomNumber(1,Height_-2)
            if i == 7 or i == 24 or i == 31:
                # move random area to another random area
                # 1 and -2 to compensate for the borders
                movebg= (' '*30) + letters
                cols, rows = randomArea(10, 10, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                x = randomNumber(1, Width_-2); y = randomNumber(1, Height_-2)
                try:
                    if randomNumber(1,20) < 20:
                        page.move(x=x,y=y,bg=movebg)
                    else:
                        page.move(x=x,y=y)
                except:
                    pass
            elif i == 18 or i == 30:
                # move entire screen in a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                rndX=randomNumber(-6,6)
                rndY=randomNumber(-6,6)
                page.move(x=rndX, y=rndY)
            elif i == 16:
                # draw random rectangle
                cols, rows = randomArea(8, 6, cols=(1,Width_-2), rows=(1, Height_-2))
                # empty the space out
                page.area(cols=cols,rows=rows); page.fill()
                page.area(row=rows[0],cols=cols); page.fill('_')
                page.area(row=rows[1],cols=cols); page.fill('_')
                page.area(col=cols[0],rows=rows); page.fill('|')
                page.area(col=cols[1],rows=rows); page.fill('|')
                page.cell(cols[0],rows[0]); page.write(' ')
                page.cell(cols[1],rows[0]); page.write(' ')
            elif i == 33:
                # draw arrows across somewhere
                row = randomNumber(1,Height_-2)
                page.row(row)
                direction = randomChoice(['>','<','><'])
                page.fill(direction)
            elif i == 15 or i == 17:
                # draw arrows up and down somewhere
                col = randomNumber(1,Width_-2)
                page.column(col)
                direction = randomChoice(['v','^','v^'])
                page.fill(direction)
            elif i==20 or i==48:
                # write random word from a message at random position
                page.cell(x,y)
                msg = messages[randomNumber(0,len(messages)-1)]
                msg = msg.split()
                page.write(msg[randomNumber(0,len(msg)-1)])
            elif i == 44 or i == 43:
                # fill random area with random letters or numbers
                cols, rows = randomArea(10, 10, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                choice = randomChoice([letters,numbers])
                page.fill(choice)
            elif i == 45:
                # skew everything a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                page.skew(randomChoice(['left', 'right']))
            elif i == 35:
                rndNum = randomNumber(0,10)
                if rndNum < 10:
                    spamSmilies(6)
                else:
                    rndX = randomNumber(0,Width_-20)+10
                    rndY = randomNumber(0,Height_-20)+10
                    drawHeart(rndX,rndY)
            elif i == 2 or i == 10 or i == 22:
                # randomly replace sections of numbers with letters
                # or entire screen of numbers with letters. or vice versa
                rndNum = randomNumber(0,10)
                cols, rows = randomArea(20, 20, cols=(1,Width_-2), rows=(1, Height_-2))
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
                    choice = randomChoice([letters, numbers])
                    rndIndex = randomNumber(0,len(choice)-2)
                    rndX=randomNumber(1,Width_-2)
                    rndY=randomNumber(1,Height_-2)
                    page.cell(rndX, rndY)
                    page.write(choice[rndIndex])
            else:
                # draw random portions of words at a random position
                word=''
                for _ in range(2):
                    rndNums=[]
                    for _ in range(2):
                        rndIndex = randomNumber(0,len(words)-1)
                        rndNums.append(randomNumber(1,len(words[rndIndex])-1))
                    rndNums.sort()
                    word += words[rndIndex][rndNums[0]:rndNums[1]]
                page.cell(x,y)
                if rndNums[0] != 2:
                    page.write(word)
                else:
                    page.write(word,direction='down')

            if message == nextmessage:
                giveMessage()
                nextmessage = randomNumber(30,60)
                message=0

        elif screenID==1:
            longevity=100
            x = randomNumber(1, Width_-2)
            y = randomNumber(1, Height_-2)
            if i == 16 or i == 21 or i==25 or i==26:
                # fill random area with random letters or numbers
                cols, rows = randomArea(10, 10, cols=(1,Width_-2), rows=(1, Height_-2))
                page.area(cols=cols,rows=rows)
                choice = randomChoice([letters,numbers])
                page.fill(choice)
            elif i == 17 or i == 19:
                # skew everything a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                page.skew(randomChoice(['left', 'right']))
            elif i == 18 or i == 30 or i == 31 or i == 32 or i == 33:
                # move entire screen left
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                rndX=randomNumber(-10,-1)
                page.move(x=rndX, y=1)
            elif i==22 or i==23 or i==24 or i==48:
                # write random word from a message at random position
                page.cell(x,y)
                msg = messages[randomNumber(0,len(messages)-1)]
                msg = msg.split()
                page.write(msg[randomNumber(0,len(msg)-1)])
            # draw random rectangle
            cols, rows = randomArea(24, 18, cols=(1,Width_-2), rows=(1, Height_-2))
            page.area(cols=cols,rows=rows)
            if i % 4 != 0:
                page.fill() # empty the space
            page.area(row=rows[0],cols=cols); page.fill('_')
            page.area(row=rows[1],cols=cols); page.fill('_')
            page.area(col=cols[0],rows=rows); page.fill('|')
            page.area(col=cols[1],rows=rows); page.fill('|')
            page.cell(cols[0],rows[0]); page.write(' ')
            page.cell(cols[1],rows[0]); page.write(' ')

        elif screenID==2:
            longevity = 20
            x = halfOf(Width_); y = halfOf(Height_)
            if i == 18 or i == 30:
                # move entire screen in a random direction
                page.area(rows=(1,Height_-2),cols=(1,Width_-2))
                rndX=randomNumber(0,13)-6
                rndY=randomNumber(0,13)-6
                page.move(x=rndX, y=rndY)
            else:
                x = halfOf(Width_); y = halfOf(Height_)
                rndX = randomNumber(1,Width_-2)
                choice = randomNumber(0,3)
                page.line((x, y), (rndX, randomChoice([1,Height_-2])))
                if choice == 0 :
                    page.fill(letters)
                elif choice == 1:
                    page.fill(numbers)
                elif choice == 2:
                    if randomNumber(0,40) > 0:
                        word='' # random portion of a word
                        for _ in range(2):
                            rndNums=[]
                            for _ in range(2):
                                rndIndex = randomNumber(0,len(words)-1)
                                rndNums.append(randomNumber(0,\
                                                len(words[rndIndex])-1))
                            rndNums.sort()
                            word.join(words[rndIndex][rndNums[0]:rndNums[1]])
                        page.fill(word)
                    else:
                        page.fill(words)
                elif choice == 3:
                    msg = messages[randomNumber(0,len(messages)-1)]
                    msg = msg.split()
                    page.fill(msg[randomNumber(0,len(msg)-1)])

if __name__=='__main__':
    # because it's fun to see how long I've run this
    savefile = os.getcwd() + '/trackers.dat'
    date, time = getTimestamp('tuple')
    timestamp = '%s %s' % (date, time)

    # parse command line arguments
    fancyline = '#-~-~-~-~-~-~--~-~-~-~-~-~-#'
    parser = argparse.ArgumentParser(prog='screensaver', description=fancyline,
                        epilog=fancyline)
    parser.add_argument('-speed', choices=['snail','slow','fast','faster',
                        'fastest','turbo'], help='# of frames to calculate on \
                        average between frames\n', default='fast')
    parser.add_argument('-size', choices=['classic','big','square','720','tv',
                        'tall'], default='big')
    parser.add_argument('--pause', help='wait for a keypress after every frame',
                        action='store_true')
    parser.add_argument('--debug', help='displays certain technical details',
                        action='store_true')
    arg = vars(parser.parse_args()) # return arguments as a dictionary

    # -speed
    delay=0
    if arg['speed']=='snail':
        speed=1; delay=250
    elif arg['speed']=='slow':
        speed=1
    elif arg['speed']=='fast':
        speed=5
    elif arg['speed']=='faster':
        speed=15
    elif arg['speed']=='fastest':
        speed=30
    elif arg['speed']=='turbo':
        speed=50
    # -size
    if arg['size']=='classic':
        Width_=80; Height_=41
    elif arg['size']=='big':
        Width_=150; Height_=41
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
    if arg['debug']:
        debug(True,'area','line','cell')
        global Debug; Debug=True
    else:
        debug(False)

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
        'what does cat food tastes like?','Harper\'s Little Room','Tarasius is watching']

    # random junk to scribble on the screen
    letters = 'abcdefghijklmnopqrstuvwxyzxxxxxBBBBBBBBBBBBABCDEFGHIJKLNOPQSTUVWXYZ'
    numbers = '371371371371222$%%%@#!@!!@#$&&&&????$$$****#######'
    words=[ 'Brianna','sister','beautiful','symmetrical','patterns','olives',
            'farts','tassaron','love love','Jade Jade','Carliii','Nathanael',
            'dick','dicks','big butts','dancers','cyan','eyeballs','boobs',
            'love love','love love','treadmills','screensaver','funky','laundry',
            'hairballs','kittens','asteroids','dinosaurs','magic','frighten',
            'Tarasius']

    init('Screensaver',width=Width_,height=Height_,forceSize=True,beQuiet=True,
    brain=True,memory=300)
    global page; page = screen()

    try:
        play(1)
    except KeyboardInterrupt:
        dumptrackertofile(savefile,timestamp)
        quit()

