
import odoo

def load_server_wide_modules():
    server_wide_modules = {'base', 'web'}

    for m in server_wide_modules:
        odoo.modules.load_openerp_module(m)


server = None

def start(preload=None, stop=False):
    global server
    print('service.server.start')

    load_server_wide_modules()
