import argparse
import datetime
import time
import os
from OpenTask import OpenTask
from CloseTask import CloseTask


parser = argparse.ArgumentParser(allow_abbrev=True)

parser.add_argument(
    '--ticket',
    '-t',
    help='what task is being worked on',
    type=str)
parser.add_argument(
    '--close',
    '-c',
    help='Close the currently open ticket',
    action='store_true')

args = parser.parse_args()
print(args)

def dir_check():
    home = os.path.expanduser('~')
    if not os.path.isdir('{}/.timesheets'.format(home)):
        os.mkdir('{}/.timesheets'.format(home))
    return '{}/.timesheets'.format(home)


def main():
    directory = dir_check()
    if args.ticket:
        if '.open' in os.listdir(directory):
            print('There is already an open task, please close.')
        else: 
            OpenTask(args.ticket, directory)
    elif args.close:
        if not '.open' in os.listdir(directory):
            print('No ticket to close')
        else:
            CloseTask(directory)
    else:
        print('no task')


if __name__ == '__main__':
    main()