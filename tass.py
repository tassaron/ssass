#!/usr/bin/python3
'''

Tassaron's Library of Useful Functions
+ Cross-Platform Terminal ASCII Screen Drawing
by tassaron - 2013-14

'''

import random
import sys
import os
import time
import math
from subprocess import call

if os.name!='nt':
    import tty
    import termios
else:
    import msvcrt

# stops user from barfing on the screen while things are being drawn
# only relevant in not-Windows
class PreventBarfing:
    def __enter__(self):
        if os.name!='nt':
            global stdinfd; global oldtcattr
            oldtcattr = termios.tcgetattr(stdinfd)
            newtcattr = oldtcattr[:]
            newtcattr[3] = newtcattr[3] & ~termios.ECHO
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, newtcattr)
        else:
            barf = True
    def __exit__(self, typ, value, callback):
        if os.name!='nt':
            global stdinfd; global oldtcattr
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
        else:
            barf = False # there we go, barfing stopped! :)

# returns single-character input
def anykey(*messages):
    # windows version
    if os.name == 'nt':
        for message in messages:
            print(message)

        from msvcrt import getch
        # getch returns b'[character]', so we turn it into a string
        # and strip out the b' and ' parts
        char = getch()
        # some inputs need to be compared using their number, for some reason
        if ord(char) == 224:
            # aha! an arrow key!
            char = ord(getch())
            if char == 72:
                char = 'up' # up
            elif char == 80:
                char = 'down' # down
            elif char == 75:
                char = 'left' # left
            elif char == 77:
                char = 'right' # right
        elif ord(char) == 3:
            char = 'q' # KeyboardInterrupt
        elif ord(char) == 27:
            char = 'p' # Esc
        elif ord(char) == 8:
            char = '\x7F' # backspace
        elif ord(char) == 18:
            char = '\x12' # ctrl-R
        else:
            char = str(char)[2:-1]
        if char == 'q':
            quit()
        return char.lower()
    else:
        # not-Windows version
        global busy
        while not busy:
            busy=True
            global stdinfd
            for message in messages:
                print(message)
            try:
                oldtcattr = termios.tcgetattr(stdinfd)
                # set the input mode of stdin so that it gets added to
                # char by char rather than line by line
                tty.setraw(stdinfd)
                # read 1 byte from stdin (indicating that a key has been pressed)
                char = sys.stdin.read(1)
            finally:
                # reset
                termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
            if char == 'q' or char == '\x03':
                quit()
            '''
            elif char == '\x08' or char == '\x7F':
                backspace should do history but it doesn't for now
            '''
            sys.stdout.flush()
            busy=False
            return char.lower() # ignore caps lock

    def tcflush():
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

# initialized a new program -- sets up global variables etc
def init(*keywords):
    # interpret initialization keywords
    global cols; global rows
    for keyword in keywords:
        if keyword.startswith('title='):
            # get program title
            title = keyword.split('=')
            title = title[1]
            if os.name == 'nt':
                call('title '+title,shell=True)
        elif keyword=='screen':
            # initialize stuff we need for the screen
            global screens; screens=[]
            screenAnnounceArea() # sets area to centre
        elif keyword.startswith('size '):
            # get custom screen size in the format 'size cols rows'
            size = keyword.split(' ')
            cols = int(size[1])
            rows = int(size[2])
            if os.name == 'nt':
                # set Windows terminal to the correct size
                call('mode con: cols='+str(cols+1)+' lines='+str(rows+1),shell=True)

    # settings that everyone needs
    def defineSettings():
        global cwd
        cwd = os.getcwd() + '/'
        savefile =  cwd + title + '_save.dat'
        global busy; busy=False
        # store stdin's file descriptor
        global stdinfd
        stdinfd = sys.stdin.fileno()
        global history; history=[]

    # used by chunderEverywhere(), the error caller
    def constructErrorDb():
        global errors
        errors={'UnknownError' : 'Unknown error D:',
                'MetaError' : 'An error was called with an incorrect name.',
                'NotPercentages' : 'Percentages do not add up to 100.',
                'UnspecifiedScreenEvent' : 'Screen event not specified.',
                'ScreenNotInitialized' : 'Screen event specified before initializing screen.',
                'InvalidScreenID' : 'The screen ID specified is not valid.',
                'InvalidXY' : 'X and/or Y coords specified are outside row/col limits.'
                }

    defineSettings()
    constructErrorDb()

