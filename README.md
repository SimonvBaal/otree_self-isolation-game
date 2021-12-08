# otree_self-isolation-game

This is the project folder for the Self-Isolation Game experimental software, run through oTree. 
This repository is meant to facilitate reproducibility.

If you are new to oTree, I recommend reading some instructions before you dive into the code here. 

The structure of the project follows oTree conventions: the models.py file is the main file where the calculations happen. 
The pages.py is straightforward, and is just used to run the calculations from the models. Then there's the templates that generate the user interface.
In the settings.py, we indicate how much money each point is worth, what condition players start with, and the order of the apps (here just one).

The settings are left to three participants, so it is easy to demo, but I have indicated where things should be changed to ready it for an actual experiment.
