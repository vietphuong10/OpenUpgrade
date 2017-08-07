# -*- encoding: utf-8 -*-

import erppeek

openerp = erppeek.Client(URL)
uid = openerp.login(LOGIN, password=PASSWORD, database=DATABASE)


INSTALL_MODULES = [
    'web_sheet_full_width',
    'stock_picking_mass_action',
    'pos_default_empty_image',
    'pos_pricelist',
    'pos_margin',
    'product_standard_price_tax_included', # Check si ça remplace un module existant.
    'product_supplierinfo_tree_price_info',
    'web_ckeditor4',
    'web_favicon',
    'web_clean_navbar',
    'web_graph_sort',
    'web_graph_improved',
    'web_group_expand',
    'web_invalid_tab',

    'web_offline_warning',
    'web_invalid_tab',
    'web_switch_company_warning',
    'bi_sql_editor',

    # TEST AND INSTALL
    'pos_order_to_sale_order',
    'account_invoice_merge_purchase',

    'account_invoice_supplierinfo_update',
    'account_invoice_supplierinfo_update_discount',
    'invoice_margin',
    'stock_picking_mass_action',
    'purchase_supplier_rounding_method',
    'product_margin_classification',
    'stock_disable_barcode_interface',
    'product_supplierinfo_tree_price_info',

    # TO INSTALL after
    # account_product_fiscal_classification (replace product_tax_group)
    # product_standard_price_tax_included (replace product_standard_price_vat_incl)

    # A TESTER
    # purchase_add_product_supplierinfo
    # account_invoice_line_price_subtotal_gross
    # purchase_last_price_info
#    'base_mail_bcc',

#    'product_replenishment_cost',
#    'pos_order_load',

    # FIXME !, en conflit avec invoice_pricelist.
#    'account_invoice_pricelist',
#    'account_invoice_pricelist_sale',
#    'account_invoice_pricelist_sale_stock',

#     FIXME : ca m'a l'air bien long, ce module à cul
#     'web_menu_navbar_needaction',
]

# Fix 2 bugs de view de merde
# delete from ir_ui_view where id = 1761;
# delete from ir_ui_view where id = 946;

# FIX incorrect company for new warehouse : 
# update stock_location slp set company_id = (select company_id from stock_location as slc where slc.location_id = slp.id limit 1) where name ilike 'WH%';


# Améliore la création de pos_default_empty_image
# ALTER TABLE product_product ADD COLUMN has_image bool DEFAULT False;
# update product_product set has_image = true where product_tmpl_id in (select id from product_template where image is not null);
# update stock_location set company_id = null where id = 1;
    
# Améliore l'installtion de invoice_margin
# ALTER TABLE account_invoice ADD COLUMN margin float;
# ALTER TABLE account_invoice_line ADD COLUMN margin float;
# ALTER TABLE account_invoice_line ADD COLUMN purchase_price float;

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

