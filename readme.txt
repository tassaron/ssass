-=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=-

            Tassaron's Somewhat Satisfactory Script Simplifier
                + Somewhat Satisfactory ASCII Screen Simplifier
                by tassaron - 2013-14

-=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=-

Requires: Python 3.4 (probably any subversion of 3)
That's it, that's all. Should work anywhere Python does. It definitely works in
my test environments, WinXP and Ubuntu 14.

'Tis basically a big file you can import that simplifies a lot of basic stuff
I always end up writing functions for anyway, + simplifies some less basic stuff
like an ascii screen (a list of rows which are lists of columns) with simple
commands to draw on it.

-=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=-

This is mainly a place for experiments. Constructive criticism is super welcome.
Follow me on Twitter: http://www.twitter.com/tassaron
The "tassaron" account on Github is also me. I lost the password.

-=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~==~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=-
TODO:
less messy handling of q/ctrl+c - it works really illogically atm
better error handling
get rid of all the Width_-1 stuff. shouldn't have to -1 so often
color support
sound support
Linux support for arrow keys
history support (backspaces goes back through screens in order they were drawn)
add a way to use screens directly, not use global screens list, etc
addBorders, rippleDraw, whatever
some kind of way to check sizes easily
ability to draw shapes like circles and diamonds using a radius
save an area to an object, to be copied in at an x,y coord in a screen
  object could also have its own attributes. useful for games!
