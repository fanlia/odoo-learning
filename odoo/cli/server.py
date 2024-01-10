
from .command import Command

def main(args):
    print('server main', args)

class Server(Command):
    def run(self, args):
        main(args)
