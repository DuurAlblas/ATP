# Controller Code

## Intro
This language is based on BrainFuck but with a flair of my own. The idea is that you can code with your controller (except that you cannot input integers with your controller), for now only Nintendo controller buttons are implemented.
Feel free to expand on this project by implementing different types of controllers like a Playstation or XBOX controller.
In short, this language is able to do some very basic instructions like incrementing and decrementing a byte and moving around in the memory but I've also implemented functions, several comparisons and arithmatic instructions. 

It is important that every line of code is exactly that, 1 line of code. This is important since we have instructions like SELECT which jump to a instruction on a given line number.
Since this language is designed with microcontrollers in mind you have a limited memory stack, I have limited the memory stack to 64 times 32 bits. If you decide to go outside that range there will be undefined behavior so make sure you don't go outside that range, or define your own range when creating a Compiler object.

The language Controller Code is Turing-complete since it implements the same functionality as Brainfuck and more and Brainfuck is Turing-complete.

## Instructions
Instruction | Action |
|--|--|
| RIGHT | Increase the memory pointer by 1.|
| LEFT | Decrease the memory pointer by 1.|
| UP | Increment the byte at the memory pointer by 1.|
| DOWN | Decrement the byte at the memory pointer by 1.|
| BA *x* | Create a function, requires 1 integer parameter *x* which will be the indentifier of the function. The code between 'BA *x*' and 'AB' belongs to the function. This creates a Label to Branch to.|
| AB | Mark the end of a function. Jump back to the "linker register" address.|
| START *x* | Start function with the identifier *x*.|
| SELECT *x* | Jump to the instruction at line *x*.|
| ZL *x* *y* | Store the *x*th argument with a maximum of 2 in memory address *y*.|
| LB *x* | Sets the memory pointer to the integer *x*. Jumps to a memory address.|
| RB | Print the value of the address where the memory pointer currently points to (to use this functionality when compiling the `main.cpp` requires a : `extern "C" void print(int x)` function) |
| AX *x* | Sets the value of integer *x* on the memory address where the memory pointer is pointing to.|
| XA *x* | Sets the value of the memory address the memory pointer is pointing to to the value of memory address *x*.|
| XB *x* | Gets the value of the memory address the memory pointer is pointing to and places it in memory address *x*.|
| XY *x* *y* | Compares the values of the memory address at *x* and *y*. If the values are equal (==) execute the next instruction, if they aren't execute the instruction after that. |
| AY *x* *y* | Compares the values of the memory address at *x* and *y*. If the value of memory address *x* is larger than the value of memory address *y* (>) execute the next instruction, if it isn't execute the instruction after that.|
| BY *x* *y* | Compares the values of the memory address at *x* and *y*. If the value of memory address *x* is smaller than the value of memory address *y* (<) execute the next instruction, if it isn't execute the instruction after that.|
| YA *x* *y* | Multiplies the value in memory address *x* with the value in memory address *y* and assigns the result to memory address *x* (*x* \*= *y*).|
| YB *x* *y* | Add the value of memory address *y* to the value on memory address *x* (*x*+=*y*).|
| YX *x* *y* | Subtract the value of memory address *y* from the value on memory address *x* (*x*-=*y*).|
| BX | Stop execution of the code. Must be placed at the end of every file.|

## CLI Arguments
I have implemented CLI Arguments for ease of use. The following arguments have been implemented:
|Argument|Explanation|
|---|---|
| -h or --help | Use this argument to see every argument and it's parameters.
| -f or --file `code.coco`| By using this argument you can use a different file from `code.coco`. Note that the extension however must be `.coco`. If you use this option with the `-C` option the output file wil be the same file name except `.coco` is replaced by `.asm`. Using the `-o` option wil override this.
| -i or --input `int,int` | When you use the `ZL` instruction the application expects input from this option. The input integers must be `,` sepperated.
|-I| By using this option you specify you want to use the Interpreter functionality in stead of the Compiler functionality (This is the Default setting).
|-C| By using this option you specify you want to use the Compiler functionality in stead of the Interpreter functionality.
|-v or --verbose | If this option is used the application will print extra information.
|-o or --ouput `code.asm` | Use this option to change the output `.asm` file name.

