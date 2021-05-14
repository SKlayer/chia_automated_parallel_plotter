set /p TEMP=Temporary Device :
set /p TARGET=Target Device:
set /p PLOTS=Amount of parallel plots:

for /l %i in (1,1,%PLOTS) do start cmd /c chia plots create -k 32 -n 1 -b 3390 -r 2 -t %TEMP -d %TARGET
