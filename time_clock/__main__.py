import argparse
import datetime
import time
import os
from OpenTask import OpenTask
from CloseTask import CloseTask
from Export import Export


def dir_check():
    home = os.path.expanduser('~')
    if not os.path.isdir('{}/dropbox/.timesheets'.format(home)):
        os.mkdir('{}/dropbox/.timesheets'.format(home))
    return '{}/dropbox/.timesheets'.format(home)

def new_ticket(args):
    directory = dir_check()
    if '.open' in os.listdir(directory):
        print('There is already an open task, please close.')
    else: 
        OpenTask(directory, args)

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
task_parser.add_argument(
    '--project',
    '-p',
    help='What project is this task a part of',
    metavar='x',
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
args = export_parser.add_mutually_exclusive_group()
args.add_argument(
    '--project',
    '-p',
    help='Project to gather time for',
    type=str)
args.add_argument(
    '--ticket',
    '-t',
    help='Ticket to gather time for',
    type=str)
export_parser.set_defaults(func=export_data)

args = parser.parse_args()
args.func(args)
