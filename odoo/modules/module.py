
import sys
import os

import odoo

def load_openerp_module(module_name):
    qualname = f'odoo.addons.{module_name}'
    if qualname in sys.modules:
        return

    __import__(qualname)

def initialize_sys_path():
    for ad in odoo.tools.config['addons_path'].split(','):
        ad = os.path.normcase(os.path.abspath(ad.strip()))
        if ad not in odoo.addons.__path__:
            odoo.addons.__path__.append(ad)

