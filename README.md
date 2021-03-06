# pyjs-compiler
Python to JavaScript Compiler. Compiles Python3 to the widely supported ES3 JavaScript including some mild minifications of code.

# Quick Start
1. Write your Python3 program
2. Open a terminal
3. Compile your Python3 into JavaScript
```
> python3 compiler.py "mymodule.py"
```
4. View your JavaScript code and HTML in the "build/" directory
5. Serve your index.html file to see the magic

## Web APIs
Python is translated directly to JavaScript case sensitively so all Web APIs such as; document, window, etc. may be used if typed exactly to match JavaScript casing and method names.

## Supported
**Literals**
* str,int,float,decimal,f-strings,etc.  

**Variables**
* everything except packing and unpacking  

**Expressions**
* everything except Matrix Multiplication and kwargs  

**Subscripting**
* everything except advanced slicing (e.g. list[1:2, 3])  

**Comprehensions**
* Not supported  

**Statements**
* everything exept packing and unpacking  

**Imports**
* supported but import aliases are not supported  

**Control Flow**
* everything except the enumerate function  
* with for context managers  

**Function and Class Definitions**
* everything except kwargs, decorators, and yield  

**Async Await**
* not supported because JavaScript is already asynchronous  

**Modules**
* converts python modules to js module pattern variables to reduce namespace use in code  
  
**Builtins**
* range, max, min, abs, isinstance, len, getattr, map, print, sum, type, zip  
  
## Coming Soon...
* import alias support  
* decorator support  
* comprehension support  
* Python standard modules support (e.g. datetime, collections, etc.)  
* Web API for Component based Web Apps  
