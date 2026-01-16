from datetime import timedelta
from datetime import datetime
import argparse
import numpy as np
import subprocess
import math
import cv2
import os
import re

def parse_args():
    parser = argparse.ArgumentParser(
        description='Print images into your GitHub contributions graph'
    )
    parser.add_argument(
        '--image', '-i',
        required=True,
        help='Path to source image (7px tall, black/white only)'
    )
    parser.add_argument(
        '--start-date', '-s',
        required=True,
        help='Start date in YYYY-MM-DD format (must be a Sunday)'
    )
    parser.add_argument(
        '--commits-per-pixel', '-c',
        type=int,
        default=220,
        help='Commits per dark pixel (default: 220)'
    )
    parser.add_argument(
        '--commits-per-blank', '-b',
        type=int,
        default=0,
        help='Commits per blank pixel (default: 0)'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Preview without making commits'
    )
    return parser.parse_args()

def print_preview(img, args, start_date):
    """Print ASCII preview of the contribution graph, chunked by year."""
    height, width = img.shape

    # Print settings summary
    print("Settings:")
    print(f"  Image:            {args.image}")
    print(f"  Start date:       {start_date.strftime('%Y-%m-%d')} ({start_date.strftime('%A')})")
    print(f"  Commits/pixel:    {args.commits_per_pixel}")
    print(f"  Commits/blank:    {args.commits_per_blank}")
    print(f"  Image dimensions: {width}x{height}")
    print()

    # Calculate date range
    end_date = start_date + timedelta(days=width * 7 - 1)

    # Get all years spanned
    years = list(range(start_date.year, end_date.year + 1))

    print("Preview:")
    for year_idx, year in enumerate(years):
        year_start = datetime(year, 1, 1)
        year_end = datetime(year, 12, 31)

        # Find column range for this year
        if year_start <= start_date:
            first_col = 0
        else:
            days_diff = (year_start - start_date).days
            first_col = days_diff // 7

        if year_end >= end_date:
            last_col = width - 1
        else:
            days_diff = (year_end - start_date).days
            last_col = days_diff // 7

        print(f"  {year}:")

        for row in range(7):
            line = "  "
            row_has_content = False
            for col in range(first_col, last_col + 1):
                day_date = start_date + timedelta(days=col * 7 + row)
                if year_start <= day_date <= year_end and start_date <= day_date <= end_date:
                    pixel = img[row][col]
                    line += "█" if pixel == 255 else "░"
                    row_has_content = True
                else:
                    line += " "
            if row_has_content:
                print(line.rstrip())

        if year_idx < len(years) - 1:
            print()

def confirm_proceed():
    """Ask user to confirm before proceeding."""
    response = input("\nProceed? [y/N]: ").strip().lower()
    return response in ('y', 'yes')

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

def git_commit_all(message, dry_run):
    if dry_run: return
    return subprocess.check_output(['git', 'commit', '-am', message])


def git_set_date(date, dry_run):
    if dry_run: return
    formatted_date = date.strftime("--date=\"%Y.%m.%d %H:%M\"")
    return subprocess.check_output(['git', 'commit', '--amend', '--no-edit', formatted_date])

def git_push(dry_run):
    if dry_run: return
    return subprocess.check_output(['git', 'push'])

def get_number_from_str(inp_str):
    num = re.findall(r'\d+', inp_str)
    return num[0]

def ind_to_coord(i, w):
    return math.floor(i % w), math.floor(i / w)

def main():
    args = parse_args()

    # Parse start date
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')

    img = cv2.imread(args.image, 0)

    # Show preview
    print_preview(img, args, start_date)

    # Handle dry-run or confirmation
    if args.dry_run:
        print("\n[DRY RUN] No commits will be made")
        return

    if not confirm_proceed():
        print("Aborted.")
        return

    print()  # Blank line before commit output

    total_days = len(img) * len(img[0])
    current_day = 0
    total_iterations = 0
    commit_day = start_date

    # For each day
    for i in range(total_days):
        coord = ind_to_coord(current_day, 7)
        pixel = img[coord[0]][coord[1]]
        commit_number = args.commits_per_pixel if pixel == 255 else args.commits_per_blank

        for i in range(commit_number):
            log_msg = f'Day {current_day + 1}. Commits {i + 1}. Iterations: {total_iterations + 1}. Date {commit_day}'
            print(log_msg)

            if commit_number == 1:
                # add new line to file
                write_file_new_line('log.txt', log_msg)
            else:
                if i == 0:
                    # add new line to file
                    write_file_new_line('log.txt', log_msg)
                else:
                    # replace last line of file
                    write_file_replace_line('log.txt', log_msg)

            total_iterations = total_iterations + 1
            git_commit_all(log_msg, args.dry_run)
            git_set_date(commit_day, args.dry_run)
        current_day = current_day + 1
        commit_day = commit_day + timedelta(days=1)

        if commit_number >= 1:
            git_push(args.dry_run)


if __name__ == '__main__':
    # Delete any previous contents of log.txt
    open('log.txt', 'w').close()
    main()