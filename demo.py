#!/usr/bin/python3
''' Demo Program for SSASS by tassaron '''

from ssass import *

Width_ = 80; Height_ = 41

def makeBorders(ch):
    construction.column(0); construction.fill(ch)
    construction.column(Width_); construction.fill(ch)
    construction.row(0); construction.fill(ch)
    construction.row(Height_); construction.fill(ch)

def construct(page, *keywords):
    construction = screen()

    if page=='mainmenu':
        #draw borders
        construction.column(0); construction.fill('#')
        construction.row(0); construction.fill('#')
        construction.column(Width_); construction.fill('#')
        construction.row(Height_); construction.fill('#')

        # start announcing at x=centre, y=3
        construction.setAnnouncementArea('centre',3)
        construction.announce('Tassaron\'s Somewhat Satisfactory Screen Simplifier',\
        'Prepare to be Somewhat Satisfied', 2)
        construction.announce(3, '1) Demonstrate Everything',\
        '2) Constructionsaver','3) Walk Around','4) Toggle Borders','5) Test Canvas',\
        '6) Melt Down','7) Show Axis Labels',1,'9) Quit')
        construction.cell(11,Height_-5); construction.write('Wowzer~!')
        # We haven't drawn the main menu, just created it in memory.


    elif page=='goodbye':
        construction.setAnnouncementArea('centre',8)
        construction.announce('See ya later alligator.',1, 'Press R to replay.')
        construction.announce('B goes back to the main menu')
        # Still haven't drawn anything


    elif page=='demo':
        construction.setAnnouncementArea() #reset
        construction.announce(6, "Enter some things.")
        construction.paint()
        # we draw the construction with that text...
        construction.announce(7, "Enter more things :O")
        # and prepare this, but don't draw it yet
        announcements = []
        totalannouncements=0
        # we do this 15 times to get 15 announcements from the user
        while totalannouncements<15:
            # after 4 announcements, start counting down how many more to enter
            if totalannouncements>4:
                construction.setAnnouncementArea()
                construction.announce(9, 'Enter ' + str(14-totalannouncements) + \
                ' more things...')
            # after 8, obviously...
            if totalannouncements>8:
                construction.announce(2, 'Your things are in a list',\
                'with a limited length!')
            # get character input from the user
            ch = getInput('type char')
            # set the announcements area to the corner
            construction.setAnnouncementArea(1,18)
            # only show five announcements at a time
            if len(announcements)<5:
                announcements.append(ch)
            else:
                # ripple append limits the list to the current length by pushing
                # everything one index back before adding a new item
                announcements = rippleAppend(announcements,ch)
            for announcement in announcements:
                construction.announce(announcement)
            totalannouncements+=1
            construction.paint()
            # then leave and do the next part in do()

    # CONSTRUCT DEMO2
    elif page=='demo2':
        construction.setAnnouncementArea('centre',8)
        construction.announce('Uhhhhhhhh','i havent done anything else')

    # CONSTRUCT CANVAS
    elif page=='canvas':
        construction.setAnnouncementArea()
        construction.announce('type something to be evaluated',\
        'write("message","message",etc)',\
        'anything that starts with construction.','type \'quit\' to leave')


    do(page, construction, keywords)