# stops until the user presses a key
def pause():
    anykey()

# returns a single-character input from the user which can be a string or an int
# input = getInput('type int')  input = getInput('type char')
# can also force to wait for a valid input
# input = getInput('valid a b c')
def getInput(*keywords):
    ch='>'
    global busy
    while not busy:
        valids=None; inputtype='char'
        for keyword in keywords:
            if keyword=='noisy':
                busy=True
                sys.stdout.write(ch)
                busy=False
            elif keyword.startswith('valid '):
                valids = keyword.split(' ')
            elif keyword.startswith('type '):
                inputtype = keyword.split(' ')
                inputtype = inputtype[1]
        if valids:
            while ch not in valids:
                ch = anykey()
        else:
            ch = anykey()
        if inputtype=='int':
            return int(ch)
        else:
            return ch

# returns a string from the user
def getStringInput(message=None):
    if message:
        write(message+' ',0)
    choice='tinkle'
    while choice=='tinkle':
        try:
            choice = input()
        except KeyboardInterrupt:
            quit()
    return choice.strip()

# safely exit the program
def quit():
    if os.name!='nt':
        # return terminal to the way it was
        global oldtcattr; global stdinfd
        termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
    raise SystemExit

# a serious error occured!
def chunderEverywhere(err='UnknownError'):
    global errors
    clear()
    if err not in errors.keys():
        err = 'MetaError'
    string = errors[err]
    newstring=''
    for character in string:
        if randomNumber()==1:
            character.upper()
        newstring+=character
    write(newstring)
    #print(errors[err], file=errfile)
    quit()

# clears the display
def clear():
    if os.name == 'nt':
        call('cls',shell=True)
    else:
        call("clear",shell=True)

def save(values, savefile, label='saved'):
    try:
        with open(savefile, 'w', encoding='utf-8') as savefile:
            for package in values:
                package = package.strip()
                try:
                    val1, val2 = package.split()
                    try:
                        val1 = int(val1)
                    except TypeError:
                        val1 = val1.strip()
                    try:
                        val2 = int(val2)
                    except TypeError:
                        val2 = val2.strip()
                except ValueError:
                    val1 = package
                    val2 = 'True'
                print(label + ':')
                print("%s=%s" % (val1, val2), file=savefile)
    except IOError:
        print("error saving data :(")
        quit()

def load(savefile, label='saved'):
    try:
        global names
        names = {}
        with open(savefile, 'r', encoding='utf-8') as savefile:
            for line in savefile:
                line = line.strip()
                key, value = line.split('=')
                key = key.strip(); value = value.strip()
                names[key] = value

    except:
        # if save.dat is corrupt, invalid, or nonexistent, recreate it
        save(savefile)

def reverseRange(number):
    return range(number,-1,-1)

# does everything
def randomNumber(lower=0, upper=1):
    return random.randint(lower,upper)

# choose one choice from a list of options
def randomChoice(choices=['dog','cat']):
    index = randomNumber(0,len(choices)-1)
    return choices[index]

# halve a number without getting a float
def halfOf(number):
    number = number/2
    number = math.floor(number)
    return int(number)

