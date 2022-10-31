# HipGISAXS-DESY-2022
Repository containing the code developed during DESY 2022 summer student program.

This project focused on the development of real space models of cellulose nanofibril (CNF) and silver nanowire (AgNW) films and simulating GISAXS scattering patterns from this data, using HipGISAXS-2.0. The code found here covers the data collection from blender, the simulation code from hipGISAXS-2.0., automation code to be ran locally or remotely (Maxwell @ DESY ) and various analysis codes that I developed as well. 

Contents:
- agnw_2360_cplx.blend; blend basis file for use with python and shell script to create agnw blender film
- agnw_auto_2360_cplx.bat; .bat file to automate data collection from blender on local system
- agnw_script_2360_cplx.py; contains code to develop thin film model from blend file and collect data
- agnw_shell.sh; shell file to automate HipGISAXS-2.0 simulation process
- agnw_shell_2.sh ; shell file to automate data collection from blender and HipGISAXS-2.0 simulation process together
- area_coverage.ipynb; jupyter script to calculate area coverage from a top down image of the blender model
- averaging_images.ipynb; jupyter script to average many images together, using either all images or subgroups

