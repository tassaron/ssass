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

    For more advanced objects, create an EntityLayer object. This functions sort
of like a Screen, except it keeps track of traits and data about the entities on
the layer. When painted with a background Screen specified, it'll draw these
entities on top of the background, allowing (for example) bouncing balls or
particle effects to be easily created and displayed. The background's screen
table is not affected by the EntityLayer's paint() method.

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
#  STUFF TO DO BEFORE I CONSIDER IT VERSION 1.0:
#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=#

complete EntityLayer enough to make Jezzball
less messy handling of q/ctrl+c - it works really illogically atm
multithreaded input support - take keypresses in the background while animating
color support
finish line()
create an exe for Windows
slightly better sound support
Linux support for arrow keys
ability to draw diamonds using a radius
better error handling
get rid of all the Width_-1 stuff. shouldn't have to -1 so often (maximumX, maximumY)
