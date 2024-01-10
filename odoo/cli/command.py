
import sys

commands = {}

class Command:
    name = None
    def __init_subclass__(cls):
        cls.name = cls.name or cls.__name__.lower()
        commands[cls.name] = cls

def main():
    args = sys.argv[1:]

    command = 'server'

    if command in commands:
        o = commands[command]()
        o.run(args)
    else:
        sys.exit('Unkown command %r' % (command,))
