# Neptune-3-Plus-Klipper
Contains my Klipper configuration for the Elegoo Neptune 3 Plus. Please note that values for Inpt shaper, rotation distance etc were from my calibrations so you may need to adjust these when calibrating your own machine.

Also if worth noting that if using or changing Nozzle sizes from the default 0.4 you will need to also change the value of max_extrude_cross_section: 0.64. To caculate the new value you can use this formulae, assuming d is your nozzle size 4 *(d)^2.

This config is for the BTT-Pad 7 and the Neptune 3 Plus.

# Klipper Z offset Recomender
zoffset_recommender is a small python script that will display a heat map of your bed with the corresponding probed values as well as reconmend an approiate z-offset.

![alt text](https://github.com/Aiddy81/Neptune-3-Plus-Klipper-Config/blob/main/Z-Offset_Recommender/example_heatmap.jpg)

There is another script klipper_mesh_transformer, simply copy your mesh to out of klipper and into this script, it will output the numpy matrix so you can just copy and past it into the zoffset_recommender.

