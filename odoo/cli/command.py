
import sys

commands = {}

def main():
    args = sys.argv[1:]
    print('hello main', args)

    command = 'server'

    if command in commands:
        o = commands[command]()
        o.run(args)
    else:
        sys.exit('Unkown command %r' % (command,))
