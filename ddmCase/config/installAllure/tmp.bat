
  @echo off
  if sys==sys (
   set regPath= HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session" "Manager\Environment
  ) else (
   set regPath= HKEY_CURRENT_USER\Environment
  )
  set key=Path
  set value=D:\Program Files (x86)\ffmpeg\bin
  :: 判断是否存在该路径
  reg query %regPath% /v %key% 1>nul 2>nul
  if %ERRORLEVEL%==0 (
   :: 取值
   For /f "tokens=3* delims= " %%i in ('Reg Query %regPath% /v %key% ') do (
      if "%%j"=="" (Set oldValue=%%i) else (Set oldValue=%%i %%j)
   )
  ) else Set oldValue="."
  :: 备份注册表
  reg export %regPath% %~dp0%~n0.reg
  :: 写入环境变量
  if "%oldValue%"=="." (
   reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%value%" /f
  ) else (
   reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%oldValue%;%value%" /f
  )
  