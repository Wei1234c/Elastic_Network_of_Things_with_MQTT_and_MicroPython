REM python -m memory_profiler 2_start_client.py > profile.txt
REM pause

REM python D:\Python\Scripts\mprof run _demp\2_start_client.py
REM python D:\Python\Scripts\mprof plot
REM pause



python -m cProfile 2_start_client.py > profile.txt
pause