# lazy print function. end is # of linebreaks. align is left, centre, right
# not to be confused with screenWrite, which is for the screen
def write(line, end=1, align='left'):
    global busy
    while not busy:
        busy=True
        global cols
        if align=='centre' or align=='center':
            spaces = (cols-len(line))/2
            spaces=math.floor(spaces)
        if align=='right':
            spaces = cols-len(line)
        if align!='left':
            sys.stdout.write(" "*spaces)
        sys.stdout.write(line)
        if align=='centre' or align=='center':
            sys.stdout.write(" "*spaces)
        if align!='left':
            # right & centre need a newline after
            sys.stdout.write("\n")
            if end>0: # it still counts as 1
                end-=1 # more intuitive this way
        while end>0:
            sys.stdout.write("\n")
            end-=1
    busy=False

# splits a list into pages and returns a list of pages
def paginate():
    pointless=True

# creates a new screen, adds it to the global list, and returns the identifier
def screenInit():
    global screens
    # the screen is a list
    screen=[]
    global rows
    # add as many rows as the height of the screen
    for _ in range(rows):
        # the row is a list too
        row=[]
        for _ in range(cols):
            # add as many cells to the row as the width of the screen
            row.append(' ')
        # add the row to the screen
        screen.append(row)
    # add the screen to the global list of screens
    screens.append(screen)
    # return the screen identifier
    return screens.index(screen)

# returns the character at position x,y
def screenPos(screenID, x,y):
    pointless=True

# returns the screen located at screenID
def takeSnapshot(screenID):
    global screens
    return screens[screenID]

# overwrites screen at screenID with local screen provided
def copySnapshotInto(screenID, snapshot):
    global screens
    screens[screenID] = snapshot

# replays all screens with a certain delay between each, for testing purposes
def replay(delay=1000, showID=True):
    global screens
    for screen in screens:
        screenID = screens.index(screen)
        if showID:
            message = 'ID: '+str(screenID)
            #clipboard = screenSelect('x 0-'+str(len(message)),'y 0-0')
            snapshot = takeSnapshot(screenID)
            screenWrite(screenID,0,0,message)
            screenDraw(screenID)
            copySnapshotInto(screenID, snapshot)
            #screenWrite(screenID,0,0,clipboard)
        else:
            screenDraw(screenID)
        if delay>0:
            if not sleep(delay):
                quit()
        else:
            pause()
    global rows # bottom middle
    screenAnnounceArea(-1,rows-1)
    screenAnnounce(screenID, 'Done.')
    screenDraw(screenID)
    quit()

# write messages to the screen, starting at x, y
# each subsequent message will drop a line
def screenWrite(screenID, x, y, *messages):
    global cols; global rows
    global screens
    for message in messages:
        if type(message)=='int':
            y+=message
        else:
            if x > cols or y > rows:
                chunderEverywhere('InvalidXY')
            if x < 0:
                x = halfOf(cols-len(message))
            if y < 0:
                y = halfOf(rows)
            screen = screens[screenID]
            row = screen[y]
            for i in range(len(message)):
                try:
                    row[x+i]=message[i]
                except IndexError:
                    continue
            screen[y] = row
            screens[screenID] = screen
            y+=1

# draw the screen at screenID
def screenDraw(screenID, disableHistory=False):
    global screens
    screen = screens[screenID]
    global busy
    while not busy:
        busy=True
        # don't let the user barf
        with PreventBarfing():
            for row in screen:
                for cell in row:
                        # write each cell in each row
                        sys.stdout.write(cell)
                # write a linebreak after every row
                sys.stdout.write('\n')
                sys.stdout.flush()
    busy=False
    global announceY; announceY=1
    global history
    if not disableHistory:
        history.append(screenID)

