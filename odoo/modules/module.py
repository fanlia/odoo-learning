
import sys

def load_openerp_module(module_name):
    print('load_openerp_module', module_name)

    qualname = f'odoo.addons.{module_name}'
    if qualname in sys.modules:
        return

    __import__(qualname)
