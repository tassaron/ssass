#!/usr/bin/python3
''' Test Program by tassaron '''
import tass
# start reading at main (the last section)

def construct(page, *keywords):
    screen = tass.screenInit()

    if page=='mainmenu':
        #draw borders
        tass.screenFill(screen, 'col 0', 'col '+str(width-1), 'row 0',\
        'row '+str(height-1), 'with #')
        # could be more readable if you used multiple lines, it's up to you
        tass.screenAnnounceArea(-1,3) # start announcing at x=centre, y=3
        tass.screenAnnounce(screen, 'Tassaron\'s Somewhat Satisfactory Screen Simplifier',\
        'Prepare to be Somewhat Satisfied', 2)
        tass.screenAnnounce(screen, 3, '1) Demonstrate Everything',\
        '2) Screensaver','3) Walk Around','4) Toggle Borders','5) Test Canvas',\
        '6) Melt Down',2,'9) Quit')
        tass.screenWrite(screen,11,height-5,'Wowzer~!')
        # personally I like passing a few lines at once
        # We haven't drawn the main menu, just created it in memory.


    elif page=='goodbye':
        tass.screenAnnounceArea(-1,8)
        tass.screenAnnounce(screen, 'See ya later alligator.',1, 'Press R to replay.')
        tass.screenAnnounce(screen, 'B goes back to the main menu')
        # Still haven't drawn anything


    elif page=='demo':
        tass.screenAnnounceArea() #reset
        tass.screenAnnounce(screen, 6, "Enter some things.")
        tass.screenDraw(screen)
        # we draw the screen with that text...
        tass.screenAnnounce(screen, 7, "Enter more things :O")
        # and prepare this, but don't draw it yet
        announcements = []
        totalannouncements=0
        # we do this 15 times to get 15 announcements from the user
        while totalannouncements<15:
            # after 4 announcements, start counting down how many more to enter
            if totalannouncements>4:
                tass.screenAnnounceArea()
                tass.screenAnnounce(screen, 9, 'Enter ' + str(14-totalannouncements) + \
                ' more things...')
            # after 8, obviously...
            if totalannouncements>8:
                tass.screenAnnounce(screen, 2, 'Your things are in a list',\
                'with a limited length!')
            # get character input from the user
            ch = tass.getInput('type char')
            # set the announcements area to the corner
            tass.screenAnnounceArea(1,18)
            # only show five announcements at a time
            if len(announcements)<5:
                announcements.append(ch)
            else:
                # ripple append limits the list to the current length by pushing
                # everything one index back before adding a new item
                announcements = tass.rippleAppend(announcements,ch)
            for announcement in announcements:
                tass.screenAnnounce(screen, announcement)
            totalannouncements+=1
            tass.screenDraw(screen)
            # then leave and do the next part in do()

    # CONSTRUCT DEMO2
    elif page=='demo2':
        tass.screenAnnounceArea(-1,8)
        tass.screenAnnounce(screen,'Uhhhhhhhh','i havent done anything else')

    # CONSTRUCT CANVAS
    elif page=='canvas':
        tass.screenAnnounceArea()
        tass.screenAnnounce(screen,'type something to be evaluated',\
        'write(screen,x,y,"message","message",etc)',\
        'anything that starts with tass.screen','type \'quit\' to leave')


    do(page, screen, keywords)

