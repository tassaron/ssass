#!/usr/bin/python3

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#
#                               ssass.py
#             The Somewhat Satisfactory ASCII Screen Simplifier
#                       an experiment by tassaron
#                          written Nov-Dec 2014
#
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

# stuff prefixed by IDEAL is what I want to get around to doing later

import sys
import os
import time
import math
import random
import threading # IDEAL: should only load this if we need it for a brain
from copy import deepcopy
from subprocess import call

# import different things depending on OS, and set a constant for later use
if os.name=='nt':
    _OSenv = 'nt'
    import msvcrt
else:
    _OSenv = 'other'
    import tty
    import termios

Debug=False

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   BASIC FUNCTIONS AND CLASSES THAT I RARELY CHANGE
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

# initializes stuff we need - this must be run ONCE before anything else
#   e.g., init('Title',width=Width_,height=Height_,forceSize=True,beQuiet=True,
#         brain=True,memory=250)
def init(title_='Defaultline Tittle',**keyword):
    global Width_; Width_=80
    global Height_; Height_=40
    global busy; busy=False
    global title; title = title_

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
        global brainEnabled; brainEnabled=False
        global tracker; tracker=0
        global bigTracker; bigTracker=0
        if _OSenv!='nt':
            # store stdin's file descriptor
            global stdinfd
            stdinfd = sys.stdin.fileno()
            global oldtcattr
            oldtcattr = termios.tcgetattr(stdinfd)

    # used by chunderEverywhere(), the error caller
    # IDEAL: errors as a class so they can be raised properly
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
    if 'brain' in keywords:
        # turn on random number generator
        global brainEnabled; brainEnabled=True
        global mainBrain
        if 'memory' in keywords:
            mainBrain = brain(memory=keyword['memory'])
        else:
            mainBrain = brain()
        global recycled; recycled=0

    if 'width' in keywords:
        Width_ = keyword['width']

    if 'height' in keywords:
        Height_ = keyword['height']
        # height shouldn't be specified if there's no screen being used, really
        global ScreenIndex; ScreenIndex=[]

        # think about forcing the screen size if height is defined
        if 'forceSize' in keywords and keyword['forceSize']!=False:
            forceSize = True
            if _OSenv == 'other':
                if 'beQuiet' in keywords and keyword['beQuiet']==True:
                    beQuiet=True
                else:
                    beQuiet=False
        else:
            forceSize = False

        if forceSize:
            if _OSenv == 'nt':
                # set Windows terminal to the correct size
                call('mode con: cols='+str(Width_+1)+' lines='+str(Height_+1),shell=True)
                # they need +1 because Windows is quirky and needs extra space

            elif _OSenv == 'other' and not beQuiet:
                # in not-Windows, tell them to adjust their screen maybe?
                # not sure if I could force this but it's not a huge deal
                disp.clear()
                disp.write('',halfOf(Height_)-1) # go down to the middle-ish
                disp.write('You may want to adjust this window to',1,'centre')
                disp.write('match the dimensions of the screen.',0,'centre')
                pause()
                disp.clear()

# parse command line arguments and return them
# doesn't work yet
def parseArgs(prog,**keyword):
    fancyline = '#-~-~-~-~-~-~--~-~-~-~-~-~-#'
    parser = argparse.ArgumentParser(prog=prog, description=fancyline,
                        epilog=fancyline)
# IDEAL: finish this
    keywords = keyword.keys()
    knownKeywords=[]
    for key in keywords:
        if key not in knownKeywords:
            parser.add_argument('-%s' % key,choices=keyword[key])
            knownKeywords.append(key)
        else:
            parser.add_argument('-%s' % key,)
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
    return arg

# quickly starts the program up for me to debug
def tass():
    debug()
    init('Whatever Who Cares',height=38,brain=True)

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
            # this doesn't apply to Windows
            pass
    def __exit__(self, typ, value, callback):
        if _OSenv=='other':
            global stdinfd; global oldtcattr
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
        else:
            # none of this does but I'd rather have it defined anyway
            pass

