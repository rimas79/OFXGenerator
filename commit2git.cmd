@echo off
call ../set_proxy.cmd
rem git add  .
git commit -a -m"Minor changes"
git push origin master