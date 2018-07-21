import argparse
import os
from TaskManager import TaskManager

parser = argparse.ArgumentParser(allow_abbrev=True)

parser.add_argument(
    '--task',
    '-t',
    help='what task is being worked on',
    type=str)

args = parser.parse_args()
print(args)

def dir_check():
    home = os.path.expanduser('~')
    if os.path.isdir('{}/.timesheets'.format(home)):
        return
    else:
        os.mkdir('{}/.timesheets'.format(home))


def main():
    dir_check()
    if args.task:
        TaskManager(args)
    else:
        print('no task')


if __name__ == '__main__':
    main()