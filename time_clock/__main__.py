import argparse
import os
from TaskManager import TaskManager

parser = argparse.ArgumentParser(allow_abbrev=True)

parser.add_argument(
    '--ticket',
    '-t',
    help='what task is being worked on',
    type=str)

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
        TaskManager(args.ticket, directory)
    else:
        print('no task')


if __name__ == '__main__':
    main()