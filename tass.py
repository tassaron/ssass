#!/usr/bin/python3
'''

Tassaron's Somewhat Satisfactory Script Simplifier
+ Somewhat Satisfactory ASCII Screen Simplifier
written Nov-Dec 2014

'''

# stuff prefixed by IDEAL: is what I want to get around to doing later

import sys
import os
import time
import math
import random
from subprocess import call
from copy import deepcopy

# import different things depending on OS, and set a constant for later use
if os.name=='nt':
    _OSenv = 'nt'
    import msvcrt
else:
    _OSenv = 'other'
    import tty
    import termios

# initializes a new program (mandatory)
def init(title='Defaultline Tittle',**keyword):
    global Width_; Width_=80
    global Height_; Height_=40
    global busy; busy=False
    global Bottom; Bottom=Height_-1
    global Right; Right=Width_-1

    # give cmd the correct title
    if _OSenv=='nt':
        call('title '+title,shell=True)

    # settings that everyone needs
    def defineSettings():
        global cwd
        cwd = os.getcwd() + '/'
        savefile =  cwd + title + '_save.dat'
        errfile = cwd + title + '_error.log'
        global busy; busy=False
        if _OSenv!='nt':
            # store stdin's file descriptor
            global stdinfd
            stdinfd = sys.stdin.fileno()
            global oldtcattr
            oldtcattr = termios.tcgetattr(stdinfd)

    # used by chunderEverywhere(), the error caller
    # IDEAL: not a shitty error thing
    def constructErrorDb():
        global errors
        errors={'UnknownError' : 'Unknown error D:',
                'MetaError' : 'An error was called with an incorrect name.',
                'NotPercentages' : 'Percentages do not add up to 100.',
                'UnspecifiedScreenEvent' : 'Screen event not specified.',
                'ScreenNotInitialized' : 'Screen event specified before initializing screen.',
                'InvalidScreenID' : 'The screen ID specified is not valid.',
                'InvalidXY' : 'X and/or Y coords specified are outside row/col limits.',
                'ScreenNotEnabled' : 'Screen-drawing is disabled because no height was defined.'
                }

    # do those things
    defineSettings()
    constructErrorDb()

    # interpret keywords
    keywords = keyword.keys()
    if 'width' in keywords:
        Width_ = keyword['width']
    if 'height' in keywords:
        Height_ = keyword['height']
        # shouldn't be specified if there's no screen being used, really
        global ScreenIndex; ScreenIndex=[]
    if 'forceSize' not in keywords or 'forceSize' in keywords and keyword['forceSize']!=False:
        if _OSenv == 'nt':
            # set Windows terminal to the correct size
            call('mode con: cols='+str(Width_+1)+' lines='+str(Height_+1),shell=True)
            # they need +1 because Windows is quirky and needs extra space
        elif _OSenv == 'other' and 'height' in keywords and 'beQuiet' not in keywords and keyword['beQuiet']!=True:
            # in not-Windows, tell them to adjust their screen maybe?
            # not sure if I could force this but it's not a huge deal
            disp.clear()
            # avoid using a screen bc I don't want this in the screenIDs
            # IDEAL: though there should be a way to accomplish that w/ a screen...
            disp.write('',halfOf(Height_)-1) # go down to the middle-ish
            disp.write('You may want to adjust this window to',1,'centre')
            disp.write('match the dimensions of the screen.',0,'centre')
            pause()
            disp.clear()

# stops user from barfing on the display while things are being drawn
# totally stole this from my friend ninedotnine ;)
class PreventBarfing:
    def __enter__(self):
        if _OSenv=='other':
            global stdinfd; global oldtcattr
            oldtcattr = termios.tcgetattr(stdinfd)
            newtcattr = oldtcattr[:]
            newtcattr[3] = newtcattr[3] & ~termios.ECHO
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, newtcattr)
        else:
            pass
    def __exit__(self, typ, value, callback):
        if _OSenv=='other':
            global stdinfd; global oldtcattr
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
        else:
            pass

# pauses for a certain amount of time without asking for user input
# returns False if the user interrupts it forcefully
def sleep(length=0,force=False):
    if force==False:
        # any less than this encourages flickering
        if length<(halfOf(Width_)+20): # width is really the deciding factor
            length=(halfOf(Width_)+20)
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
            # really need to do this better
            busy=False
            return False
    busy=False
    return True

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

# IDEAL: fix this
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
    dispWrite(newstring)
    print(errors[err], file=errfile)
    quit()

