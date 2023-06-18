# snake

need i say more?

## preface

a while ago i learned some dvorak, got the basics. 
getting increasingly more interested in the world of neovim,
i decided to drop the dvorak, because the thought of relearning 
the vim-bindings in dvorak didnt tickle my fancy.

yesterday at 3 am i got the idea to try dvorak again.
this wasnt all random, i was partially inspired by
[theprimeagens](https://www.youtube.com/c/theprimeagen) videos.
he is a dvorak + nvim user, as per my understanding.
in so deciding, i had to get some practice in.
what better way could there be to practice than to write up a snake game in python with
unfamiliar modules (namely curses and using enums and collections.deque) -
and then publish it alongside a readme due to some fancy never-before-seen bugs?

quite the series of events that lead to this repo being created. and all for a game of snake...

## usage

you will need to at the very least install the curses library for python3 to run this.
when all dependencies are ready, grab the python file and run it normally in a terminal.

curses will hijack it and do its thing - it should handle os stuff, but what do i know?

the game will start frozen. begin by moving in a direction using the corresponding arrow keys.

if you care to, you may remap to wasd (or ,aoe for dvorak-gamers) through the inputkeys enum.

## known bugs

the bug itself is weird. when tail and head enum values are the same, ie both are 'o',
moving the character either down or to the right after having eaten food and gained an initial tail,
will result in the immediate resolution and termination of the program. moving up and to the left is fine.

the reason i am writing this: why does the game not work properly when the head and tail enum values are
set to the same character? to my knowledge of enums in python, the values shouldnt really matter
the way i use them in the code, unless i have made some grand oversights.

i believe the bug might then lie with curses. still i do not know for certain.

what i do know (possibly) is that it failed in the get_player_head function.

## reflections

every key stroke from start to finish on this project and elsewhere has been
through dvorak. it has been both painful and fun.

most of all it has been slow

it took me about 5 or 6 hours of work, embarrassingly enough. and i still have bug i dont
understand. not to mention i havent even added a sort of fixed frame timer.

besides all this, some parts of the code and the way i reasoned about it was pretty good,
i must say. i liked using enums and dataclasses, they often yield very beautiful code.

but now i have no more patience. enough typing.
