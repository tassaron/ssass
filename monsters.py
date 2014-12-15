#!/usr/bin/python3

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#
#                               monsters.py
#             The Somewhat Satisfactory Monster Simulation Thing
#                        an experiment by tassaron
#                           written Dec 2014
#
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

from ssass import *

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   SPECIAL MOVES
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
potentMoves = {
    'type' : 'science',
    'Migraine' : (20, 65, 1, 'headache')
}

smartMoves = {
    'type' : 'science',
    'Biochemistry' : (25, 75, 2),
    'Neuroscience' : (15, 75, 2, 'headache')
}

contagiousMoves = {
    'type' : 'undead',
    'Infect' : (25, 65, 0, 'poison')
}

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   NORMAL MOVES
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

undeadMoves = {
    'type' : 'undead',
    'Claw' : (10, 95, 0),
    'Bite' : (8, 100, 0, 'poison')
}

scienceMoves = {
    'type' : 'science',
    'Logic' : (15, 86, 1),
    'Math' : (8, 90, 1, 'headache')
}

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   SPECIALIZED MOVES
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

deductrixMoves = {
    'type' : 'science',
    'Deduce Meaning' : (40, 75, 1),
    'Introspect' : (5, 100, -2)
}

'''
typeMoves {
    'type' : 'typename',
    'moveName' : (int(baseDamage), int(baseAccuracy), int(magicMultiplier), str(specialEffects))
'''

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   CREATURE DEFS
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

# attributes settable in an instance's keywords
validAttributes = [
    'article', 'name', 'hp', 'secondaryType', 'specialTraits'
]

class Creature:

    def __init__(self, **keyword):
        properName = ''
        name = self.name.split()
        maxI = len(name)
        i=0
        for part in name:
            if maxI>i>0:
                # put spaces between words
                # not at the end or start
                properName+=' '
            part = capitalize(part)
            properName += '%s' % part
            i+=1
        self.properName = properName

        # create a capitalized name with traits prefixed
        if len(self.specialTraits)>0:
            self.fancyName=''
            for trait in self.specialTraits:
                self.fancyName += '%s ' % capitalize(trait)
            self.fancyName+= properName
        else:
            self.fancyName=None

        # do any final pluses and minuses according to
        # this creature's special traits
        if 'tall' in self.specialTraits:
            self.hp+=10
            self.mp-=10
        if 'potent' in self.specialTraits:
            self.mp+=20
            self.moveList.append(potentMoves)
        if 'smart' in self.specialTraits:
            self.mp+=10
            self.moveList.append(smartMoves)
        if 'deductrix' in self.specialTraits:
            self.moveList.append(deductrixMoves)

        super().__init__()


#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   COMMON TYPES
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

class Undead(Creature):

    def __init__(self, **keyword):

        # default attributes of this type...
        self.colour = 'green'                  # colour of the creature's name
        self.immunities = ['death','poison']   # who it's normally immune to
        self.strongths = ['nature','life']     # who it's normally stong against
        self.weaknesses = ['science']          # who it's normally weak against
        self.moveList=[]
        self.moveList.append(undeadMoves)

        super().__init__(**keyword)

class Death(Creature):

    def __init__(self, **keyword):

        # a death monster? :P
        self.colour = 'black'
        self.immunities = ['death','poison']
        self.strongths = ['nature','life']
        self.weaknesses = ['undead']
        self.moveList=[]

        super().__init__(**keyword)

class Poison(Creature):

    def __init__(self, **keyword):

        self.colour = 'violet'
        self.immunities = None
        self.strongths =  ['life']
        self.weaknesses = ['science']
        self.moveList=[]

        super().__init__(**keyword)

class Nature(Creature):

    def __init__(self, **keyword):
        self.colour = 'lime'
        self.immunities = None
        self.strongths =  ['science']
        self.weaknesses =  ['death']
        self.moveList=[]

        super().__init__(**keyword)

class Life(Creature):

    def __init__(self, **keyword):
        self.colour = 'white'
        self.immunities = None
        self.strongths = ['undead']
        self.weaknesses =  ['science']
        self.moveList=[]

        super().__init__(**keyword)

class Science(Creature):

    def __init__(self, **keyword):
        self.colour = 'grey'
        self.immunities = ['undead']
        self.strongths = ['undead', 'life']
        self.weaknesses = ['death']
        self.moveList=[]
        self.moveList.append(scienceMoves)

        super().__init__(**keyword)

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   UNDEAD ENEMIES
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

class Zombie(Undead):

    def __init__(self, *traits, **keyword):

        # default attributes of this monster...
        self.article = 'a'
        self.name = 'zombie'
        self.hp = 100
        self.mp = 0
        self.secondaryType = None
        self.specialTraits = []
        for trait in traits:
            self.specialTraits.append(trait)

        diceroll=randomNumber(0,10)
        if diceroll==0:
            if 'tall' not in self.specialTraits:
                self.specialTraits.append('tall')
        elif diceroll==1:
            if 'smart' not in self.specialTraits:
                self.specialTraits.append('smart')

        diceroll=randomNumber(0,2)
        if diceroll==0:
            self.description = ("A disgusting, rotten corpse barely holding itself",
            "together long enough to shamble towards your tasty, tasty brains.")
        elif diceroll==1:
            self.description = ("An adorable young girl, fingers dripping with",
            "red finger paint. :3 She's also eating the paint! ...Oh, it's a zombie.")
        elif diceroll==2:
            self.description = ("A handsome jogger with guts squishing around",
            "in his sneakers. Luckily he doesn't seem to mind!")

        super().__init__(**keyword)

