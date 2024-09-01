# This utility preprocesses BAT files

it processes only the command -
["#include"](https://en.wikipedia.org/wiki/Include_directive#C/C++ "Wikipedia: Include directive in C/C++") at the moment.
This command performs the inclusion of another BAT file.
syntax:  
> :#include "somefolder\some.bat"  
> :#include "%someenvpath%\sss.hbat"

The two main options are either just a relative or absolute path, or through environment variables.

---

## Notes

* A colon at the beginning is required.

* After starting the preprocessor, this expression will be replaced by the contents of the file.

* Quotes on both sides are required.

* If percent signs are used in quotes - then it will expand the path in variable environments.
This means that before starting the preprocessor,
you have to create this environment variables,
otherwise nothing will come of it.

* You cannot include the main file.
For example, if the main file is some.bat,
then it is impossible to include it itself, not the file that has the same name, namely this file cannot be included.

---

## Supported file extensions for "include" command

* .bat
* .cmd
* .hbat
* .hb

---

## An example of how BPP works

> file: test.bat

    echo hello world  

---

> file: main.bat

    @echo off  
    echo 123  
    :#include "test.bat"  
    exit /b 0

---

> After preprocessing main.bat:

    python bpp.py -s main.bat -o main2.bat

---

> file: main2.bat

    @echo off  
    echo 123  
    ::File - "test.bat"  
    ::------------------------------ (  
    
    echo hello world  
    
    ::------------------------------ )  
    exit /b 0  

---

In short, this inclusion system is very similar to the one in the C language.

---

## bpp.bat and [bpp.py](../bpp.py) utility basic help

    BPP Utility Help
    This utility preprocesses bat files.

    Syntax:
        python bpp.py -s | --source <source file> [-o | --output <output file>] [-r | --run]

    Options:
        --source | -s <source file>  
        [--output] | [-o] <output file>  
        [--run] | [-r]  
        [--help] | [-h]  
        [--version]  

    Examples:
        $ python bpp.py --output newbat.bat --source mybat.bat
        $ python bpp.py -o script.bat -s script2.bat --run
        $ python bpp.py --run -s script.cmd
        $ python bpp.py -r -s script.cmd

***The -r or --run option runs the file via cmd.exe after preprocessing.***

---

## Good syntax for Include directive

    :#include "hello.hbat"
    :#include "folder\hello3.hb"
    :#include "C:\hello2.bat"
    :#include "%hellobat_path%"
    :#include "%hello_path%\hello4.hbat"

---

## Bad syntax for Include directive

    :#include
    :#include "
    :#include ""
    #include "hello.hbat"
    :include "C:\hello2.bat"
    :#include C:\hello2.bat"
    :#include "%hello_path%
    :#include C:\hello2.bat
    :#include "C:\hello2.bat"ahhhh
    :#include ahhhh"C:\hello2.bat"

---

## **`build.bat`** - builds the entire BPP utility

This utility just compiles all BPP modules and after **`bpp.py`**.
But to compile you need the following tools, which must be added to the Path environment variable:

1. Python interpreter (preferably something from version 3.8)
2. Cython (More specifically Cythonize)
3. Nuitka (For compiling **`bpp.py`**)
4. C Compiler (GCC)

And maybe something else depending on the version of these tools.

[build.bat](../Scripts/build.bat "File: build.bat") takes one parameter, which is '-o'.
If you specify this parameter, then all unnecessary files will be deleted.
The compiled binaries will be in the 'Dist' folder, which is located at the root of the BPP folder.
