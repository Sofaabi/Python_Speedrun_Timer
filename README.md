# CLI-Speedrun-Timer
A simple CLI speedrun timer that saves personal bests for splits as a .csv file.

Several things to note:
 - The settings you're using mupen64plus and playing sm64 16 star, but is entirely agnostic to it just change some variables.
 - If you want to change the location or name of the file, change line 18 to whatever you want.
 - If you want to change what hotkey advances to the next split or restarts the timer, change line 19 or 20 respectively.
 - Do not delete individual splits from rows of the .csv file. Deletion of entire rows should be fine.
 - Deleting the "Bests" row will reset your personal best.
 - Due to issues with input(), after the final split pressing y or n **ANYWHERE** will immediately save or cancel saving the file. _ = input() is just there to halt the execution until you make a selection and press enter. I have no idea how to fix this.
 - The splits starting line 21 are all that need to be editted to change whatever splits are, you can add as many as you like. They are currenly set up for SM64 16 star splits. Adding splits without making a new file will cause a crash.
