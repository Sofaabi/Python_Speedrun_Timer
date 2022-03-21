# CLI-Speedrun-Timer
A simple CLI speedrun timer that saves personal bests for splits as a .csv file.

Several things to note:
 - If you want to change the location or name of the file, change line 15 to whatever you want.
 - If you want to change what hotkey advances to the next split, change line 16.
 - Do not delete individual splits from rows of the .csv file. Deletion of entire rows should be fine.
 - Deleting the "Bests" row will reset your personal bests.
 - Due to issues with input(), after the final split pressing y or n **ANYWHERE** will immediately save or cancel saving the file. _ = input() is just there to halt the execution until you make a selection and press enter. I have no idea how to fix this.
 - The splits starting line 17 are all that need to be editted to change whatever splits are, you can add as many as you like. They are currenly set up for SM64 16 star splits. Adding splits without making a new file will cause a crash.