class Zambie(Undead):
    pass

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   DEATH ENEMIES
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

class SentientVirus(Death):
    def __init__(self, *traits, **keyword):

        # default traits for this creature
        self.article='a'
        self.name='sentient virus'
        self.hp=400
        self.mp=800
        self.secondaryType = 'life'

        # get special traits as defined by keywords
        self.specialTraits = []
        for trait in traits:
            self.specialTraits.append(trait)

        self.description = ("We're doomed.",)

        super().__init__(**keyword)

class Demon(Death):
    def __init__(self, *traits, **keyword):

        # default traits for this creature
        self.article='a'
        self.name='demon'
        self.hp=900
        self.mp=900
        self.secondaryType = None

        # get special traits as defined by keywords
        self.specialTraits = []
        for trait in traits:
            self.specialTraits.append(trait)

        self.description = ("We're doomed.",)

        super().__init__(**keyword)

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   POISON ENEMIES
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

class Spider(Poison):
    def __init__(self, *traits, **keyword):

        # default traits for this creature
        self.article='a'
        self.name='giant spider'
        self.hp=120
        self.mp=06
        self.secondaryType = 'nature'

        # get special traits as defined by keywords
        self.specialTraits = []
        for trait in traits:
            self.specialTraits.append(trait)

        self.description = ("We're doomed.",)

        super().__init__(**keyword)

class Gelatin(Poison):
    def __init__(self, *traits, **keyword):

        # default traits for this creature
        self.article='a'
        self.name='mobile gelatin'
        self.hp=240
        self.mp=400
        self.secondaryType = None

        # get special traits as defined by keywords
        self.specialTraits = []
        for trait in traits:
            self.specialTraits.append(trait)

        self.description = ("We're doomed.",)

        super().__init__(**keyword)

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   NATURE ENEMIES
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

class Bear(Nature):
    pass

class MageTurkey(Nature):
    pass

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   SCIENCE ENEMIES
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

class PsychicHobo(Science):

    def __init__(self, *traits, **keyword):

        # default traits for this creature
        self.article='a'
        self.name='psychic hobo'
        self.hp=200
        self.mp=200
        self.secondaryType = None

        # Get special traits as defined by keywords
        self.specialTraits = []
        for trait in traits:
            self.specialTraits.append(trait)

        # Randomly choose some more special traits to add
        diceroll=randomNumber(0,10)
        if diceroll==0:
            if 'tall' not in self.specialTraits:
                self.specialTraits.append('tall')
        elif diceroll==1 or diceroll==4:
            if 'smart' not in self.specialTraits:
                self.specialTraits.append('smart')
        elif diceroll==2:
            if 'smart' not in self.specialTraits:
                self.specialTraits.append('potent')

        # Pick a description
        diceroll=randomNumber(0,1)
        if diceroll==0:
            self.description = ("A smelly (yet somehow striking) lady with hair",
            "disturbingly held in mid-air like Medusa tentacles by an unknown force.")
        elif diceroll==1:
            self.description = ("An elderly man who, despite his greying hair,",
            "looks rather spry for his age. He wields a shopping cart and a",
            "determined expression.")

        super().__init__(**keyword)

class Deductrix(Science):

    def __init__(self, *traits, **keyword):

        # default traits for this creature
        self.article='the'
        self.name='Deductrix'
        self.hp=800
        self.mp=1800
        self.secondaryType = 'undead'

        # Get special traits as defined by keywords
        self.specialTraits = ['deductrix']
        for trait in traits:
            self.specialTraits.append(trait)

        self.description = ("A half-rotten mobile corpse of indeterminate gender,",
        "with a fierce look in its eyes. You can tell that this is one seriously",
        "educated zombie.")

        super().__init__(**keyword)

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#   GAMEPLAY
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

def main():
    giveMessage('centre','centre','Hello World!')

def giveMessage(x, y, *messages):
    if type(x)==str:
        if x == 'centre' or x == 'center':
            x = halfOf(Width_)
    if type(y)==str:
        if y == 'centre' or y == 'center':
            y = halfOf(Height_)

    # determine longest message
    longestMessage=0
    for message in messages:
        msgLen = len(message)
        if msgLen > longestMessage:
            longestMessage = msgLen
    # determine where to start writing
    longestMessage=halfOf(longestMessage)
    x = x-longestMessage
    y = y-len(messages) # length of message list (which is # of rows dropped)
    # empty out the area where we're about to write...
    page.area(cols=(x-9,x+longestMessage+9), rows=(y-2,y+len(messages)+2))
    page.fill(' ')
    # now, write the text
    page.cell(x,y)
    page.write(messages)
    # and draw the borders
    page.area(col=x-10,rows=(y-1,y+len(messages)+2)) # left wall
    page.fill('|')
    page.area(col=x+longestMessage+10,rows=(y-1,y+len(messages)+2)) # right wall
    page.fill('|')
    page.area(cols=(x-9,x+longestMessage+9),row=y-2) # top wall
    page.fill('_')
    page.area(cols=(x-9,x+longestMessage+9),row=y+len(messages)+2) # bottom wall
    page.fill('_')
    page.paint()
    pause()

def waitForInput():
    pass

if __name__=='__main__':
    Width_ = 145
    if currentOS()=='nt':
        Height_ = 51
    else:
        Height_= 41

    # initialize ssass
    init('Monster Mash',width=Width_,height=Height_,forceSize=True,beQuiet=True)

    page = Screen()

    try:
        main()
    except KeyboardInterrupt:
        quit()
