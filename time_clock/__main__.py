import argparse
import datetime
import time
import os
from OpenTask import OpenTask
from CloseTask import CloseTask
from Export import Export


def dir_check():
    home = os.path.expanduser('~')
    if not os.path.isdir('{}/.timesheets'.format(home)):
        os.mkdir('{}/.timesheets'.format(home))
    return '{}/.timesheets'.format(home)

def new_ticket(args):
    directory = dir_check()
    if '.open' in os.listdir(directory):
        print('There is already an open task, please close.')
    else: 
        OpenTask(args.ticket, directory)

def close_ticket(args):
    directory = dir_check()
    if not '.open' in os.listdir(directory):
        print('No ticket to close')
    else:
        CloseTask(directory)

def export_data(args):
    directory = dir_check()
    if '.open' in os.listdir(directory):
        print('Please close the open ticket to continue')
    else:
        Export(directory, args)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

task_parser = subparsers.add_parser('ticket')
task_parser.add_argument(
    'ticket',
    help='What task is being worked on',
    metavar='ticket',
    type=str)
task_parser.set_defaults(func=new_ticket)

close_parser = subparsers.add_parser('close')
close_parser.set_defaults(func=close_ticket)

export_parser = subparsers.add_parser('export')
export_parser.add_argument(
    '--month',
    '-m',
    help='Export data for month',
    metavar='1-12',
    type=int)
export_parser.add_argument(
    '--year',
    '-y',
    help='Year to export',
    type=int)
export_parser.set_defaults(func=export_data)

args = parser.parse_args()
args.func(args)
