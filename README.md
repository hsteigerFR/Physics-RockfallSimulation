# Physics - Rockfall Simulation

Authors : Hugo Steiger, Cécile Aprili, Tristan Durey, Pierre Gibert, Antoine Quillivic, Nicolas Van Kempen  
Mentor : Madani Hamlaoui  
Full documentation (in french) : https://drive.google.com/drive/folders/12cettIedVXWK-mmxdB9t7zCneQAwkQOn?usp=sharing

-------------------------------------------------------------------------------------------------------------------------------------------------------------

This program was made for a group project carried out as part as my first engineering year at Mines Nancy. Its goal was to simulate rockfalls in order to predict and prevent damages on roads or buildings. The simulation is quite plain looking as the work was mainly focused on the physical model and the iterative solving of the rock movement equations. An explicit Euler method was used to solve the equations iteratively, showing the rock movement in real time. The simulation has limitations : the separation between a bouncing behaviour and a sliding behaviour is hard to establish and may not always work properly.

Here is an illustration of how the program works :

![Capture](https://user-images.githubusercontent.com/106969232/182220344-56c53d96-5bae-4be9-be34-3ff5afb428ba.JPG)

The user enters the different simulation constants, mainly regarding the initial state of the rock or the modeling of the environment, and simply has to press "Animation" to start the simulation. The UI was made with the Tkinter library. With the constants used in the program saved in this repository, the simulation should look like this :

![Demo](https://user-images.githubusercontent.com/106969232/182220775-f850ad5b-6811-44c7-a134-d495518d60c1.gif)

-------------------------------------------------------------------------------------------------------------------------------------------------------------

HOW TO USE :
- Open "simulation.py" with a Python or text editor.
- The constants of the model can be changed from line 202.
- Run the program with Python3.
- "Quitter" closes the program, "Animation" starts the simulation, "Pause" pauses it and "Étape par Étape" enables to run the simulation step by step.

Tested on Python 3.9.1, Windows 10 (x64). For more information on the physical modeling and empirical validation, check the project documentation on the Drive link above.
