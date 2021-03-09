#!/usr/bin/env python3

# Sam Elliott - Prudential scripting exercise.
# Written with Python 3.6.8 on CentOS Linux release 8.3.2011
# Provided instructions as follows:

# Write a script to clean up log files in a directory.  You can use any language.  Your script should accept parameters for the maximum age of a log file in days and the target archive network directory to move the old log files to.  Move any file older than the max days to the target directory.

import sys
import os
import glob
import shutil
import time
from datetime import datetime, date, timedelta

def main():
    # For checking to see if a forward slash is given as an extension.
    illegal_character = set("/")
    while True:
        try:
            file_extension = input("\nExtension of log files to parse. No beginning\nperiod. Enter nothing to parse all files: ")
            if any((c in illegal_character) for c in file_extension):
                print(f"Illegal character ( / ) found. Try again.")
                continue
            elif (file_extension == ""):
                print(f"Any and all files will be parsed.")
        except ValueError:
            continue
        break   

    while True:
        try:
            file_age = int(input("\nInput maximum age in days, integers only,\nof log files to retain: "))
            if (file_age < 0):
                print(f"This isn't Star Trek; no sorting of logs from the future. Try again.")
                continue
        except ValueError:
            print(f"Integer numbers only. Try again.")
            continue
        break

    while True:
        try:
            # os.path.normpath prevents trailing slashes from leading to erroneous comparisons to destination_path later.
            source_path = os.path.normpath(input("\nSource directory for log pruning.\nRelative and absolute paths work: "))
            if (source_path == ""):
                print(f"Input directory to scan. Try again.")
                continue
            elif (os.path.exists(source_path) == False):
                print(f"Non-existent path provided. Try again.")
                continue
            elif (os.path.isfile(source_path) == True):
                print(f"File specified, not a directory. Try again.")
                continue
            elif (os.access(source_path, os.R_OK) == False):
                print(f"Cannot read from source directory. Remediate this or provide a new directory.")
                continue
        except ValueError:
            continue
        break

    while True:
        try:
            destination_path = os.path.normpath(input("\nDirectory to move older log files to.\nRelative and absolute paths work: "))
            if (source_path == ""):
                print(f"Input directory to move logs to. Try again.")
                continue
            elif (os.path.exists(destination_path) == False):
                print(f"Non-existent path provided. Try again.")
                continue
            elif (os.path.isfile(destination_path) == True):
                print(f"File specified, not a directory. Try again.")
                continue
            elif (destination_path == source_path):
                print(f"Why even bother with this script? Try again.")
                continue
            elif (os.access(destination_path, os.W_OK) == False):
                print(f"Cannot write to destination directory. Remediate this or provide a new directory.")
                continue
        except ValueError:
            continue
        break

    move_date = date.today() - timedelta(file_age)
    print(f"Everything older than the following date now being moved: ",move_date)
    move_date = time.mktime(move_date.timetuple())
    
    log_count = 0
    log_total_size = 0.0

    if (file_extension == ""):
        file_extension = "*.*"
    else:
        file_extension = ("*." + file_extension)

    for filename in glob.glob1(source_path, file_extension):
        srcfile = os.path.join(source_path, filename)
        destfile = os.path.join(destination_path, filename)
        if os.stat(srcfile).st_mtime < move_date:
            if not os.path.isfile(destfile):
                log_total_size = log_total_size + (os.path.getsize(srcfile) / (1024))
                shutil.move(srcfile, destfile)
                log_count = log_count + 1
    
    if (log_count == 0):
        print(f"\nNo files met provided criteria; no work performed.")
    else:
        print(f"\nTotal number of logs moved:",log_count)
        print(f"Size of logs moved:",round(log_total_size,3), "KiB")

main()
