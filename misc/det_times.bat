set /p TEMP=Temporary Device :
set /p TARGET=Target Device:
set /p PLOTS=Amount of parallel plots:

FOR /L %%i IN (1,1,100) DO (
	IF /I %%i LEQ %PLOTS% (
		echo %%i
		start cmd /c chia plots create -k 32 -n 1 -b 3390 -r 2 -t %TEMP% -d %TARGET%
		PAUSE
	)
)