# SomewhatSatisfactoryError would be better but that's too long to bother with
# still unused for now; I'll get around to it
class TassError(Exception):
    def __init__(self, error='Unknown', *args):
        global errors
        if error in errors:
            print("\n%s:" % error)
            print(errors[error] % args)
        print("why would you do this. WHY")
        quit()

# the old error message printing thing. I'm getting rid of this
def chunderEverywhere(err='UnknownError'):
    global errors
    disp.clear()
    if err not in errors.keys():
        err = 'MetaError'
    string = errors[err]
    newstring=''
    for character in string:
        if randomNumber()==1:
            character.upper()
        newstring+=character
    disp.write(newstring)
    print(errors[err], file=errfile)
    quit()

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
            # IDEAL: really need to do this better
            busy=False
            return False
    busy=False
    return True

# untest save thing that I need to improve upon
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

# samesies
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

# debug mode - makes some functions print technical details of current actions
# into a file called title_debug.dat
def debug(enable=True, *disables):
    global Debug
    if enable:
        Debug=True
        global DebugDisables; DebugDisables=[]
        for keyword in disables:
            DebugDisables.append(keyword)
        cwd = os.getcwd() + '/Screensaver'
        debugFile = cwd + '_debug.dat'
        # overwrite old debug file
        with open(debugFile, 'w', encoding='utf-8') as savefile:
            print('Debug Output:',file=savefile)
    else:
        Debug=False

# writes debug messages to a file
def debugMessage(action, **keyword):
    if Debug and action not in DebugDisables:
        global cwd; global title
        debugFile = cwd + title + '_debug.dat'
        keywords = sorted(keyword.keys())
        with open(debugFile, 'a', encoding='utf-8') as savefile:
            print('%s {' % capitalize(action),file=savefile,end='')
            for key in keywords:
                    if key != 'message':
                        print(' %s: %s;' % (key, keyword[key]),file=savefile,end='')
                    else:
                        print(' %s' % keyword[key],file=savefile,end='')
            print(' }',file=savefile)

# safely exit the program
def quit(clearDisplay=True):
    try:
        if _OSenv!='nt':
            # make the terminal echo user input again
            # if you somehow exit w/o this, the terminal will be temporarily f'd ;D
            global oldtcattr; global stdinfd
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
        if clearDisplay:
            disp.clear()
    except:
        # oh well, just let me leave
        pass
    debugMessage('Tassaron',message='Buh-bye!')
    raise SystemExit  # buh-bye!

# functions that affect the display are separated here to differentiate them
# from similarly-named screen methods
class disp:
    # clears the display
    def clear():
        if _OSenv == 'nt':
            # apparently this was the source of 90% of crashes on Windows
            try:
                call('cls',shell=True)
                # because cls is just that slow??
            except KeyboardInterrupt:
                pass # whatever
        else:
            #call(["printf", "\033c"]) # maybe?
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



#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   USER INPUT RELATED STUFF
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

# returns single-character input, not really intended to be used directly
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

# stops until the user presses a key; discards the input
def pause():
    anykey()

# returns a single-character input from the user which can be a string or an int
# if valid inputs are defined, it'll keep asking until one is received
# input = getInput(vartype='int', valid='abc')
def getInput(*keywords, **keyword):
    ch='>'
    global busy
    while not busy:
        valids=None; type_='string'
        if 'noisy' in keywords:
            disp.write(ch,0)
        keywords = keyword.keys()
        if 'valid' in keywords:
            valids = listFromString(keyword['valid'])
        elif 'vartype' in keywords and keyword['vartype']=='int':
            type_='int'
        if valids:
            # if valid inputs are defined, keep asking until we get one
            while ch not in valids:
                ch = anykey()
        else:
            # otherwise, just take anything and return it
            ch = anykey()

        if type_=='int':
            return int(ch)
        else:
            return ch

