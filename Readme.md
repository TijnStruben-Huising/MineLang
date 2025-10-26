# Welcome to a new innovative language
Prepare to combine the fun of games with the joy of programming

# Paradigm

MineLang is similar to assembly but with a new paradigm of memory management, say goodbye to register issues, pointers, and mmaps, this is all managed for you in a revolutionairy, memory safe new concept.
The memory starts of as an infinite minesweeper board without any bombs, you may move the cursor, place or remove bombs and use the number in each square to do jumps in the code.

# Requirements
Python, eh something decently modern will work
gcc, it's hard coded and im too dumb as a rock to change that
bash or something like it

# Synthax

## Operations
direction: . . | . + | . - | + . | - . | + - | - + | + + | - -
int : i64 in hex form
OP : MOV \<direction\> | GOTO \<int\> | DO \<int\> \<int\> \<int\> \<int\> \<int\> \<int\> \<int\> \<int\> \<int\> | FLAG | PLACE | SYSCALL | READ | WRITE | \<int\>

Note: SYSCALL not yet implemented

MOV: move the cursor up or down along x and y (+ is for up, - is for down, . is for stay) (first one is for x, second is for y)

GODO:
    self explanatory, labels are created by just writing an int (if the label is repeated, it is undefined behavior)

FLAG:
    remove bomb if there, if no bomb, the program crashes

PLACE:
    add bomb, if there is already one, program crashes

READ:
    reads bit from stdin, places bomb on cursor if it is 1, else not
WRITE:
    writes bit to stdout: 1 if there is bomb, else 0
DO:
    reads number of current square, performs a goto, if the current square is a bomb, crashes

# Usage

mine \<origin file\> \<output file\>
(will write to a \<origin file\>.s file too)