def do(page, screen, *keywords):
    global width; global height; global x; global y
    global crosshairs; global firsttimewalking; global borders

    if page=='mainmenu':
        tass.screenDraw(screen)
        ch = tass.getInput('type int','valid 1 2 3 4 5 6 9')
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
                tass.screenFill(screen, 'col 0', 'col '+str(width-1), 'row 0',\
                'row '+str(height-1)) #clear borders
            else:
                borders=True
                tass.screenFill(screen, 'col 0', 'col '+str(width-1), 'row 0',\
                'row '+str(height-1), 'with #')
            do('mainmenu',screen)
        elif ch==5:
            construct('canvas')
        elif ch==6:
            # iterate as many times as there are rows
            for i in range(height):
                '''
                # iterate over the rows of the screen
                for y in tass.reverseRange(height-2):
                    # move each row one row down
                    tass.screenRowMove(screen, y, y+1) #move each row one row down
                '''
                # move entire screen, starting at the row we're on, down by 1
                tass.screenAreaMove(screen,cols=(0,width),rows=(i,height),y=i+1)
                if not tass.screenDraw(screen):
                    construct('mainmenu')
                if not tass.sleep():
                    construct('mainmenu')
            # once done animating, show the last screen
            do('transition',screen)
        elif ch==9:
            construct('goodbye')
        # dan's gonna say I found a way to use goto in Python


    elif page=='demo':
        screen = tass.screenInit()
        tass.screenAnnounceArea()
        tass.screenAnnounce(screen, 17, 'What do you think?', '1) It was good',\
        '2) Back to mainmenu', '3) Quit now!','9) I want to see more')
        tass.screenDraw(screen)
        ch = tass.getInput('type int','valid 1 2 3 9')
        if ch==1:
            snapshot = tass.takeSnapshot(screen)
            tass.screenFill(screen) #clear
            tass.screenAnnounce(screen,'thanks')
            tass.screenDraw(screen)
            tass.pause()
            do('demo',snapshot)
        elif ch==2:
            construct('mainmenu')
        elif ch==3:
            construct('goodbye')
        elif ch==9:
            construct('demo2')


    elif page=='demo2':
        tass.screenDraw(screen)
        tass.pause()
        construct('mainmenu')

    elif page=='screensaver':
        words = ['poo','fart','smell','bark','lol']
        tass.screenAnnounceArea() # reset to centre top
        tass.screenAnnounce(screen,'It\'ll stop on its own',\
        'but you can use ctrl+c to stop it manually')
        ch = tass.randomNumber(100,200)
        for i in range(ch):
            message = tass.randomChoice(words)
            x = tass.randomNumber(0,width-1)
            y = tass.randomNumber(0,height-1)
            tass.screenWrite(screen, x, y, message)
            # write frame number in the corner
            frame = str(i)+'/'+str(ch)
            tass.screenWrite(screen, (width-len(frame)), height-1,frame)
            # these return false if the user interrupts them
            if not tass.screenDraw(screen):
                construct('mainmenu')
            if not tass.sleep(150):
                construct('mainmenu')
        construct('mainmenu')


    elif page=='goodbye':
        tass.screenDraw(screen)
        ch = tass.getInput('type char')
        if ch=='r':
            tass.replay()
            tass.pause()
        elif ch=='b':
            construct('mainmenu')
        else:
            tass.quit()


    elif page=='walk':
        # fill screen with dots
        tass.screenFill(screen,'with .')
        if crosshairs:
            # empty row and col with player
            tass.screenFill(screen,'col '+str(x),'row '+str(y))
        if firsttimewalking:
            x=tass.halfOf(width)
            y=tass.halfOf(height)
            tass.screenAnnounceArea()
            tass.screenAnnounce(screen, 2,'use ASWD to move around',\
            'C for crosshairs',10,'B to go back')
            firsttimewalking=False
        # draw player at x and y
        tass.screenWrite(screen,x,y,'@')
        # actually draw the screen
        tass.screenDraw(screen)
        ch = tass.getInput('type char','valid a w s d c b')
        if ch=='a':   # left
            if x>0:
                tass.screenCellMove(screen, x,y,x-1,y)
                x-=1
        elif ch=='w': # up
            if y>0:
                tass.screenCellMove(screen, x,y,x,y-1)
                y-=1
        elif ch=='s': # down
            if y<height-1:
                tass.screenCellMove(screen, x,y,x,y+1)
                y+=1
        elif ch=='d': # right
            if x<width-1:
                tass.screenCellMove(screen, x,y,x+1,y)
                x+=1
        elif ch=='b': # GO BACK
            construct('mainmenu')
        elif ch=='c': # crosshairs
            if crosshairs:
                crosshairs=False
            else:
                crosshairs=True
        # we can skip the constructor this time
        do('walk',screen)
        # this way we overwrite the walk screen instead of making tons of them


    elif page=='canvas':
        tass.screenDraw(screen)
        ch = tass.getStringInput()
        if ch=="quit":
            construct('mainmenu')
        copy = ch
        ch = 'tass.screen'+tass.capitalize(copy)
        eval(ch)
        do('canvas',screen)


    elif page=='transition':
        # the screen will slowly scroll downwards, and then...
        tass.screenFill(screen) # clear the screen
        tass.screenWrite(screen,-1,-1,'Press any key to reset.')
        tass.screenDraw(screen) # draw the empty screen
        tass.pause() # lol ;)
        construct('mainmenu')


if __name__ == '__main__':
    # initialize program
    global width; global height
    width = 79; height = 40
    tass.init('Somewhat Satisfactory Screen Simplifier Demo', width, height, 'screen')

    # a wild ride
    global borders; borders=True
    construct('mainmenu')
