@setlocal enableextensions
@cd /d "%~dp0"
@echo off
python update.py %*

net stop Apache2.4
net stop FusionService

net start Apache2.4
net start FusionService

pause