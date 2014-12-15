#!/usr/bin/python3

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#
#                               nate.py
#                A Bouncy Screensaver with Someone's Name
#                       an experiment by tassaron
#                         written Dec 13, 2014
#
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

from ssass import *

def main():

    nate1 = "|\  |  /\  _____  ____"
    nate2 = "| \ | /__\   |   |___"
    nate3 = "|  \|/    \  |   |____"
    widthOfObject = len(nate2)

    date, time = getTimestamp('tuple')
    timeStarted = '%s_%s' % (date, time)
    global currentTime
    startDaemonThread(getTime)

    framesCreated=0
    framesDrawn=0
    randomCharacters = '-~~*' * 8
    randomCharacters+=' '*60

    # create the main screen
    page = Screen()

    # bouncing nate
    x = halfOf(Width_ - widthOfObject)
    y = halfOf(Height_-1)
    direction = randomChoice(['ne','nw','se','sw'])

    rainy = 0

    rightBorder = Width_-1; leftBorder = 1
    bottomBorder = Height_-1; topBorder = 1

    while True:
        if rainy==0:
            rainy = Height_-2 # start positions of rain
            rainx = [randomNumber(10,Width_-10) for i in range(12)]

        for rx in rainx:
            choice = randomChoice(randomCharacters)
            page.cell(rx, rainy); page.write(' ')
            page.cell(rx, rainy-2); page.write(choice)
        rainy-=1

        # draw randomized background
        i = randomNumber(1,10)

        if i > 8:
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

        # draw ascii art at x and y
        page.cell(x,y)
        page.write(nate1,nate2,nate3)
        page.area(cols=(x, x+widthOfObject), rows=(y, y+2))

        # determine bounce and direction
        if direction == 'ne': # up right
            if x+widthOfObject >= rightBorder and y >= topBorder:
                direction = 'nw'
            elif x+widthOfObject <= rightBorder and y <= topBorder:
                direction = 'se'
            elif x+widthOfObject >= rightBorder and y <= topBorder:
                direction = 'sw'
        elif direction == 'nw': # up left
            if x <= leftBorder and y >= topBorder:
                direction = 'ne'
            elif x >= leftBorder and y <= topBorder:
                direction = 'sw'
            elif x <= leftBorder and y <= topBorder:
                direction = 'se'
        elif direction == 'se': # down right
            if x+widthOfObject <= rightBorder and y+3 >= bottomBorder:
                direction = 'ne'
            elif x+widthOfObject >= rightBorder and y+3 <= bottomBorder:
                direction = 'sw'
            elif x+widthOfObject >= rightBorder and y+3 >= bottomBorder:
                direction = 'nw'
        elif direction == 'sw': # down left
            if x >= leftBorder and y+3 >= bottomBorder:
                direction = 'nw'
            elif x <= leftBorder and y+3 >= bottomBorder:
                direction = 'ne'
            elif x <= leftBorder and y+3 <= bottomBorder:
                direction = 'se'

        # change x and y
        if direction == 'ne': # up right
            x+=1; y-=1
        elif direction == 'nw': # up left
            x-=1; y-=1
        elif direction == 'se': # down right
            x+=1; y+=1
        elif direction == 'sw': # down left
            x-=1; y+=1

        page.move(x=x,y=y,bg=randomCharacters)

        framesCreated+=1
        if framesCreated % 2 == 0:
            page.addBorders()
            if not page.paint():
                quit()
            if not sleep():
                quit()
                framesDrawn+=1

def getTime():
    global currentTime
    date, time = getTimestamp('tuple')
    currentTime = '%s_%s' % (date, time)
    startTimer(60, getTime)


if __name__=='__main__':

    Width_ = 150
    if currentOS() == 'nt':
        Height_=51
    else:
        Height_=41

    init("Nate's Screensaver",width=Width_,height=Height_,forceSize=True,beQuiet=True)

    try:
        main()
    except KeyboardInterrupt:
        quit()