# returns a string from the user
def getStringInput(message=None):
    if message:
        disp.write('%s ' % message,0)
    choice=None
    while choice==None:
        try:
            choice = input()
        except KeyboardInterrupt:
            quit()
    return choice.strip()


#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   RANDOMNESS
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

# choose one choice from a list; uses main brain object if it's enabled
def randomChoice(choices=['dog','cat']):
    # IDEAL: add weighted choices at some point
    if not brainEnabled:
        return random.choice(choices)
    else:
        return choices[randomNumber(0,len(choices)-1)]

# returns tuple of cols and rows ( presumably to be passed into area() )
# optional maxWidth/maxHeight defines maximum difference between cols/rows
# uses main brain object if it's enabled
def randomArea(maxWidth=-1, maxHeight=-1, **keyword):
    keywords = keyword.keys()

    # here's one way of doing cols/rows without copy and pasting code
    totalSize = [ Width_-1, Height_-1 ]
    maxSize = [ maxWidth, maxHeight ]

    for i in range(2):
        # determine where to pick a starting coord
        # IDEAL: should be better than this. doesn't really work
        if 'cols' in keywords and i==0:
            col1, col2 = keyword['cols']
            start = randomNumber(col1, col2)
        elif 'rows' in keywords and i==2:
            row1, row2 = keyword['rows']
            start = randomNumber(row1, row2)
        else:
            start = randomNumber(0, totalSize[i])

        randomRange=[]
        for _ in range(2):
            if maxSize[i] != -1:
                randomRange.append( randomNumber(0, maxSize[i]) )
            else:
                randomRange.append( randomNumber(0, totalSize[i]) )
        randomRange.sort() # put them in order smallest > lowest

        # if the bigger coord is off the screen, crop it at the edge
        if randomRange[1] > totalSize[i]:
            randomRange[1] = totalSize[i]

        if i==0:
            cols = ( start + randomRange[0], start + randomRange[1] )
        else:
            rows = ( start + randomRange[0], start + randomRange[1] )

    return cols, rows

# generates number between 0 and Width_ by default
# because that's usually the biggest # required
# uses main brain object if it's enabled
def randomNumber(lower=0, *keywords):
    # default upper range to width
    global Width_; upper=Width_
    for keyword in keywords:
        if type(keyword)==int:
            # accept any int as new upper range
            upper=keyword

    global brainEnabled
    if not brainEnabled:
        number = random.randint(lower,upper)
    else:
        global mainBrain
        global rndNum; global smallRndNum
        if upper!=Width_:
            if upper > 50:
                mainBrain.getRandomNumber()
                number = squeezeNumber(rndNum, upper)
            else:
                mainBrain.getSmallRandomNumber()
                number = squeezeNumber(smallRndNum, upper)
            if lower!=0:
                number+=lower
        else:
            mainBrain.getRandomNumber()
            number = rndNum
    global tracker; tracker+=1
    global bigTracker; bigTracker+=number
    return number

