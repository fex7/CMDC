@Echo off
SetLocal


:: Constants
set PYTHON=%~dp0\..\Python\v3.8.5\python.exe
set PYBPP=%~dp0\..\BPP\bpp.py
set BLIB=%~dp0\..\BLib
set BATPATH=%~dp0\..\BLib
set BATLIB=%~dp0\..\BLib

:: Return variables
set ret_main=null

:: Definitions
goto :EndOfDefines

:: Common return definition
:return
:{
	endlocal
	goto :eof
:}

:main (argv)
:::Main function.:::
:{
	call "%PYTHON%" "%PYBPP%" %*
:}
(goto:return)


:: End of definitions
:EndOfDefines

call :main %*
exit /b %ErrorLevel%