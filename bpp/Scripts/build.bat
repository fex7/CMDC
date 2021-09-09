@Echo off
SetLocal


goto:docstringend
	file: build.bat
	When you run this script, it will compile the BPP utility.
	Everything needed for autonomous BPP work will be compiled,
	all BPP modules, bpp.py itself, and even Python will be compiled.
	Everything compiled will go to the "Dist" folder -
	which is located in the root of the BPP folder.
	All that is needed from there is a "bpp.exe" file.
	Do not touch the rest.
	"bpp.exe" - leave it there.

	Command Line parameters:
		Param: "-o" is optimizing mode (DLLs cleanup)
		Param: "--help" is basic help

	In order for the compiler to work, it is necessary:
		1. Python
		2. Cython (For compiling modules)
		3. Nuitka (For compiling bpp.py)
		4. C Compiler
	Perhaps something else depends on your system.
	
:docstringend

:: Constants
set dist_path=%~dp0\..\Dist
set bppylib_path=%~dp0\..\Lib\BpPyLib
set pybpp_path=%~dp0\..\bpp.py
set cleaning_directory=%dist_path%\tmp_cleaningdir_17


goto :EndOfDefines

:: Common return definition
:return
:{
	endlocal
	goto :end
:}


:: Completion of the script
:end
:{
	if errorlevel 0 (
		:goodend
		exit /b 0
	) else (
		:errend
		exit /b 1
	)
:}


:Print_PythonNotFound ()
:{
	::: Print Python not found message :::
	echo. & echo.
	echo | set /p="build.bat::Error: Python interpreter not found or "
	echo | set /p="not in 'Path' environment variable"
	echo. & echo.
:}
(goto:return)


:Print_CythonizeNotFound ()
:{
	::: Print Cythonize not found message :::
	echo. & echo.
	echo | set /p="build.bat::Error: Cythonize was not found or "
	echo | set /p="is missing from the 'Path' environment variable"
	echo. & echo.
:}
(goto:return)


:Print_NuitkaNotFound ()
:{
	::: Print Nuitka not found message :::
	echo. & echo.
	echo | set /p="build.bat::Error: Nuitka was not found or "
	echo | set /p="is missing from the 'Path' environment variable"
	echo. & echo.
:}
(goto:return)


:Print_ModuleNotExist (module_name)
:{
	::: Print "module" not exist message :::
	::: Params:
	:::     module_name - Name of the module that will be printed

	setlocal
	set param1=%1
	if not defined param1 goto:return
	echo. & echo.
	echo | set /p="build.bat::CompilationCriticalError: The module '%param1%' was not compiled, "
	echo | set /p="so the whole compilation was not completed successfully"
	echo. & echo.
	endlocal
:}
(goto:return)


:Print_ExecutableNotExist ()
:{
	::: Prints out if bpp.py is not compiled :::
	echo. & echo.
	echo build.bat::CompilationError: The 'bpp.py' was not compiled.
	echo. & echo.
:}
(goto:return)


