@Echo off
SetLocal


:: Constants
set BATBPP=%~dp0\bpp.bat

:: Variables
set ret_main=null

goto :EndOfDefines

:return
:{
	endlocal
	goto:eof
:}

:help ()
:::Help for cmdc utility:::
:{
	echo CMDC Utility
	echo cmdc.bat [-o output_file] [-s source_file] [-r]
:}
(goto:return)

:main (argv)
:::Main function.:::
:{
	setlocal
	set arg1=%1
	if not defined arg1 (
		call :help
	) else (
		call "%BATBPP%" %*
	)
	endlocal & (
		goto:return
	)
:}
(goto:return)

:EndOfDefines

call :main %*
exit /b %ErrorLevel%