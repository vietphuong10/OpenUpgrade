# -*- encoding: utf-8 -*-

import erppeek

openerp = erppeek.Client(URL)
uid = openerp.login(LOGIN, password=PASSWORD, database=DATABASE)



# Fix 2 bugs de view de merde
# delete from ir_ui_view where id = 1761;
# delete from ir_ui_view where id = 946;

# FIX incorrect company for new warehouse : 
# update stock_location slp set company_id = (select company_id from stock_location as slc where slc.location_id = slp.id limit 1) where name ilike 'WH%';


# Améliore la création de pos_default_empty_image
# update stock_location set company_id = null where id = 1;

# Fix pos_order : set correct picking_type_id
# update purchase_order po set picking_type_id = (select id from stock_picking_type stp where code= 'incoming' and stp.company_id = po.company_id limit 1) where picking_type_id != (select id from stock_picking_type stp where code='incoming' and stp.company_id = po.company_id limit 1);

# TODO, fix les sequence des stock_picking_type qui sont toute associées à REG.


# TODO, pos_margin, ajouter colonne à la création, with margin = 0

# Install Obsolete Modules
for module_name in INSTALL_MODULES:
    openerp = erppeek.Client(URL)
    uid = openerp.login(LOGIN, password=PASSWORD, database=DATABASE)
    modules = openerp.IrModuleModule.browse([('name', '=', module_name)])
    if len(modules) == 0:
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print "Module not found %s" % module_name
    elif modules[0].state == 'uninstalled':
        module = modules[0]
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print "Installing %s" % module.name
        try:
            openerp.IrModuleModule.button_immediate_install([module.id])
        except Exception:
            print "Caramba, encore raté ! "
            pass
    elif modules[0].state != 'installed':
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print "Warning, %s module in %s state" % (module_name, modules[0].state)

