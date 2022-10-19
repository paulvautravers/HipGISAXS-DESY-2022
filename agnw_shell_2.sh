#!/bin/sh
# components of updated file name 
file_prefix="agnw_2360_s"
file_suffix=".npy"
# for loop from 1 to 256, in integer steps
for i in {1..256..1};
do
  #blender opened with base file and python script applied to it
  blender agnw_2360_cplx.blend -P agnw_script_2360_cplx.py
  #new file name constructed and python output overwritten
  new_file_name="agnw_2360_s$i.npy"
  mv agnw_temp.npy $new_file_name
  echo "Sample data $new_file_name produced!"
  
  #hipgisaxs simulation
  python3 main_u1.py $i
  echo "Sample $i GISAXS pattern produced!"
done

