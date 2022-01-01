# AntiochusProjectMagshimim

This is the version of the Antiochus project of magshimim with the python Tkinter GUI.
The code itself is written in c, but python utilizes it to the GUI itself.


This project takes the compiled c code, and makes python use it
python has a library which contains an object called CDLL,
which imports the functions out of this compiled c code,
and allow python to use it through the object itself,


All of the "heavy lifting" calculating goes to c,
the compiled code contains all of the calculation the game needs,
and python just connects all of it and run the GUI using tkinter.