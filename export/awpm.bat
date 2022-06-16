@REM aw project manager

@echo off
set PYTHONPATH=%~dp0\..\src;%PYTHONPATH% 

python -m awpm %*



