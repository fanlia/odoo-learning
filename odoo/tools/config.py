
import configparser as ConfigParser
import os
import optparse
from os.path import expandvars, expanduser, abspath, realpath, normcase

import logging
logging.basicConfig(level=logging.DEBUG)

import odoo
from .. import release

class configmanager(object):
    def __init__(self, fname=None):

        self.options = {
            'admin_passwd': 'admin',
        }

        version = '%s %s' % (release.description, release.version)
        self.parser = parser = optparse.OptionParser()

        # Common
        group = optparse.OptionGroup(parser, "Common options")
        group.add_option("-c", "--config", dest="config", help="specify alternate config file")
        group.add_option("-i", "--init", dest="init", help="install one or more modules (comma-separated list, use \"all\" for all modules), requires -d")
        group.add_option("-u", "--update", dest="update",
                          help="update one or more modules (comma-separated list, use \"all\" for all modules). Requires -d.")
        group.add_option("--addons-path", dest="addons_path",
                         help="specify additional addons paths (separated by commas).",
                         type="string")
        group.add_option("--upgrade-path", dest="upgrade_path",
                         help="specify an additional upgrade path.",
                         type="string")
        group.add_option("--load", dest="server_wide_modules", help="Comma-separated list of server-wide modules.")
        parser.add_option_group(group)

        # Database
        group = optparse.OptionGroup(parser, "Database related options")
        group.add_option("-d", "--database", dest="db_name",
                         help="specify the database name")
        parser.add_option_group(group)

        # Advanced
        group = optparse.OptionGroup(parser, "Advanced options")
        group.add_option("--stop-after-init", action="store_true", dest="stop_after_init",
                          help="stop the server after its initialization")
        parser.add_option_group(group)

    def parse_config(self, args=None):
        opt = self._parse_config(args)
        odoo.modules.module.initialize_sys_path()
        return opt

    def _parse_config(self, args=None):
        if args is None:
            args = []

        def die(cond, msg):
            if cond:
                self.parser.error(msg)

        opt, args = self.parser.parse_args(args)

        die(args, 'unrecognized parameters: "%s"' % ' '.join(args))

        rcfilepath = os.path.expanduser('~/.odoorc')
        self.rcfile = os.path.abspath(opt.config or rcfilepath)
        self.load()

        keys = [
            'init',
            'update',
            'addons_path',
            'upgrade_path',
            'server_wide_modules',
            'db_name',
            'stop_after_init',
        ]

        for key in keys:
            self.options[key] = getattr(opt, key)

        return opt

    def load(self):
        p = ConfigParser.RawConfigParser()
        p.read([self.rcfile])
        for (name, value) in p.items('options'):
            self.options[name] = value

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default=None):
        return self.options.get(key, default)

    def _normalize(self, path):
        if not path:
            return ''
        return normcase(realpath(abspath(expanduser(expandvars(path.strip())))))

config = configmanager()
