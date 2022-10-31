@echo off
REM allows iterable to be updated
setlocal EnableDelayedExpansion
REM set j to initial sample number for automation
set j=1
for /L %%i in (1,1,64) do (
    set new_file_name=agnw_2360_cplx_s!j!.npy
    REM Open blender with base blend file and execute python script on it to collect data from the model
    REM Change path accordingly
    "C:\Program Files\Blender Foundation\Blender 3.2\blender.exe" --enable-autoexec agnw_2360_cplx.blend -P agnw_script_2360_cplx.py
    REM temporary file name produced from .py script is updated, avoids overwriting data during iteration
    move agnw_temp.npy !new_file_name!
    echo Produced !new_file_name!
    set /a j+=1
)

    