# returns single-character input
def anykey(*messages):
    # windows version
    if _OSenv == 'nt':
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
            global stdinfd; global oldtcattr
            for message in messages:
                print(message)
            try:
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
            sys.stdout.flush()
            busy=False
            return char.lower() # ignore caps lock

    def tcflush():
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

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
                dispWrite(ch,0)
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
        dispWrite(message+' ',0)
    choice='tinkle'
    while choice=='tinkle':
        try:
            choice = input()
        except KeyboardInterrupt:
            quit()
    return choice.strip()

def reverseRange(number):
    return range(number,-1,-1)

def listFromString(string):
    characters=[]
    for i in range(len(string)):
        characters.append(string[i])
    return characters

# capitalizes first letter by default, or a specified letter
def capitalize(string, index=0):
    maxindex = len(string)-1
    if index > maxindex or index < 0:
        return string
    elif index==maxindex:
        return string[:index]+string[index].upper()
    elif index==0:
        return string[0].upper()+string[1:]
    else:
        return string[:index]+string[index].upper()+string[index+1:]

# halve a number without getting a float
def halfOf(number):
    number = number/2
    number = math.floor(number)
    return int(number)

# does everything
def randomNumber(lower=0, upper=1):
    return random.randint(lower,upper)

# choose one choice from a list of options
def randomChoice(choices=['dog','cat']):
    index = randomNumber(0,len(choices)-1)
    return choices[index]

# keeps list the same length by deleting first item, sliding each item 1 index
# back, and adding your new item to the end
def rippleAppend(theList, newItem):
    # set each item equal to the item 1 index ahead
    for i in range(len(theList)):
        try:
            theList[i]=theList[i+1]
        except IndexError:
            # when there's no more indexes ahead, append our new item
            theList[i]=newItem
    return theList

# safely exit the program
def quit(clearDisplay=True):
    if _OSenv!='nt':
        # make the terminal echo user input again
        # if you somehow exit w/o this, the terminal will be temporarily f'd ;D
        global oldtcattr; global stdinfd
        termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
    if clearDisplay:
        disp.clear()
    raise SystemExit  # buh-bye!

class disp:
    # clears the display
    def clear():
        if _OSenv == 'nt':
            # apparently this was the source of 90% of crashes on Windows
            try:
                call('cls',shell=True)
                return True
                # because cls is just that slow??
            except KeyboardInterrupt:
                return False
        else:
            call("clear",shell=True)

    # writes to the display. end is # of linebreaks. align is left, centre, right
    def write(line, end=1, align='left'):
        global busy
        while not busy:
            busy=True
            # decide how many spaces
            if align=='centre' or align=='center':
                spaces = (Width_-len(line))/2
                spaces=math.floor(spaces)
            if align=='right':
                spaces = Width_-len(line)

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

