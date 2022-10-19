"""
Python code written to randomise a basis array of nanowires and let them settle on a substrate
in Blender. This relies on the initial blender file having a substrate and series of wires that 
are placed in a collection 'AgNW'. Outputs numpy file containing scales, positions and euler
rotations of nanowires
Paul Vautravers 19/09/2022
"""
import bpy 
import numpy as np
import random
import mathutils

#assignment of nanowire collection
units = bpy.data.collections['AgNW']
    
def get_xyz_angles():
#function to collect the xyz coords and euler angles of each agnw
#returns xyz coords and euler angles
    
    for i, obj in enumerate(units.all_objects):
        
	#positions and angles are collected in temporary array
        xyz_coords_euler_angles_temp = np.hstack((obj.matrix_world.to_translation()[:],obj.matrix_world.to_euler()[:]))
        
        if i == 0:
            xyz_coords_euler_angles = xyz_coords_euler_angles_temp
        else:
            
            xyz_coords_euler_angles = np.vstack((xyz_coords_euler_angles,xyz_coords_euler_angles_temp))
            
    return xyz_coords_euler_angles

def randomise_agnw(r_mean,r_sig,l_mean,l_sig,shift):
#function to randomise the scale, rotation and position of wires around initial array site
#inputs are the mean and standard deviation of radius and length respectively, plus a shift
#returns the radii and lengths of every wire

#units are considered in micrometres, e.g 10 for the mean length is a 10 micrometre long wire
#must be accounted for in hipgisaxs
    
    radii_arr = np.array([])
    len_arr = np.array([])

    for obj in units.all_objects:
    
	#objects must be selected in blender to operate on them
        obj.select_set(True)
    
	#radii and lengths of wires are Gaussian distributed
        rand_radius = np.random.normal(r_mean,r_sig)
        rand_length = np.random.normal(l_mean,l_sig)
    
        radii_arr = np.append(radii_arr,rand_radius)
        len_arr = np.append(len_arr,rand_length)
	
	#x,y dimensions calculated from radius and applied to wires
        rand_xy = rand_radius/(np.sqrt(2))
        obj.dimensions = [rand_xy,rand_xy,rand_length]
	
	#wires shifted randomly in x,y,z around their original lattice site
        rand_translation = tuple(np.random.uniform(-shift,shift,size=3))
        obj.location = obj.location + mathutils.Vector(rand_translation)

	#angles distributed over 2 pi and object angle updated
        rand_rotation = tuple(np.random.uniform(0,2,size=3))
        obj.rotation_euler = mathutils.Euler(rand_rotation)
    
	#object deselected before next iteration
        obj.select_set(False)
        
    radii_arr = np.reshape(radii_arr,(len(radii_arr),1))
    len_arr = np.reshape(len_arr,(len(len_arr),1))
    
    scale_arr = np.hstack((radii_arr,len_arr))
    
    return scale_arr

def get_data(key_frame,scale_arr):
#function to collect agnw data at the specified frame
#inputs are the frame number to take data, and scale array to combine with coordinates
#returns a 'frame handler' which is then applied in a separate function below

    #function defined within larger function
    def xyz_handler(scene):
        
        if bpy.context.scene.frame_current == key_frame:
        
	    #coords and angles collected and joined with scale array
            xyz_angles_arr = get_xyz_angles()
            xyz_angle_scales_data = np.hstack((xyz_angles_arr,scale_arr))
	    
            #data is deleted for wires that fell through the substrate
	    #occurs when there's a large number of wires
            del_indices = np.array([],dtype=int)
            for i,val in enumerate(xyz_angle_scales_data[:,2]):
                if val < 0:
                    del_indices = np.append(del_indices,int(i))
            xyz_angle_scales_data = np.delete(xyz_angle_scales_data,del_indices,0)
            
            #data saved under temporary filename in same folder as this script
            np.save("agnw_temp",xyz_angle_scales_data)
            
	    #blender quits so that automation can open the script again
            bpy.ops.wm.quit_blender()
            
    return xyz_handler

def register(update):
#function to apply the frame handler defined above
    bpy.app.handlers.frame_change_post.append(update)
           
def main():
#wires randomised and relevant data collected at specified frame number 
  
    bpy.app.handlers.frame_change_post.clear()
    scale_array = randomise_agnw(0.06,0.001,10,0.1,5) #default values 0.06,0.001,10,0.1,5
    bpy.ops.screen.animation_play()
    register(get_data(400,scale_array)) #default value of 400

main()

