#!/usr/bin/python3

from tass import *

def draw():
    page.clear()
    page.line((x, y),(column,row))
    page.fill('#')
    page.paint()
    if not sleep():
        quit()

if __name__=='__main__':
    Width_=80; Height_=32
    init('Spinner',width=Width_, height=Height_)
    x = 39; y = 19
    page = screen()
    while True:
        column = Width_-1
        for row in range(Height_-1):
            draw()
        #for column in range(Width_-1,-1,-1):
        #    draw()
        column = 0
        for row in range(Height_-1, -1, -1):
            draw()
        #for column in range(Width_-1):
        #    draw()
