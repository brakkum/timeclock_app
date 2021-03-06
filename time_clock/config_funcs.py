from configparser import SafeConfigParser


def set_config(args):
    config = SafeConfigParser()
    config.read('./time_clock/config.ini')
    if args.option in config['settings']:
        config.set('settings', args.option, args.value)
        with open('./time_clock/config.ini', 'w') as config_file:
            config.write(config_file)
        print('Config setting {} set to {}'.format(args.option, args.value))
    else:
        print('{} not in settings'.format(args.option))

def list_config(args):
    help_doc = open('./time_clock/config_help', 'r').readlines()
    for line in help_doc:
        print(line.strip())
        print('Set to {}'.format(get_config_setting(line.split(':')[0])))

def get_config_setting(opt):
    config = SafeConfigParser()
    config.read('./time_clock/config.ini')
    return config.getboolean('settings', opt)