# fill the whole screen or certain rows or columns with certain characters
# screenFill(screenID, 'col 50', 'col 40', 'row 30', 'with $')
# ^- would fill columns 50 and 40, and row 30 with the character $
# screenFill(screenID) <-- clears the entire screen
def screenFill(screenID, *keywords):
    global screens
    screen = screens[screenID]
    fillcols=[]
    fillrows=[]
    ch=' '
    characters=[]
    for keyword in keywords:
        _, *values = keyword.split(' ')
        if keyword.startswith('col ') or keyword.startswith('row '):
            value = int(values[0])
            if keyword.startswith('col '):
                fillcols.append(value)
            elif keyword.startswith('row '):
                fillrows.append(value)
        elif keyword.startswith('with '):
            ch = randomChoice(values)

    # filling column(s)
    if len(fillcols)>0:
        for fillcol in fillcols:
            # iterate through rows; fill certain cells
            for row in screen:
                row[fillcol] = ch
    # filling row(s)
    if len(fillrows)>0:
        for fillrow in fillrows:
            row = screen[fillrow]
            # iterate over cells in row; fill them
            for i in range(len(row)):
                row[i]=ch
    # fill everything
    if len(fillrows)+len(fillcols)==0:
        for row in screen:
            for i in range(cols):
                row[i] = ch

# move the cell at oldx,oldy to newx,newy, replacing old with bg
def screenCellMove(screenID, oldx,oldy,newx,newy, bg=' '):
    global screens
    screen = screens[screenID]
    row = screen[oldy]
    copy = row[oldx]
    row[oldx]=bg
    row = screen[newy]
    row[newx]=copy

# move specified row to newrow, replacing with bg
def screenRowMove(screenID, row, newrow, bg=' '):
    global screens
    screen = screens[screenID]
    row = screen[row]
    newrow = screen[newrow]
    # set new row to the old row
    for cell in range(len(newrow)):
        newrow[cell]=row[cell]
    # iterate over cells in the old row
    for cell in range(len(row)):
        # set each cell to bg
        row[cell]=bg

# move specified col to newcol, replacing with bg
def screenColMove(screenID, col, newcol, bg=' '):
    global screens
    screen = screens[screenID]
    # old column is a list
    oldcol=[]
    # run through the screen collecting contents of old column (old cells)
    # and replacing old cells with bg
    for row in screen:
        for cell in range(len(row)):
            # cell is the index of the cell, not the contents
            if cell==col:
                oldcol.append(cell)
                row[cell]=bg
    # run through the screen setting new cell to its corresponding old cell
    for row in screen:
        for cell in range(len(row)):
            if cell==newcol:
                row[cell]=oldcol[cell]

# moves a certain area of the screen
# screenMove(screenID, 'cols=0-10', 'rows=0-10', 'x 6', 'y 6', 'bg=#')
# ^-- moves a 10x10 area starting at 0x0 to start at 6x6
# replaces any non-overlapping cells with bg or spaces if none
# logically this should all be in a super screenMove() but I'm lazy right now
def screenAreaMove(screenID, *keywords):
    pointless=True

# similar to screenWrite except it remembers where to write and automatically
# drops a line every time it's called, until the area is reset manually
def screenAnnounce(screenID, *messages):
    global announceY; global announceX
    for message in messages:
        if type(message)==int:
            announceY+=message
        else:
            screenWrite(screenID, announceX, announceY, message)
        global rows
        if announceY < rows-1:
            announceY+=1

def screenAnnounceArea(x=-1, y=1):
    global announceX; global announceY
    announceX=x; announceY=y;

# pauses for a certain amount of time without asking for user input
# returns False if the user interrupts it forcefully
def sleep(length=75):
    if length<75:
        length=75
    # time.sleep uses seconds. let's use milliseconds
    length=length/1000

    global busy
    while not busy:
        busy=True
        try:
            # janitors required!
            with PreventBarfing():
                time.sleep(length)
        except KeyboardInterrupt:
            busy=False
            return False
    busy=False
    return True

# keeps list the same length by deleting first item, sliding each item 1 index
# back, and adding your new item to the end
def rippleAppend(theList, newItem):
    # set each item equal to the item 1 index ahead
    for i in range(len(theList)):
        try:
            theList[i]=theList[i+1]
        except IndexError:
            # when there's no more indexes ahead, append our new item
            theList.append(newItem)
    return theList

if __name__=='__main__':
    init("Tassaron's Library", True)
    write("Pretty soon this'll make some folders for me.", 2, 'center')
    pause()
