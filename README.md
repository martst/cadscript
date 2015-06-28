# cadscript
Convert csv data created by profile plugin of QGIS into CAD script file.

The program uses TKinter to provide a simple GUI interface.

X and Y offsets can be set to allow multiple profiles to loaded into a CAD drawing. 
A multiplier can be used on the Y axis to make the profile more readable.

At line 160 in program profile points are ignored if there wasnot a significant height cahnge since the last point. This value can be changed as required. This is used to reduce the number of lines in the scr file as the CAD program can complain about too many points
