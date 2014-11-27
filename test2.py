#!/usr/bin/python3
import tass

if __name__=='__main__':
    tass.init('Screen Drawing Test',79,40,'screen')
    screen = tass.screenInit()
    # fill every other line with 0s or 1s
    for row in range(40):
        if row % 2 == 0:
            tass.screenFill(screen, 'row '+str(row),'with 0')
        else:
            tass.screenFill(screen, 'row '+str(row),'with 1')
    # because otherwise it's hard to see what's happening
    while True:
        tass.screenDraw(screen)
        tass.pause()
        tass.screenAreaMove(screen, rows=(25,35), cols=(2,5), x=5, y=6)
        tass.screenDraw(screen)
        tass.pause()
        tass.screenAreaMove(screen, rows=(4,7), cols=(10,15), x=35, y=15)