:main (argv)
:{
	::: Main function :::
	
	::: Params:
	:::     argv -- command line arguments

	:: Parsing command line arguments
	set param1=%1
	set param2=%2
	if defined param2 (
		echo CommandLineError: build.bat you cannot specify more than one parameter & goto:errend
	)
	if defined param1 (
		if "%param1%" equ "-o" (
			set optimize=1
		) else if "%param1%" equ "--help" (
			echo build.bat [--help][-o] --- Param '-o' is optimizing mode & goto:goodend
		) else (
			echo CommandLineError: The '%param1%' unsupported parameter & goto:errend
		)
	) else (
		set optimize=0
	)

	:: Checking dependencies
	echo You have launched a builder for the BPP project.
	echo After compilation, you will get the 'bpp.exe' executable file in the 'Dist' folder. & echo.

	echo Checking dependencies started...
	call python --help > nul
	if %errorlevel% neq 0 (
		call :Print_PythonNotFound & goto:errend
	)
	call cythonize --help > nul
	if %errorlevel% neq 0 (
		call :Print_CythonizeNotFound & goto:errend
	)
	call python -m nuitka --help > nul
	if %errorlevel% neq 0 (
		call :Print_NuitkaNotFound & goto:errend
	)
	echo The checks were successful! & echo. & echo.
	echo Start Building... & echo. & echo.
	if "%optimize%" equ "1" echo Warning: Build started in Optimization mode! & echo. & echo.

	:: Creating the necessary folders
	mkdir "%dist_path%" > nul
	mkdir "%dist_path%\Lib" > nul
	mkdir "%dist_path%\Lib\BpPyLib" > nul

	:: Adds __init__.py file
	copy /y "%bppylib_path%\__init__.py" "%dist_path%\Lib\BpPyLib" > nul

	:: Compilation BPP library
	call cythonize -i -3 "%bppylib_path%\abcs.py"
	call cythonize -i -3 "%bppylib_path%\bppcli.py"
	call cythonize -i -3 "%bppylib_path%\compat.py"
	call cythonize -i -3 "%bppylib_path%\cores.py"
	call cythonize -i -3 "%bppylib_path%\exceptions.py"
	call cythonize -i -3 "%bppylib_path%\includer.py"
	call cythonize -i -3 "%bppylib_path%\precommands.py"
	call cythonize -i -3 "%bppylib_path%\preprocessor.py"
	call cythonize -i -3 "%bppylib_path%\prompts.py"
	call cythonize -i -3 "%bppylib_path%\structures.py"
	call cythonize -i -3 "%bppylib_path%\utils.py"
	call cythonize -i -3 "%bppylib_path%\version.py"
	
	:: Compiling the 'bpp.py' utility
	echo. & call python -m nuitka --standalone --mingw64 --output-dir="%dist_path%" "%pybpp_path%"
	
	:: Cleaning
	move /y "%bppylib_path%\*.pyd" "%dist_path%\Lib\BpPyLib" > nul
	move "%dist_path%\bpp.dist\*.*" "%dist_path%" > nul
	del /q "%bppylib_path%\*.c" > nul
	rmdir /s /q "%dist_path%\bpp.dist" > nul
	rmdir /s /q "%dist_path%\bpp.build" > nul

	:: Optimizing
	if "%optimize%" equ "1" (
		mkdir "%cleaning_directory%" > nul
		move "%dist_path%\*.pyd" "%cleaning_directory%" > nul
		move "%dist_path%\*.dll" "%cleaning_directory%" > nul
		move "%cleaning_directory%\python*.dll" "%dist_path%" > nul
		rmdir /s /q "%cleaning_directory%" > nul
	)

	:: Checking compiled files
	set errorflag=0
	if not exist "%dist_path%\Lib\BpPyLib\abcs*.pyd" call :Print_ModuleNotExist abcs.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\bppcli*.pyd" call :Print_ModuleNotExist bppcli.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\compat*.pyd" call :Print_ModuleNotExist compat.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\cores*.pyd" call :Print_ModuleNotExist cores.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\exceptions*.pyd" call :Print_ModuleNotExist exceptions.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\includer*.pyd" call :Print_ModuleNotExist includer.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\precommands*.pyd" call :Print_ModuleNotExist precommands.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\preprocessor*.pyd" call :Print_ModuleNotExist preprocessor.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\prompts*.pyd" call :Print_ModuleNotExist prompts.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\structures*.pyd" call :Print_ModuleNotExist structures.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\utils*.pyd" call :Print_ModuleNotExist utils.py & set errorflag=1
	if not exist "%dist_path%\Lib\BpPyLib\version*.pyd" call :Print_ModuleNotExist version.py & set errorflag=1
	if not exist "%dist_path%\bpp.exe" call :Print_ExecutableNotExist & set errorflag=1
	
	:: User choice if something didn't compile
	if "%errorflag%" equ "1" (
		choice /m "Do you want to complete the compilation? Some BPP modules did not compile!"
		if errorlevel 2 (
			rmdir /s /q "%dist_path%" > nul
			echo. & echo. & echo Compilation failed!
			goto :errend
		)
		echo. & echo. & echo Warning: Is the building finished, but with errors
		goto :errend
	)
	echo. & echo. & echo Building completed successfully!
:}
(goto:return)


:EndOfDefines

:: Point of entry
call :main %*
goto :end