## Interpreter
The Interpreter uses a dictionary named `interpreterDict` that contains the Instructions as keywords and the actual functionality as the value. The Interpreter also uses a class name `Platform` this class simulates a microcontroller environment by having the instruction list and another list that acts as memory. By keeping track of where we are in both lists using the instruction pointer and memory pointer we can freely move throughout the memory and execute all the code. Using this dictionary and simulated platform a user can write simple (or very advanced) applications.

The Interpreter functionality can be used by starting the application using the `-I` CLI argument.

## Compiler
The Compiler uses a dictionary named `compilerDict` that contains the Instrucitons as keywords and the actual functionality as the value, the same way the Interpreter does. All these instructions will generate strings with assembly code. The `Compiler.compile()` function wil return a single string containing all the instructions from the Controller Code that was supplied. Using the `Compiler.export()` function you can export the string to a `.asm` file. The Compiler wil add a label to each block of assembly that corresponds to a single line in Controller Code. These labels are used to jump around to line numbers in Controller Code.

The Compiler functionality can be used by starting the application using the `-C` CLI argument.

## Error-handling
Error handling is done purely on syntax level. There are checks to see whether functions have `AB` instructions and whether they are nested in eachother. Also whenever there is a `START` instruction the Lexer checks whether the supplied function identifier actualy exists.I've also implemented parameter checking. But even though there is a lot of syntax checking there is nearly no logic checking. When you've created code that's going to have undefined behavior that's on you so be vigilant when writing your code.

I've created a error class named `cError`, this class can be printed and be thrown using the `.throw()` method when you throw a error the python application with immediatly exit.

## Excercise Requirements
As mentioned before the language Controller Code is Turing-complete since Brainfuck is to and they implemented the same basic functionalities.

I have showcased loop (and also goto) functionality in the file `loopy.coco` which is explained in the section `Examples`.

I have implemented lambda's throughout the whole application but a good example is the dictionary `interpreterDict` in the file `interpreter.py` on line #6.

I have applied inheritance in `support.py` on line #59-#85. I have implemented the bare minimum but it is possible to create additional error types which could all be `throw()`'n. 

Where usefull I have implemented object printing, for example the `cError` class can be printed which is very usefull since you would want the user to see the errors.

In the file `support.py` I have implemented a decorator that checks whether the functions supplied filename actually exists. I have applied decorator function `check_existance(func : Callable[[str], Any])` on the function `readFile(filename: str)`.

Every function has type annotation using the `Typing` library.

I have implemented the required Higher Order Functions on the following lines:
|File| Line # | Function|
|---|---|---|
|`cc.py`|34|`map()`|
|`lexer.py`|19|`map()`|
|`lexer.py`|20|`map()`|
|`lexer.py`|91|`map()`|
|`support.py`|34|`map()`|
|`compiler.py`|394|`map()`|

My Interpreter support multiple functions in each file. When the code has been compiled you could pass parameters to the Controller Code using the R0-R3 registers. Functions can call other functions which I showcase in the section `Examples` in the `Double Recursive Function` example. Function results will be printed to the screen using a `extern "C" void print(int x)` function in the `main.cpp` when compiling or using the `print()` function of python during Interpreting, the instruction `RB` is used to print.

Extra functionality I have implemented is the `cError` class used to show the user errors, the class can be found in the `support.py` on lines #59-#85. 

## Examples
For my course I have to implement the following examples.

### Double Recursive Function

Here is a example of a double recursive function. It is used to determine whether a integer is a even or odd number.

First the example code in C++:

