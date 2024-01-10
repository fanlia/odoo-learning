
import sys
from pathlib import Path

import odoo
from .command import Command

def main(args):
    print('server main', args)

class Server(Command):
    def run(self, args):
        odoo.tools.config.parser.prog = f'{Path(sys.argv[0]).name} {self.name}'
        main(args)
