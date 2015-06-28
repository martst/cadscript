# cadscript
Convert csv data created by profile plugin of QGIS into CAD script file.

The program uses TKinter to provide a simple GUI interface.

X and Y offsets can be set to allow multiple profiles to loaded into a CAD drawing. 
A multiplier can be used on the Y axis to make the profile more readable.

At line 160 in the program profile points are ignored if there is not a significant height change since the last point. This value can be changed as required. This is used to reduce the number of lines in the scr file as the CAD program can complain about too many points

As well as plotting the profile, axis and grid lines are drawn

I know that it is not an elegant program and I am sure I have broken many python rules but it does the job for me
