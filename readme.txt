-=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=-

            Tassaron's Somewhat Satisfactory Script Simplifier
                + Somewhat Satisfactory ASCII Screen Simplifier
                by tassaron - 2013-14

 -=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=-

Requires: Python 3.4 (probably any subversion of 3)
That's it, that's all. Should work anywhere Python does. It definitely works in
my test environments, WinXP and Ubuntu 14.

'Tis basically a big file you can import that simplifies a lot of basic stuff
I always end up writing functions for anyway, + simplifies some less basic stuff
like an ascii screen (a list of rows which are lists of columns) with simple
commands to draw on it.

-=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=-

This is mainly a place for experiments. Constructive criticism is super welcome.
Follow me on Twitter: http://www.twitter.com/tassaron

-=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=-
TODO:
less messy handling of q/ctrl+c - it works really illogically atm
make screenFill better (should use keyword args and accept areas)
better error handling
Linux support for arrow keys
clean up code to use less globals and be neater in parts
color support (using ansi.sys and control codes?) (definitely possible)
sound support