# makes screen objects
class screen:

    # INSTANCE VARIABLES
    '''
     str self.action  <- stores most recently triggered 'action' function
    list self.screen
     int self.announceX
     int self.announceY
     int self.x
     int self.y
    bool self.centreY
    bool self.centreX
    list self.area (x,y coords in tuples)
    '''

    # create a new screen object, return the screenID
    def __init__(self):
        self.action='init'
        # the screen is a list
        self.screen=[]
        # add as many rows as the height of the screen
        for _ in range(Height_):
            # the row is a list too
            row=[]
            for _ in range(Width_):
                # add as many cells to the row as the width of the screen
                row.append(' ')
            # add the row to the screen
            self.screen.append(row)
        # the screen table now exists

        # create announceX, announceY
        self.announceX=halfOf(Width_)
        self.announceY=halfOf(Height_-6)
        # set some defaults for cell()
        self.x=0; self.y=0; self.centreX=False; self.centreY=False

        global ScreenIndex
        self.screenID = len(ScreenIndex)
        ScreenIndex.append(self)

    def cell(self,x,y):
        self.action='cell'
        self.centreX=False
        self.centreY=False
        if type(x) != int:
            if x=='announceX':
                self.x = self.announceX
            elif x=='centre' or x=='center':
                self.centreX=True
                self.x = halfOf(Width_-1)
        else:
            self.x=x*1
        if type(y) != int:
            if y=='announceY':
                self.y = self.announceY
            elif y=='centre' or y=='center':
                self.centreY=True
                self.y = halfOf(Height_-1)
            elif y=='bottom':
                self.y=Height_-1
        else:
            self.y=y*1

    # expects to receive ranges of cols & rows or single one & range of another
    def area(self, **keyword):
        self.action = 'area'
        # create the lists we're going to need
        affectedRows=[]; affectedCols=[]; affectedCells=[]
        # get the keywords
        keywords = keyword.keys()

        # figure out what our starting row and ending row is. same for columns
        if 'cols' in keywords and 'col' not in keywords:
            startcol, endcol = keyword['cols']
        if 'rows' in keywords and 'row' not in keywords:
            startrow, endrow = keyword['rows']
        if 'row' in keywords and 'col' not in keywords:
            startrow = keyword['row']
            endrow = keyword['row']
            if 'cols' not in keywords:
                startcol = 0; endcol = Width_-1
        if 'col' in keywords and 'row' not in keywords:
            startcol = keyword['col']
            endcol = keyword['col']
            if 'rows' not in keywords:
                startrow = 0; endrow = Height_-1
        # be inclusive with ranges
        endcol+=1; endrow+=1 # 2,5 returns 2-5

        # create list of affected rows
        for row in range(endrow-startrow):
            affectedRows.append(row+startrow)
        # create list of affected columns
        for col in range(endcol-startcol):
            affectedCols.append(col+startcol)
        # using both lists, create list of affected cells
        for row in affectedRows:
            for col in affectedCols:
                affectedCells.append((col,row))
        # a list of x,y tuples
        self.affectedCells = affectedCells

    def line(self,**keyword):
        self.area(**keyword)

    def row(self,row):
        if type(row)=='int':
            self.line(row=row)
        elif row=='centre' or row=='center':
            self.line(row=halfOf(Height_))
        else:
            # get it from the last cell()?
            self.line(row=self.y)
        self.action='row'

    def column(self,col):
        if type(col)=='int':
            self.line(col=col)
        elif col=='centre' or col=='center':
            self.line(col=halfOf(Width_))
        else:
            # get it from the last cell()?
            self.line(col=self.x)
        self.action='column'

    def everything(self):
        self.area(cols=(0,Width_-1),rows=(0,Height_-1))

    # fills an area
    def fill(self, *keywords):
        # create list of random fill choices
        characters=[]
        for keyword in keywords:
            keyword = listFromString(keyword)
            characters += list(keyword)
        # use space if nothing was specified
        if len(characters)==0:
            characters.append(' ')
        for coord in self.affectedCells:
            x = coord[0]; y = coord[1]
            try:
                row = self.screen[y]
                row[x] = randomChoice(characters)
            except IndexError:
                pass

    # writes text starting at cell
    def write(self, *messages, **keyword):
        if self.action=='cell':
            direction='right'
            keywords = keyword.keys()
            if 'direction' in keywords:
                direction = str(keyword['direction'])

            if direction=='right':
                y = int(self.y)
                for message in messages:
                    x = int(self.x)
                    # if it's a number, drop so many rows
                    if type(message)=='int':
                        y+=message
                    else:
                        # if centred, compensate for the length of the message
                        if self.centreX==True:
                            x -= halfOf(len(message))
                        row = self.screen[y]
                        for i in range(len(message)):
                            try:
                                row[x+i]=message[i]
                            except IndexError:
                                continue
                        y+=1
            elif direction=='down':
                x = int(self.x)
                for message in messages:
                    y = int(self.y)
                    # if it's a number, drop so many... columns
                    if type(message)=='int':
                        x+=message
                    else:
                        # if centred, compensate for the length of the message
                        if self.centreY==True:
                            y -= halfOf(len(message))
                        row = self.screen[y]
                        for i in range(len(message)):
                            try:
                                row = self.screen[y+i]
                                row[x] = message[i]
                            except IndexError:
                                continue
                        x+=1

    # what affectedCells would be if it started at x,y instead
    def areaOffset(self,x,y):
        # determine where the old area was
        cols=[]; rows=[]
        for coord in self.affectedCells:
            cols.append(coord[0])
            rows.append(coord[1])
        cols.sort(); rows.sort()
        oldcols = (cols[0],cols[-1])
        oldrows = (rows[0],rows[-1])

        # find the difference
        difference = x-oldcols[0]
        newcols=(x,oldcols[1]+difference)
        difference = y-oldrows[0]
        newrows=(y,oldrows[1]+difference)

        # determine where the new area will be
        self.area(cols=newcols, rows=newrows)

    # moves things to a new x and y, replacing the old area with ch
    def move(self,**keyword):
        bg = '   '
        keywords = keyword.keys()
        if 'bg' in keywords:
            bg = listFromString(keyword['bg'])

        if self.action == 'cell':
            if 'x' in keywords and 'y' in keywords:
                row = self.screen[self.y]
                clipboard = row[self.x]
                row[self.x] = randomChoice(bg)
                row = self.screen[keyword['y']]
                row[keyword['x']] = clipboard
        elif self.action == 'column' or self.action == 'row' or self.action == 'area':
            clipboard=[]
            for coord in self.affectedCells:
                row = self.screen[coord[1]]
                # copy cell to clipboard before overwriting
                clipboard.append(row[coord[0]])
                row[coord[0]] = randomChoice(bg)
            if self.action == 'column' and 'x' in keywords:
                for i in range(Height_-1):
                    row = self.screen[i]
                    row[keyword['x']] = clipboard[i]
            elif self.action == 'row' and 'y' in keywords:
                row = self.screen[keyword['y']]
                for i in range(Width_-1):
                    row[i] = clipboard[i]
            elif self.action == 'area':
                if 'x' in keywords and 'y' in keywords:
                    # set self.affectedCells to the new area
                    self.areaOffset(keyword['x'],keyword['y'])
                    i=0
                    for coord in self.affectedCells:
                        if coord[0] > 0 and coord[0] < Width_ and coord[1] > 0 and coord[1] < Height_:
                            row = self.screen[coord[1]]
                            row[coord[0]] = clipboard[i]
                            i+=1

    # returns a true copy of the screen
    def takeSnapshot(self):
        return deepcopy(self.screen)

    # overwrites screen table with another screen table provided
    def replaceWithSnapshot(self,snapshot):
        self.screen = deepcopy(snapshot)

    '''
    # replays all screens with a certain delay between each, for testing purposes
    def replayAll(delay=1000, showID=True):
        for i in screens:
            screenID = screens.index(i)
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
        screenAnnounceArea(-1,Height_-1)
        screenAnnounce(screenID, 'Done.')
        screenDraw(screenID)
        quit()
    '''

    # displays row and col numbers on the edges of the screen
    # at the end, sets screen back to how it was (but doesn't draw it again)
    def showAxisLabels():
        # save the current screen
        restorePoint = self.takeSnapshot()
        for col in range(Width_):
            # add last # of column # to each column on row 0
            self.cell(col,0)
            self.write(str(col)[-1])
        for row in range(Height_):
            # add last # of row # to each row on column 0
            self.cell(0,row)
            self.write(str(row)[-1])
        # show the screen with axis labels added
        self.paint()
        # set the screen back to how it was before
        self.replaceWithSnapshot(restorePoint)

    # paint the screen  (aka draw it, display it, w/e)
    def paint(self, paintAllAtOnce=True):
        global busy
        while not busy:
            busy=True
            # in Windows it flickers if we don't clear
            # in Linux it flickers if we do :P
            if _OSenv=='nt':
                if not disp.clear():
                    return False
            if paintAllAtOnce:
                entirescreen = ''
                for y in range(Height_):
                    row = self.screen[y]
                    for x in range(Width_):
                        cell = row[x]
                        entirescreen += cell
                    # write a linebreak after every row
                    entirescreen+='\n'
                # draw the entire screen at once (reduces flicker on some machines)
                sys.stdout.write(entirescreen)
            else:
                for y in range(Height_):
                    row = self.screen[y]
                    for x in range(Width_):
                        cell = row[x]
                        sys.stdout.write(cell)
                    sys.stdout.write('\n')
            sys.stdout.flush()
        busy=False
        return True

    # replaces characters with other characters
    # IDEAL: anything
    def findReplace(cellToFind, replaceWith):
        pass

    def setAnnouncementArea(self, x=-1, y=-1):
        if x==-1:
            self.announceX=0
        elif type(x)=='int':
            self.announceX=x
        elif x == 'centre' or x == 'center':
            self.announceX='centre'

        if y==-1:
            self.announceY=0
        elif type(y)=='int':
            self.announceY=y
        elif y == 'centre' or y == 'center':
            self.announceY=halfOf(Height_-1)

    # similar to screen.wite except it remembers where to write and automatically
    # drops a line every time it's called, until the area is reset manually
    def announce(self, *messages):
        for message in messages:
            if type(message)==int:
                self.announceY+=message
            else:
                self.cell(self.announceX,self.announceY); self.write(message)
                if self.announceY < Height_-1:
                    self.announceY+=1

if __name__=='__main__':
    raise SystemExit
