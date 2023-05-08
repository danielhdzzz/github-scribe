from datetime import timedelta
from datetime import datetime
import numpy as np
import subprocess
import math
import cv2
import os
import re

settings = {
  "commits_per_pixel": 480,
  "commits_per_blank_pixel": 0,
  "deploy": True,
  "source_img": './messages/message2.png',
  "start_date": {
    "y": 2023,
    "m": 4,
    "d": 2
  }
}

def write_file_new_line(filename, string):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:          
            f.write('\n' + string)   
    else:
        with open(filename, 'w') as f:                   
            f.write(string)

def write_file_replace_line(filename, string):
    lines = open(filename, 'r').readlines()
    # Edit the last line of the list of lines
    new_last_line = string
    lines[-1] = new_last_line
    # now write the modified list back out to the file
    open(filename, 'w').writelines(lines)

def git_commit_all(message):
    if settings['deploy'] == False: return
    return subprocess.check_output(['git', 'commit', '-am', message])

def git_set_date(date):
    if settings['deploy'] == False: return
    formatted_date = date.strftime("--date=\"%Y.%m.%d %H:%M\"")
    return subprocess.check_output(['git', 'commit', '--amend', '--no-edit', formatted_date])

def git_push():
    if settings['deploy'] == False: return
    return subprocess.check_output(['git', 'push'])

def get_number_from_str(inp_str):
    num = re.findall(r'\d+', inp_str)
    return num[0]

def ind_to_coord(i, w):
    return math.floor(i % w), math.floor(i / w)

def main():
    img = cv2.imread(settings['source_img'],0)
    total_days = len(img) * len(img[0])
    current_day = 0
    total_iterations = 0
    commit_day = datetime(
        settings['start_date']['y'],
        settings['start_date']['m'],
        settings['start_date']['d']
    )

    # For each day
    for i in range(total_days):
        coord = ind_to_coord(current_day,7)
        pixel = img[coord[0]][coord[1]]
        commit_number = settings['commits_per_pixel'] if pixel == 255 else settings['commits_per_blank_pixel']

        for i in range(commit_number):
            log_msg = f'Day {current_day + 1}. Commits {i + 1}. Iterations: {total_iterations + 1}. Date {commit_day}'
            print(log_msg)

            if commit_number == 1:
                # add new line to file
                write_file_new_line('log.txt' , log_msg)
            else:
                if i == 0:
                    # add new line to file
                    write_file_new_line('log.txt' , log_msg)
                else:
                    # replace last line of file
                    write_file_replace_line('log.txt', log_msg)
            
            total_iterations = total_iterations + 1
            git_commit_all(log_msg)
            git_set_date(commit_day)
        current_day = current_day + 1
        commit_day = commit_day + timedelta(days=1)

        if commit_number >= 1:
            git_push()

def init():
    # Delete any previous contents of log.txt
    open('log.txt', 'w').close()
    main()

init()