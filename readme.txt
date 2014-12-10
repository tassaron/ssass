#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#
#                               ssass.py
#             The Somewhat Satisfactory ASCII Screen Simplifier
#                       an experiment by tassaron
#                          written Nov-Dec 2014
#
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

    Initialize the module with init().

    Use a Screen object to display stuff to the user. It comes with a bunch of
handy selector methods like area(), cell(), line(), and everything(), as well as
drawing functions like fill() and write(). Easy to use and capable of animating
at low framerates.

    Use a Brain object to assist with doing a large number of big actions (like
filling a huge area with random characters). These actions may cause lag if they
need to request too many random numbers. A brain object generates a store of
random numbers at once and allows the module to reuse previously generated numbers
from this store while new numbers are being generated.

    Other fun little features: Get current date and time in various formats using
getTimestamp(). Get keypresses and respond to them immediately using getInput().
Debug numerous problems by enabling debug().

    Coming Someday: colour support, sound support

    Broken Things: line(), demo.py

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

    Requires: Python 3.4 (probably any subversion of 3). That's it, that's all.
Should work anywhere Python does. It definitely works in my test environments,
WinXP and Ubuntu 14. I even remembered to use Windows line endings in my text
editor so this file would open properly in Notepad :o)

    This is mainly an experiment; I don't really expect it to be super useful.
I'm just trying to reinvent the wheel for fun and as a learning process. Constructive
criticism is super welcome. Follow me on Twitter: http://www.twitter.com/tassaron

    The "tassaron" account on Github is also me. I lost the password.


#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#
#  TO DO:
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

less messy handling of q/ctrl+c - it works really illogically atm
better error handling
get rid of all the Width_-1 stuff. shouldn't have to -1 so often (maximumX, maximumY)
color support
sound support
Linux support for arrow keys
history support (backspaces goes back through screens in order they were drawn)
addBorders, rippleDraw, whatever
some kind of way to check sizes easily
ability to draw shapes like circles and diamonds using a radius
save an area to an object, to be copied in at an x,y coord in a screen
  object could also have its own attributes. useful for games!
could other programs' output be piped into a screen?
