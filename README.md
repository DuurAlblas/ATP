# Controller Code

## Intro
This language is based on BrainFuck but with a flair of my own. The idea is that you can code with your controller (except that you cannot input integers with your controller), for now only Nintendo controller buttons are implemented.
Feel free to expand on this project by implementing different types of controllers like a Playstation or XBOX controller.
In short, this language is able to do some very basic instructions like incrementing and decrementing a byte and moving around in the memory but I've also implemented functions. 

## Instructions
| Instruction | Action |
|--|--|
| RIGHT | Increase the memory pointer by 1.|
| LEFT | Decrease the memory pointer by 1.|
| UP | Increment the byte at the memory pointer by 1.|
| DOWN | Decrement the byte at the memory pointer by 1.|
| BA *x* | Create a function, requires 1 integer parameter which will be the indentifier of the function. The code between 'BA *x*' and 'AB' belongs to the function. This creates a Label to Branch to.|
| AB | Mark the end of a function. Jump back to the Link Register address.|
| START *x* | Start function with the identifier *x*.|
| SELECT *x* | Jump to the instruction at line *x*.|
| LB *x* | Sets the memory pointer to the integer *x*. Jumps to a memory address.|
| RB *x* | Print the value of the address where the memory pointer points to.|
| XA *x* | Copy the value of memory address *x* to the address of the memory pointer.|
| AX *x* | Sets the value of memory address *x* to the value of the memory pointer.|
| XY *x* *y* | Compares the values of the memory address at *x* and *y*. If the values are equal (==) execute the next instruction, if they aren't execute the instruction after that. |
| AY *x* *y* | Compares the values of the memory address at *x* and *y*. If the value of memory address *x* is larger than the value of memory address *y* (>) execute the next instruction, if it is execute the instruction after that.|
| BY *x* *y* | Compares the values of the memory address at *x* and *y*. If the value of memory address *x* is smaller than the value of memory address *y* (<) execute the next instruction, if it is execute the instruction after that.|
| YX | Stop execution of the code. Must be placed at the end of every file.|

## Interpreter


## Compiler

## Error-handling

## Tutorial

## Examples
### Double Recursive Function

|line # | code | 
|--|--|
|1 | 