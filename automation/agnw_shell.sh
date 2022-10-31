#!/bin/sh
file_prefix="agnw_s"
file_suffix=".npy"
for i in {0..10..20};
do
  /mnt/c/Program\ Files/Blender\ Foundation/Blender\ 3.2/blender.exe -b agnw_auto.blend -P agnw_script.py

##  'C:\Program Files\Blender Foundation\Blender 3.2\blender.exe' -b agnw_auto.blend -P agnw_script.py
  new_file_name="$name_prefix$i$name_suffix"
  mv agnw_temp.npy new_file_name
done

