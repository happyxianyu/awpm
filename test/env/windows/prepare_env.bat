@REM just a demo

@ECHO off

CALL :NORMALIZEPATH %~dp0
SET PRNT_PATH=%RETVAL%

SET "PATH=%PRNT_PATH%\export;%PATH%"


:: ========== FUNCTIONS ==========
EXIT /B

:NORMALIZEPATH
  SET RETVAL=%~f1
  EXIT /B

