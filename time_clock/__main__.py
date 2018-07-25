from configparser import SafeConfigParser
import argparse
import datetime
import time
import os
from time_clock.open_task import OpenTask
from time_clock.close_task import CloseTask
from time_clock.export import Export



def set_config(args):
    config = SafeConfigParser()
    config.read('./time_clock/config.ini')
    if args.set in config['settings']:
        config.set('settings', args.set, args.value)
        with open('./time_clock/config.ini', 'w') as config_file:
            config.write(config_file)
            print('Config setting {} set to {}'.format(args.set, args.value))

def get_config_setting(opt):
    config = SafeConfigParser()
    config.read('./time_clock/config.ini')
    return config.getboolean('settings', opt)

def get_config():
    config = SafeConfigParser()
    config.read('./time_clock/config.ini')
    config_obj = {}
    for setting in config.options('settings'):
        config_obj[setting] = config.getboolean('settings', setting)
    return config_obj

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
        OpenTask(directory, args, get_config())

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
        Export(directory, args, get_config())


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
config_set = config_parser.add_mutually_exclusive_group()
config_set.add_argument(
    '--set',
    '-s',
    help='config option to set',
    type=str)
config_parser.add_argument(
    'value',
    help='boolean true/false',
    choices=['true', 'false'],
    type=str)
config_parser.set_defaults(func=set_config)

args = parser.parse_args()


def main():
    args.func(args)
