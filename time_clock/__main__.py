from time_clock.config_funcs import set_config, list_config, get_config_setting
import argparse
import os
from time_clock.open_task import OpenTask
from time_clock.close_task import CloseTask
from time_clock.export import Export


def dir_check():
    home = os.path.expanduser('~')
    if get_config_setting('dropbox'):
        home += '/dropbox'
    if not os.path.isdir('{}/.timesheets'.format(home)):
        os.mkdir('{}/.timesheets'.format(home))
    return '{}/.timesheets'.format(home)


def new_ticket(args):
    directory = dir_check()
    if '.open' in os.listdir(directory):
        print('There is already an open task, please close.')
    else:
        OpenTask(directory, args)


def close_ticket(args):
    directory = dir_check()
    if '.open' not in os.listdir(directory):
        print('No ticket to close')
    else:
        CloseTask(directory)


def export_data(args):
    directory = dir_check()
    if '.open' in os.listdir(directory):
        print('Please close the open ticket to continue')
    else:
        Export(directory, args)


def print_help(args):
    parser.print_help()


parser = argparse.ArgumentParser()
parser.set_defaults(func=print_help)
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
task_parser.add_argument(
    '--company',
    '-c',
    help='What company is this task for',
    metavar='y',
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
    choices=range(1, 13),
    type=int)
export_parser.add_argument(
    '--year',
    '-y',
    help='Year to export',
    type=int)
export_parser.add_argument(
    '--project',
    '-p',
    help='Project to gather time for',
    type=str)
export_parser.add_argument(
    '--ticket',
    '-t',
    help='Ticket to gather time for',
    type=str)
export_parser.add_argument(
    '--company',
    '-c',
    help='Company to gather time for',
    type=str)
export_parser.set_defaults(func=export_data)

config_parser = subparsers.add_parser('config')
config_choices = config_parser.add_subparsers()
config_set = config_choices.add_parser(
    'set',
    help='set config setting')
config_set.add_argument('option', help='what option to set')
config_set.add_argument('value', choices=['true', 'false'])
config_set.set_defaults(func=set_config)
config_list = config_choices.add_parser(
    'list',
    help='list config settings')
config_list.set_defaults(func=list_config)

args = parser.parse_args()


def main():
    args.func(args)
