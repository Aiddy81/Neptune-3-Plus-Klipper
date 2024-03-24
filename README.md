# Neptune-3-Plus-Klipper
Contains my Klipper configuration for the Elegoo Neptune 3 Plus. Please note that values for Inpt shaper, rotation distance etc were from my calibrations so you may need to adjust these when calibrating your own machine.

This config is for the BTT-Pad 7 but may work with other devices.

# Klipper Z offset Recomender
zoffset_recommender is a small python script that will display a heat map of your bed with the corresponding probed values as well as reconmend an approiate z-offset.

![alt text](https://github.com/Aiddy81/Neptune-3-Plus-Klipper-Config/blob/main/Z-Offset_Recommender/example_heatmap.jpg))

There is another script klipper_mesh_transformer, simply copy your mesh to out of klipper and into this script, it will output the numpy matrix so you can just copy and past it into the zoffset_recommender.

