"""

    Display series of numbers in infinite loop
    Listen to key "s" to stop
    Only works on Windows because listening to keys
    is platform dependent

"""

# msvcrt is a windows specific native module
import msvcrt
import time


# asks whether a key has been acquireds
def kbfunc():
    # this is boolean for whether the keyboard has bene hit
    x = msvcrt.kbhit()
    if x:
        # getch acquires the character encoded in binary ASCII
        ret = msvcrt.getch()
    else:
        ret = False
    return ret


# begin the counter
number = 1

# infinite loop
while True:

    # acquire the keyboard hit if exists
    x = kbfunc()

    # if we got a keyboard hit
    if x != False and x.decode() == 's':
        # we got the key!
        # because x is a binary, we need to decode to string
        # use the decode() which is part of the binary object
        # by default, decodes via utf8
        # concatenation auto adds a space in between
        print("STOPPING, KEY:", x.decode())
        # break loop
        break
    else:
        # prints the number
        print(number)
        # increment, there's no ++ in python
        number += 1
        # wait half a second
        time.sleep(0.5)