|Line # | C++ Code |
|--|--|
|1 | bool even(unsigned int n);
|2 | bool odd(unsigned int n);
|3 | bool odd(unsigned int n){
|4 |&emsp;if(n==0){return false;}
|5 |&emsp;return even(n-1);
|6 | }
|7 | bool even(unsigned int n){
|8 |&emsp;if(n==0){return true;}
|9 |&emsp;return odd(n-1);
|10| }

Next the same example code in Controller Code:

|Line# | Controller Code | Comments|
|--|--|--|
|1 | BA 2| Create a function with the identifier 2 (this is the `even` function)
|2 | XY 1 2| Compare the value in memory address 1 to the value in memory addres 2
|3 | SELECT 18| If they are equal go to line 18
|4 | DOWN| Else lower the value on the memory address where the memory pointer is pointing to (1)
|5 | START 1| Start the function with identifier 1
|6 | AB| End of the function with identifier 2
|7 | BA 1| Create a function with the identifier 1 (this is the `odd` function)
|8 | XY 1 2| Compare the value in memory address 1 to the value in memory addres 2
|9 | SELECT 12| If they are equal go to line 12
|10| DOWN| Else lower the value on the memory address where the memory pointer is pointing to (1) 
|11| START 2| Start the function with identifier 2
|12| AB| End of the function with identifier 1 return to where you were called
|13| AX 7| Set the value of the memory address the memory pointer (1) is pointing to to the value 7 (we want to know if 7 is even or odd)
|14| RIGHT| Increase the memory pointer by 1
|15| AX 0| Set the value of the memory address the memory pointer (2) is pointing to to the value 0
|16| LEFT| Decrease the memory pointer by 1
|17| START 2| Call the function with identifier 2 (`even`) to determine whether the value on memory address where the memory pointer is point to is even
|18| UP| Raise the value on memory address where the memory pointer is pointing to (1)
|19| RB | Print the value of the memory address where the memory pointer is currently pointing to which is 1; 0 or false for a odd number, 1 or true for a even number (since 7 is odd the result would be 0)
|20| BX | Stop execution of the code

### Loopy function

This is a example of a function that will loop. Inside the loop we will calculate the sum of the given integer and decrease it with 1 in each loop until it reaches 0.

First the example code in C++:

|Line # | C++ Code |
|--|--|
|1 | unsigned int summy(unsigned int n){
|2 |&emsp;unsigned int result = 0;
|3 |&emsp;while(n>=1){
|4 |&emsp;&emsp;result += n;
|5 |&emsp;&emsp;n--;
|6 |&emsp;}
|7 |&emsp;return result;
|8 |}

Next the same example code in Controller Code:

|Line # | Controller Code | Comments|
|--|--|--|
|1 | BA 1| Create a function with the identifier 1 (this is the `summy` function)
|2 | RIGHT| Increase the memory pointer by 1
|3 | AX 0| Set the value of the memory address where the memory pointer (2) is pointing to to 0 (this is the `result` variable)
|4 | RIGHT| Increase the memory pointer by 1
|5 | AX 0| Set the value of the memory address where the memory pointer (3) is pointing to to 0 (the 0 comparison in the while condition)
|6 | LB 1| Set the memory pointer to the integer 1 (`n`)
|7 | XY 1 3 | Compare the value at memory pointer 1 to the value at memory pointer 3 (0)
|8 | SELECT 15| If the values are equal go to line 15
|9 | YB 2 1 | Adds the value at the memory address 1 to the value at memory address 2 (`result += n`)
|10| DOWN | Decrease the value at the memory address where the memory pointer is pointing to by 1
|11| SELECT 7 | Go to line 7 to compare again
|12| AB | End of the function with the identifier 1
|13| AX 5 | Set the value of the memory address where the memory pointer is pointing to to the value 5
|14| START 1 | Start the function with the identifier 1
|15| XA 2 | Copy the value at the memory address of memory pointer 2 to the memory address where the current memory pointer is pointing to
|16| RB | Print the value of the memory address where the memory pointer currently points to
|17| BX | Stop execution of the code