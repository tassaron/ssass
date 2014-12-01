#!/usr/bin/python3
'''

Animation Test by tassaron

'''

import tass
_width=79; _height=32
_frameDelay=100 # sleep time between frames
# this should be run at 10 fps

def newFrame(fill=True,reset=True):
    frame = tass.screenInit()
    if fill:
        # add borders to every frame
        tass.screenFill(frame,'row 0','col 0','row '+str(_height-1),'col '+str(_width-1),'with #')
    if reset:
        # reset announcements to a nice spot
        tass.screenAnnounceArea(-1,2)
    return frame # which is a screenID

def show(sceneID):
    middle = tass.halfOf(_height) # handy
    frames=[] # initialize a list of frames to show
    # each scene will create a list of frames. this organizes the animation

    if sceneID==-1:                                                     #GOODBYE
        frame = newFrame()####
        tass.screenWrite(frame,-1,middle-2,'Goodbye chum~ :\'(')
        tass.screenWrite(frame,-1,middle-1,'Hope to be seen by you again sometime!')
        tass.screenWrite(frame,-1,middle+3,'O       O')
        tass.screenWrite(frame,-1,middle+4,'\_______/')
        tass.screenWrite(frame,-1,_height-4,'press any key to exit')
        frames.append(frame)###
    elif sceneID==0:                                                      #INTRO
        frame = newFrame()####
        tass.screenWrite(frame,-1,-1,'1')
        frames.append(frame)###
        frame = newFrame()####
        tass.screenWrite(frame,-1,-1,'2')
        frames.append(frame)###

    for frame in frames:
        tass.screenDraw(frame)
        tass.sleep(_frameDelay)
    tass.pause() # between scenes



if __name__=='__main__':
    tass.init('Animation Test',_width,_height,'screen')
    tass.clear()
    for scene in range(1):
        try:
            show(scene)
        except KeyboardInterrupt:
            show(-1)