def do(page, construction, *keywords):
    global x; global y
    global crosshairs; global firsttimewalking; global borders

    if page=='mainmenu':
        construction.paint()
        ch = getInput('type int','valid 1 2 3 4 5 6 7 9')
        # check input
        if ch==1:
            construct('demo')
        elif ch==2:
            construct('screensaver')
        elif ch==3:
            x=1; y=1; crosshairs=False; firsttimewalking=True
            construct('walk')
        elif ch==4:
            if borders:
                borders=False
                # clear the borders
                makeBorders(' ')
            else:
                borders=True
                makeBorders('#')
            do('mainmenu',construction)
        elif ch==5:
            construct('canvas')
        elif ch==6:
            # iterate as many times as there are rows
            for i in range(Height_):
                # move entire screen, starting at the row we're on, down by 1
                construction.area(cols=(0,Width_),rows=(i,Height_))
                construction.move(x=0,y=i+1)
                if not construction.paint():
                    construct('mainmenu')
                if not sleep():
                    construct('mainmenu')
            # once done animating, show the last screen
            do('transition',construction)
        elif ch==7:
            construction.showAxisLabels()
            pause() # ehhh
            do('mainmenu',construction)
        elif ch==9:
            construct('goodbye')
        # dan's gonna say I found a way to use goto in Python


    elif page=='demo':
        construction = screen()
        construction.setAnnouncementArea()
        construction.announce(17, 'What do you think?', '1) It was good',\
        '2) Back to mainmenu', '3) Quit now!','9) I want to see more')
        construction.paint()
        ch = getInput('type int','valid 1 2 3 9')
        if ch==1:
            snapshot = construction.takeSnapshot()
            construction.everything(); construction.fill() #clear
            construction.announce('thanks')
            construction.paint()
            pause()
            do('demo',snapshot)
        elif ch==2:
            construct('mainmenu')
        elif ch==3:
            construct('goodbye')
        elif ch==9:
            construct('demo2')


    elif page=='demo2':
        construction.paint()
        pause()
        construct('mainmenu')

    elif page=='screensaver':
        words = ['poo','fart','smell','bark','lol']
        construction.setAnnouncementArea() # reset to centre top
        construction.announce('It\'ll stop on its own',\
        'but you can use ctrl+c to stop it manually')
        ch = randomNumber(100,200)
        for i in range(ch):
            message = randomChoice(words)
            x = randomNumber(0,Width_-1)
            y = randomNumber(0,Height_-1)
            construction.cell(x, y); construction.write(message)
            # write frame number in the corner
            frame = str(i)+'/'+str(ch)
            construction.cell((Width_-len(frame)-1), Height_-1); construction.write(frame)
            # these return false if the user interrupts them
            if not construction.paint():
                construct('mainmenu')
            if not sleep(150):
                construct('mainmenu')
        construct('mainmenu')


    elif page=='goodbye':
        construction.paint()
        ch = getInput('type char')
        if ch=='r':
            replay()
            pause()
        elif ch=='b':
            construct('mainmenu')
        else:
            tass.quit()


    elif page=='walk':
        # fill screen with dots
        construction.everything(); construction.fill('.')
        if crosshairs:
            # empty row and col with player
            construction.column(x); construction.fill()
            construction.row(y); construction.fill()
        if firsttimewalking:
            x=halfOf(Width_)
            y=halfOf(Height_)
            construction.setAnnouncementArea()
            construction.announce(2,'use ASWD to move around',\
            'C for crosshairs',10,'B to go back')
            firsttimewalking=False
        # draw player at x and y
        construction.cell(x,y); construction.write('@')
        # actually draw the construction
        construction.paint()
        ch = getInput('type char','valid a w s d c b')
        if ch=='a':   # left
            if x>0:
                construction.cell(x,y); construction.move(x-1,y)
                x-=1
        elif ch=='w': # up
            if y>0:
                construction.cell(x,y); construction.move(x,y-1)
                y-=1
        elif ch=='s': # down
            if y<Height_-1:
                construction.cell(x,y); construction.move(x,y+1)
                y+=1
        elif ch=='d': # right
            if x<Width_-1:
                construction.cell(x,y); construction.move(x+1,y)
                x+=1
        elif ch=='b': # GO BACK
            construct('mainmenu')
        elif ch=='c': # crosshairs
            if crosshairs:
                crosshairs=False
            else:
                crosshairs=True
        # we can skip the constructor this time
        do('walk',construction)
        # this way we overwrite the walk screen instead of making tons of them


    elif page=='canvas':
        construction.paint()
        ch = getStringInput()
        if ch=="quit":
            construct('mainmenu')
        copy = ch
        ch = 'construction.'+copy
        eval(ch)
        do('canvas',construction)


    elif page=='transition':
        # the screen will slowly scroll downwards, and then...
        construction.everything(); construction.fill() # clear the construction
        construction.cell('centre','centre'); construction.write('Press any key to reset.')
        construction.paint() # draw the empty construction
        pause() # lol ;)
        construct('mainmenu')


if __name__ == '__main__':
    # initialize program
    init('Somewhat Satisfactory ASCII Screen Simplifier Demo', width=Width_,\
        height=Height_,forceSize=True,beQuiet=True)

    # a wild ride
    global borders; borders=True
    construct('mainmenu')
