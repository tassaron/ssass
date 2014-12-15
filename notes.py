#!/usr/bin/python3

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#
#                               notes.py
#                           A Note-Taking App
#                          written by tassaron
#                          created: 14.12.2014
#
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

from ssass import *

# adds \n into text at the right spots depending on Width_
def linewrap():
    pass

def loadNotes():
    global noteFile; global notes
    with open(noteFile, 'r', encoding='utf-8') as noteDB:
        nowReading = None
        currentID=0
        for line in noteDB:
            if not line.startswith('# '): # ignore comments
                if line.startswith('#=~=~=~=#'):
                    _, title = line.split(' ')
                    # the key is a sequential numeric id and a title
                    # we must strip off the last character, a newline
                    nowReading = '%s %s' % (currentID, title[:-1])
                    notes[nowReading]=[]
                    currentID+=1
                if nowReading: # if we have a title, add to its data
                    if not line.startswith('#'):
                        # again, we have to strip off the newline
                        notes[nowReading].append(line[:-1])

def showNotes():
    disp.clear()
    disp.write('',6)
    global notes; noteTitles = notes.keys()
    # create list of notes
    # don't use global notes after this ;p
    notes=['']*len(noteTitles)
    for title in noteTitles:
        noteID, noteTitle = title.split(' ')
        notes[int(noteID)] = noteTitle
    i=0
    for note in notes:
        # write the ID and the note title
        disp.write('%s. %s' % (str(i), note))
        i+=1
    validIDs = [ i for i in range(len(notes)) ]
    ch = getInput(vartype='char',valid=stringFromList(validIDs))
    chosenNote = Note(ch)
    chosenNote.show()

class Note:

    def __init__(self, noteID):
        global notes
        self.ID = noteID
        noteTitles = notes.keys()
        for title in noteTitles:
            if title.startswith(str(noteID)):
                _, title_ = title.split(' ')
                self.title = title_
                self.content = notes[title]

    def show(self):
        disp.write('',6)
        disp.write(self.title, 1, 'centre')
        for line in self.content:
            disp.write(line,0,'left')
        pause()


Width_=108; Height_=41
init(title='Notes',width=Width_,height=Height_)
noteFile = currentDir() + 'notes.dat'
notes = {}

if __name__=='__main__':
    try:
        loadNotes()
        while True:
            showNotes()
    except KeyboardInterrupt:
        quit()