# attempts to regulate frame speed by allowing the program to reuse
# previously generated random numbers while generating new ones
# in a background thread. as a possibly-useful side effect, allows us to shave
# dice if we ever need to ;)
class brain:

    def __init__(self, **keyword):
        # use keywords to enable/disable extra things

        # This gives more beautiful patterns but takes longer
        # to generate a number than the built-in random
        self.thoughtShuffler = random.SystemRandom()

        keywords = keyword.keys()
        if 'memory' in keywords:
            self.memory = int(keyword['memory'])
        else:
            self.memory = 250 # default

        # initialize lists of random numbers
        self.rndNums = [i for i in range(1000)]
        self.smallRndNums = [i for i in range(100)]*self.memory
        self.rndNumMaxI = len(self.rndNums)
        self.smallRndNumMaxI = len(self.smallRndNums)
        self.rndNumI = 0; self.smallRndNumI = 0
        debugMessage('brain',message=' Generated %s numbers for the pool...' % str(self.rndNumMaxI+self.smallRndNumMaxI))

        # shuffle number pool
        reshuffle = threading.Thread(target=self.shuffleNumbers,daemon=True)
        reshuffle.start()
        reshuffleSmall = threading.Thread(target=self.shuffleSmallNumbers,daemon=True)
        reshuffleSmall.start()

    def shuffleNumbers(self):
        self.thoughtShuffler.shuffle(self.rndNums)
        debugMessage('brain',message='Recycled %s numbers while shuffling rndNums' % self.rndNumI)
        global recycled; recycled+=self.rndNumI

    def shuffleSmallNumbers(self):
        self.thoughtShuffler.shuffle(self.smallRndNums)
        debugMessage('brain',message='Recycled %s numbers while shuffling smallRndNums' % self.smallRndNumI)
        global recycled; recycled+=self.rndNumI

    def getSmallRandomNumber(self):
        global smallRndNum
        if self.smallRndNumI > self.smallRndNumMaxI-500:
            # reshuffle pregenerated numbers in a new thread
            self.smallRndNumI=0
            debugMessage('brain',message='Shuffling smallRndNums...')
            reshuffle = threading.Thread(target=self.shuffleSmallNumbers,daemon=True)
            reshuffle.start()
        try:
            smallRndNum = self.smallRndNums[self.smallRndNumI]
        except IndexError:
            debugMessage('brain',message='Lag!', smallRndNum='37')
            smallRndNum=37
        self.smallRndNumI+=1

    def getRandomNumber(self):
        global rndNum
        if self.rndNumI > self.rndNumMaxI:
            # reshuffle pregenerated numbers in a new thread
            self.rndNumI=0
            debugMessage('brain',message='Shuffling rndNums...')
            reshuffle = threading.Thread(target=self.shuffleNumbers,daemon=True)
            reshuffle.start()
        try:
            rndNum = self.rndNums[self.rndNumI]
        except IndexError:
            debugMessage('brain',message='Lag!', rndNum='371')
            rndNum = 371
        self.rndNumI+=1

# it's fun to pointlessly keep track of numbers
def getTrackers():
    global tracker; global bigTracker
    if brainEnabled:
        global recycled
        return tracker, bigTracker, recycled
    else:
        return tracker, bigTracker, 0

# squeezes the range of a generated random number
# make sure it knows the old maximum number if you don't use the default
def squeezeNumber(number, newMax, **keyword):
    keywords = keyword.keys()
    if 'direction' in keywords:
        # round down or up?
        direction = keyword['direction']
    else:
        # tell it to decide later
        direction='decide'
    if 'oldMax' in keywords:
        oldMax = keyword['oldMax']
    elif 'oldmax' in keywords:
        oldMax = keyword['oldmax']
    else:
        # we'll just assume
        if number > 50:
            oldMax = 1000
        else:
            oldMax = 50
    proportion = number / oldMax
    equals = proportion * newMax
    if direction=='down':
        return math.floor(equals)
    elif direction=='up':
        return math.ceil(equals)
    else:
        fraction, integer = math.modf(equals)
        if fraction >= 0.5:
            integer+=1
        return int(integer)

# squeezes the range of a generated random area
def squeezeArea(area,into):
    cols, rows = area
    col1, col2 = cols
    col1=int(col1*into); col2=int(col2*into)
    cols = (col1, col2)
    row1, row2 = rows
    row1=int(row1*into); row2=int(row2*into)
    rows = (row1, row2)
    return cols, rows



#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   MISCELLANEOUS HANDY TOOLS
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

# I feel like I may want to do something more with this someday
def listFromString(string):
    return list(string)

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
def halfOf(number,rounding='down'):
    number = number/2
    if rounding=='down':
        number = math.floor(number)
    else:
        number = math.ceil(number)
    return number

# divide like you're in grade two point three
# easier than modulus, and more useful in many cases >_>
def simpleDivide(num1, num2):
    result = num1 / num2
    result = int(result)
    if result < 0:
        result *= -1
    remainder = num1 - num2 * result
    return result, remainder

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

