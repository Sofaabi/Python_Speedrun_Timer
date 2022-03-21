import time
import sys
from threading import Event
from os.path import exists
from os import execl, system
from pynput import keyboard
import pandas as pd
from datetime import datetime


#  All time values that are not strings or time.sleep are handled as milliseconds.

create_split = Event()
check_save_file = Event()
save_file = Event()
restart_delay = 1.783  # The approximate time for mugenplus to reset for sm64

time_filepath = "sm64_16_star_times.csv"
hotkey = keyboard.Key.alt_r
reset_hotkey = keyboard.Key.f9  # This is the default key to restart mugenplus
splits = ["BOB  ",
          "WF   ",
          "CCM  ",
          "BITDW",
          "SSL  ",
          "LLL  ",
          "HMC  ",
          "MIPS ",
          "DDD  ",
          "BITFS",
          "BLJs ",
          "BITS ",
          "DED  "]


def restart_program():
    time.sleep(restart_delay)
    system('clear')
    python = sys.executable
    execl(python, python, *sys.argv)


def get_csv_db(time_file):
    times_csv = None
    personal_bests = None
    if exists(time_file):
        times_csv = pd.read_csv(time_file, index_col=0)
        if "Bests" in times_csv.index:
            personal_bests = times_csv.loc["Bests"].values.flatten().tolist()
            for i in range(len(personal_bests)):
                personal_bests[i] = string_to_ms(personal_bests[i])
    else:
        times_csv = pd.DataFrame(columns=splits + ["Total Time"])

    return times_csv, personal_bests


# Times is a list of length equal to the length of split + a total time
# Best of is similar
def save_times(times_csv, time_file, times, personal_bests):
    if personal_bests is not None:
        personal_bests = update_personal_bests(times, personal_bests)

    for i, t in enumerate(times):
        times[i] = ms_to_string(t)
    times_csv.loc[datetime.now().strftime("%Y/%m/%d-%H:%M:%S")] = times
    if personal_bests is not None:
        for i, t in enumerate(personal_bests):
            personal_bests[i] = ms_to_string(t)
        times_csv.loc["Bests"] = personal_bests
    else:
        times_csv.loc["Bests"] = times
    times_csv.to_csv(time_file)


def update_personal_bests(times, personal_bests):
    if times[-1] < personal_bests[-1]:
        return times.copy()
    return personal_bests


def ns_to_ms(ns):
    return ns//1000000


def string_to_ms(time_string):
    t = time_string.split(':')
    return int(int(t[0])*60000 + float(t[1])*1000)


def ms_to_string(ms):
    ms = int(ms)
    m = int(ms // 60000)
    s = int((ms % 60000) // 1000)
    ms = int(ms % 1000)
    timer = "{:02d}:{:02d}.{:02d}".format(m, s, ms//10)  # //10 for some reason makes it output correctly
    return timer


def on_press(key):
    yes = [{keyboard.KeyCode(char='y')}, {keyboard.KeyCode(char='Y')}]
    no = [{keyboard.KeyCode(char='n')}, {keyboard.KeyCode(char='N')}]
    if check_save_file.is_set():
        # This can be handled better, man is it jank
        if any([key in y for y in yes]):
            save_file.set()
            return False
        elif any([key in n for n in no]):
            return False
    if key == hotkey:
        create_split.set()
        time.sleep(.001)
    elif key == reset_hotkey:
        restart_program()


def on_release(key):
    return


def get_difference_string(split_time, pb):
    diff = split_time - pb
    symbol = "+"
    if diff < 0:
        symbol = "-"
        diff = -diff
    return symbol + ms_to_string(diff)


def run(personal_bests, times_csv, time_file):
    current_split = 0
    times = []
    time_start = ns_to_ms(time.time_ns())
    previous_time = time_start
    split_pb_sum = 0

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        time_current = ns_to_ms(time.time_ns())
        time_passed = time_current - time_start
        timer = ms_to_string(time_passed)

        if create_split.is_set():
            # Calculate and store split time
            split_time = time_current - previous_time
            previous_time = time_current
            times.append(split_time)

            # Get the current vs the best_of if best_of exists
            diff = "- - -"
            if personal_bests is not None:
                split_pb_sum += personal_bests[current_split]
                diff = get_difference_string(time_passed, split_pb_sum)

            #  basically print(splits[current_split] + ": " + timer + " | " + diff)
            #  but puts the carat at the end of the line
            sys.stdout.write("\r")
            sys.stdout.write(splits[current_split] + ": " + timer + " | " + diff + "\n")
            sys.stdout.flush()

            current_split += 1
            create_split.clear()
            # If final split is over
            if current_split == len(splits):
                # Add the total time to the times to save
                times.append(time_passed)
                check_save_file.set()
                print("Save times? [Y/n]: ")
                _ = input()
                if save_file.is_set():
                    save_times(times_csv, time_file, times, personal_bests)
                break
        else:
            #  basically print(splits[current_split] + ": " + timer, end="\r")
            #  but puts the carat at the end of the line
            sys.stdout.write("\r")
            sys.stdout.write(splits[current_split] + ": " + timer)
            sys.stdout.flush()

        time.sleep(0.0001)


csv, bests = get_csv_db(time_filepath)
run(bests, csv, time_filepath)
