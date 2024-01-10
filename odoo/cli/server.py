
import os
import sys
import logging
from pathlib import Path

import odoo
from .command import Command

_logger = logging.getLogger('odoo')

def report_configuration():
    """ Log the server version and some configuration values.

    This function assumes the configuration has been initialized.
    """
    config = odoo.tools.config
    _logger.info("Odoo version %s", odoo.release.version)
    if os.path.isfile(config.rcfile):
        _logger.info("Using configuration file at " + config.rcfile)
    _logger.info('addons paths: %s', odoo.addons.__path__)
    if config.get('upgrade_path'):
        _logger.info('upgrade path: %s', config['upgrade_path'])
    host = config['db_host'] or os.environ.get('PGHOST', 'default')
    port = config['db_port'] or os.environ.get('PGPORT', 'default')
    user = config['db_user'] or os.environ.get('PGUSER', 'default')
    _logger.info('database: %s@%s:%s', user, host, port)

def main(args):
    odoo.tools.config.parse_config(args)
    report_configuration()
    config = odoo.tools.config
    preload = []
    if config['db_name']:
        preload = config['db_name'].split(',')

    stop = config["stop_after_init"]
    rc = odoo.service.server.start(preload=preload, stop=stop)
    sys.exit(rc)

class Server(Command):
    def run(self, args):
        odoo.tools.config.parser.prog = f'{Path(sys.argv[0]).name} {self.name}'
        main(args)