# give back a human-readable timestamp
def getTimestamp(type_='tuple'):
    import time
    localtime = time.localtime() # returns tuple of local time info
    validTypes = ['tuple','table']

    if type_ in validTypes:
        # use 12-hour time
        meridean = 'a'
        hour = localtime[3]
        if hour > 12:
            hour-=12 # IDEAL: use correct term
            meridean = 'p'

        if type_=='tuple':  # d/m/y
            date = str(localtime[2])+'/'+str(localtime[1])+'/'+str(localtime[0])

            # add 0 to the minute when needed
            minute = str(localtime[4])
            if len(minute) < 2:
                minute = '0'; minute+=str(localtime[4])

            time = str(hour)+':'+minute+meridean+'m'
            timestamp = date, time
        elif type_=='table':
            timestamp = {
                "Year"      : localtime[0],
                "Month"     : localtime[1],
                "Day"       : localtime[2],
                "Hour"      : hour,
                "Minute"    : localtime[4],
                "Meridean"  : meridean+'m'
            }
        return timestamp
    else:
        return 'Invalid Type'


#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   SCREEN OBJECTS
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

# instances have 1 table of columns and rows each to represent a screen which
# can be controlled using their selector and action methods
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
    list self.selectedCells (x,y coords in tuples)
    list self.selectedArea (col/row ranges in tuples)
    '''

    # RULES:
    # 1. Put coords in the order x,y / col,row / width,height when possible.
    # 2. Selector methods must not perform actions and vice versa.

    # create a new screen object, return the screenID
    def __init__(self):
        self.action='init'
        # the screen is a list with (Height) # of (Width)-length rows
        self.screen = [' ']*Height_
        self.screen = [ [row]*Width_ for row in self.screen]

        # create announceX, announceY
        self.announceX=halfOf(Width_)
        self.announceY=halfOf(Height_-6)
        # set some defaults for cell()
        self.x=0; self.y=0; self.centreX=False; self.centreY=False

        global ScreenIndex
        self.screenID = len(ScreenIndex)
        ScreenIndex.append(self)

        debugMessage('screen',message=' Newly Initialized')

    #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
    #   SELECTOR METHODS
    #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

    # select a cell
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
            self.x=x
        if type(y) != int:
            if y=='announceY':
                self.y = self.announceY
            elif y=='centre' or y=='center':
                self.centreY=True
                self.y = halfOf(Height_-1)
            elif y=='bottom':
                self.y=Height_-1
        else:
            self.y=y
        debugMessage('cell',x=self.x,y=self.y)

    # selects an area (called by most selector methods)
    # expects to receive ranges of cols & rows or single one & range of another
    def area(self, **keyword):
        self.action = 'area'
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

        # make lists of the ranges we need to select
        if startcol < endcol:
            affectedCols = [ i for i in range(startcol, endcol+1) ]
        else:
            affectedCols = [ i for i in range(endcol, startcol+1) ]
        if startrow < endrow:
            affectedRows = [ i for i in range(startrow, endrow+1) ]
        else:
            affectedRows = [ i for i in range(endrow, startrow+1) ]

        # using both lists, create list of <s>affected</s> selected cells
        totalCols = range(len(affectedCols))
        totalRows = len(affectedRows)
        affectedCols = affectedCols * totalRows
        selectedCells = []
        for row in range(totalRows):
            selectedCells.extend([ (affectedCols[col], affectedRows[row]) for col in totalCols])

        debugMessage('area',colstart=affectedCols[0],colend=affectedCols[-1],\
                     rowstart=affectedRows[0],rowend=affectedRows[-1],\
                     selectedCells=len(selectedCells))

        '''
        This is a bit faster than calling append() several thousand times was.
        The speed difference kinda adds up if the screen is updating rapidly.

        It would be trivial to only select existing cells here, but it'll be a
        lot easier later to just select blindly for now because then we know
        that two areas covering equal ranges are going to include an equal
        number of cells.
        '''

        self.selectedArea = (startcol, endcol), (startrow, endrow)
        # and the grand finale...
        self.selectedCells = selectedCells # a list of x,y tuples

    # select a line (currently broken)
    def line(self, startcell=(), endcell=()):
        startx, starty = startcell
        endx, endy = endcell

        # if it's all on one row or column...
        if startx == endx and starty == endy:
            self.cell(startx,starty)
        elif startx == endx:
            self.area(col=startx,rows=(starty, endy))
        elif starty == endy:
            self.area(cols=(startx,endx),row=starty)
        else:
            # so we're selecting an angled line are we?
            self.action = 'line' # okayyy, maybe self.action was a bad idea

            # first we'll need the horizontal difference between the Xs
            horiDiff = endx-startx
            if horiDiff < 0:
                hdirection = 'left'
                horiDiff *= -1
            else:
                hdirection = 'right'
                horiDiff += 1
            # then, the vertical difference between the Ys
            vertDiff = endy-starty
            if vertDiff < 0:
                vdirection = 'up'
                vertDiff *= -1
            else:
                vdirection = 'down'
                vertDiff += 1  #?

            # bigger # divided by smaller # = length of segments
            # & get remainders so we can handle angles that don't divide evenly
            if horiDiff > vertDiff:
                segmentLength, extraLength = simpleDivide(horiDiff, vertDiff)
            else: # should be imposs for #s to be =
                segmentLength, extraLength = simpleDivide(horiDiff, vertDiff)
            if segmentLength==0:
                segmentLength = 1
            extraSegments, extraLength = simpleDivide(extraLength, segmentLength)

            # construct list of rows between y's, in order
            if starty < endy:
                rows = range(starty, endy+1)
            elif starty > endy:
                # reverse range to go up (high #s are lower)
                rows = range(starty, endy-1, -1)
            rows = list(rows)
            segmentRange = range(segmentLength)
            if hdirection=='left':
                segmentRange = [ i*-1 for i in segmentRange ]

            '''
            Okay, this isn't working. I'll have to do something that forms a list
            of segments and iterates through them incrementing the y value instead.
            Or at least, I /think/ that'll be easier. :|

            Better use, learn how to make a generator.
            '''
            #segments = (segmentLength if extraLength==0 else segmentLength+extraLength, extraLength-1 for row in rows) #?

            i=0; selectedCells = []
            for y in rows:
                if extraLength > 0:
                    if hdirection=='right':
                        selectedSegment = [ (startx+j, y) for j in range(1, extraLength+1) ]
                        startx += extraLength
                    else:
                        selectedSegment = [ (startx-j, y) for j in range(1, extraLength+1) ]
                        startx -= extraLength
                    selectedCells.extend(selectedSegment)
                    extraLength=0
                if hdirection=='right':
                    x = startx+(segmentLength*i)
                    selectedSegment = [ (x+j, y) for j in segmentRange ]
                elif hdirection=='left':
                    x = startx-(segmentLength*i)
                    selectedSegment = [ (x-j, y) for j in segmentRange ]
                selectedCells.extend(selectedSegment)
                i+=1
            if extraSegments > 0:
                y = endy
                if hdirection=='right':
                    x = startx+(segmentLength*i)
                    selectedSegment = [ (x+j, y) for j in range(extraSegments)]
                else:
                    x = startx-(segmentLength*i)
                    selectedSegment = [ (x-j, y) for j in range(extraSegments)]
                selectedCells.extend(selectedSegment)

            debugMessage('line',start=startcell,end=endcell,astart=(startx,starty),
                         aend=(endx, endy), horiDiff=horiDiff, vertDiff=vertDiff,
                         segLen=segmentLength, xtraLen=extraLength,hdir=hdirection,
                         vdir=vdirection)

            self.selectedCells = selectedCells # a list of x,y tuples
            # we don't need to reset self.selectedArea

    # rows and columns are areas but if you haven't guessed yet...
    def row(self,row):
        if type(row)==int:
            self.area(row=row, cols=(0, Width_-1))
        elif row=='centre' or row=='center':
            self.area(row=halfOf(Height_),cols=(0,Width_-1))
        else:
            # get it from the last cell()?
            self.area(row=self.y, cols=(0,Width_-1))
        self.action='row'

    # ...I want my code to be readable, and these help a lot
    def column(self,col):
        if type(col)==int:
            self.area(col=col, rows=(0, Height_-1))
        elif col=='centre' or col=='center':
            self.area(col=halfOf(Width_), rows=(0, Height_-1))
        else:
            # get it from the last cell()?
            self.area(col=self.x, rows=(0, Height_-1))
        self.action='column'

    # same excuse ;P
    def everything(self):
        self.area(cols=(0,Width_-1),rows=(0,Height_-1))

    #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
    #   ACTION METHODS
    #=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

    # paint the screen  (aka draw it, display it, w/e)
    def paint(self, paintAllAtOnce=True):
        global busy
        while not busy:
            busy=True
            # in Windows it flickers if we don't clear
            # in Linux it flickers if we do :P
            if _OSenv=='nt':
                disp.clear()
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
                        sys.stdout.flush()
                    sys.stdout.write('\n')
            sys.stdout.flush()
        busy=False
        debugMessage('screen',message=' Painted~')
        return True

    # fills a non-cell selection
    def fill(self, *keywords):
        # create list of random fill choices
        characters=[]
        for keyword in keywords:
            keyword = listFromString(keyword)
            characters.extend(keyword)
        # use space if nothing was specified
        if len(characters)==0:
            characters.append(' ')

        rndNumsReqd=0
        for coord in self.selectedCells:
            x = coord[0]; y = coord[1]
            try:
                row = self.screen[y]
                try:
                    if x >= 0:
                        row[x] = randomChoice(characters)
                        rndNumsReqd+=1
                except IndexError:
                    continue # don't draw columns that are off-screen
            except IndexError:
                break # we're done if the current row is off-screen
        debugMessage('screen',message=' Filled using %s random numbers' % rndNumsReqd)

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
                    if type(message)==int:
                        y+=message
                    else:
                        # if centred, compensate for the length of the message
                        if self.centreX==True:
                            x -= halfOf(len(message))
                        try:
                            row = self.screen[y]
                            for i in range(len(message)):
                                try:
                                    if x+i >= 0:
                                        row[x+i]=message[i]
                                except IndexError:
                                    continue
                            y+=1
                        except IndexError:
                            pass
            elif direction=='down':
                x = int(self.x)
                for message in messages:
                    y = int(self.y)
                    # if it's a number, drop so many... columns
                    if type(message)==int:
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

    def setAnnouncementArea(self, x=-1, y=-1):
        if x==-1:
            self.announceX=0
        elif type(x)==int:
            self.announceX=x
        elif x == 'centre' or x == 'center':
            self.announceX='centre'

        if y==-1:
            self.announceY=0
        elif type(y)==int:
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

    # moves things to a new x and y, replacing the old area with ch
    def move(self,**keyword):
        keywords = keyword.keys()
        # create list of potential background fills
        bg = ' '
        if 'bg' in keywords:
            bg = listFromString(keyword['bg'])

        # MOVING CELLS
        if self.action == 'cell':
            if 'x' in keywords and 'y' in keywords:
                row = self.screen[self.y]
                clipboard = row[self.x]
                row[self.x] = randomChoice(bg)
                row = self.screen[keyword['y']]
                row[keyword['x']] = clipboard

        # MOVING ANYTHING ELSE
        elif self.action == 'column' or self.action == 'row' or self.action == 'area':
            # copy the selected area to a clipboard - make null entries for nonexistence
            # IDEAL: a copy() method
            clipboard = [ None if Height_ < y < 0 or Width_ < x < 0 else self.screen[y][x]
                          for (x, y) in self.selectedCells if x < Width_ and y < Height_ ]
            # empty out the selected area with our bg choices
            self.fill(bg)

            # IDEAL: fix the other actions, not just area
            if self.action == 'column' and 'x' in keywords:
                for i in range(Height_-1):
                    row = self.screen[i]
                    row[keyword['x']] = clipboard[i]
            elif self.action == 'row' and 'y' in keywords:
                row = self.screen[keyword['y']]
                for i in range(Width_-1):
                    row[i] = clipboard[i]
            elif self.action == 'area':
                # IDEAL: behaviour if x or y isn't defined
                if 'x' in keywords and 'y' in keywords:
                    newStartCol = keyword['x']; newStartRow = keyword['y']
                    # figure out where the new area is
                    oldcols, oldrows = self.selectedArea

                    # find the difference
                    oldStartCol, oldEndCol = oldcols
                    difference = newStartCol - oldStartCol
                    newcols = [ newStartCol, oldEndCol + difference ]
                    oldStartRow, oldEndRow = oldrows
                    difference = newStartRow - oldStartRow
                    newrows = [ newStartRow, oldEndRow + difference ]
                    newcols.sort(); newrows.sort()
                    tuple(newcols); tuple(newrows)

                    # determine where the new area will be
                    oldSelectedCells = self.selectedCells
                    self.area(cols=newcols, rows=newrows)

                    # IDEAL: fix fill and move both doing this bg/fill thing...
                    i=0; choice = randomChoice(bg)
                    for coord in self.selectedCells:
                        x, y = coord
                        try:
                            row = self.screen[y]
                            try:
                                if clipboard[i]:
                                    row[x] = clipboard[i]
                                else:
                                    row[x] = choice
                            except IndexError:
                                i+=1
                                continue
                        except IndexError:
                            # and we're done if the current row is off-screen
                            break
                        i+=1

                    # it's unintuitive to leave the new area selected
                    self.selectedArea = oldcols, oldrows
                    self.selectedCells = oldSelectedCells

    # skews selected area right or left
    def skew(self,direction,**keyword):
        if self.action=='area':
            keywords = keyword.keys()
            bg = ' '
            if 'bg' in keywords:
                bg = listFromString(bg)

            cols, rows = self.selectedArea
            startcol, endcol = cols
            startrow, endrow = rows
            rows = [ i for i in range(startrow, endrow+1) ]
            # copy area to clipboard row-by-row
            clipboard = [ self.screen[row][startcol:endcol+1] for row in rows]
            # empty the area out
            self.fill(bg)

            # we'll use row# as # of spaces to skew, thus...
            height = endrow-startrow
            if direction=='right':
                # ...going right we start with big numbers...
                height = range(height,-1,-1)
            else:
                # ...and going left we start with small.
                height = range(height)

            # start here
            y = startrow
            x = startcol
            for row in height:
                self.cell(x+row,y)
                self.write("".join(clipboard[row]))
                y+=1

            # don't let cell() change the action
            self.action='area'

    # empties the entire screen
    def clear(self):
        oldAction = self.action
        self.everything()
        self.fill()
        # reset this bc this isn't an explicit selector
        self.action = oldAction

    # returns a true copy of the screen
    def takeSnapshot(self):
        return deepcopy(self.screen)
        # this is slow-ish, but it's not a common action either

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

    # replaces characters with other characters within an area
    def findReplace(self, thingToFind, replaceWith):
        thingsToFind = listFromString(thingToFind)
        thingsToReplaceWith = listFromString(replaceWith)
        rndNumsReqd=0
        for coord in self.selectedCells:
            x = coord[0]; y = coord[1]
            try:
                row = self.screen[y]
                if row[x] in thingsToFind:
                    row[x] = randomChoice(thingsToReplaceWith)
                    rndNumsReqd+=1
            except IndexError:
                pass
        debugMessage('screen',message=" Used %s random numbers to findReplace cells" % rndNumsReqd)


#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#                                  Buh-bye!
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

if __name__=='__main__':
    raise SystemExit

