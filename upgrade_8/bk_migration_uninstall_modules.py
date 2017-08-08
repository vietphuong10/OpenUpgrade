# -*- encoding: utf-8 -*-

import erppeek

openerp = erppeek.Client(URL)
uid = openerp.login(LOGIN, password=PASSWORD, database=DATABASE)

UNINSTALL_MODULES = [
    'process',
    'account_delete_move_null_amount',
    'account_mass_drop_moves',
    'account_merge_moves_by_patterns',
    'account_move_period_date_conform',
    'account_tax_update',
    'auth_generate_password',
    'grap_reporting',
    'intercompany_trade_purchase_discount',
    'intercompany_trade_purchase_order_reorder_lines',
    'intercompany_trade_sale_order_dates',
    'manage_accounts_integrity',
    'mobile_app_inventory',
    'module_parent_dependencies',
    'pos_backup_draft_orders',
    'pos_both_mode',
    'pos_improve_header',
    'pos_improve_images',
    'pos_improve_posbox',
    'pos_keep_draft_orders',
    'pos_remove_default_partner',
    'pos_second_header',
    'pos_street_market',
    'product_average_consumption',
    'product_get_cost_field',
    'product_stock_cost_field_report',
    'purchase_compute_order',
    'purchase_compute_order_pos',
    'purchase_compute_order_sale',
    'sale_fiscal_company',
    'sale_reporting',
    'stock_picking_mass_assign',
    'web_confirm_window_close',
    'web_popup_large',
]

INSTALL_MODULES = [
    'product_replenishment_cost',
    'pos_order_load',
    'pos_pricelist',
    'stock_picking_mass_action',
]

# Uninstall Obsolete Modules
for module_name in UNINSTALL_MODULES:
    openerp = erppeek.Client(URL)
    uid = openerp.login(LOGIN, password=PASSWORD, database=DATABASE)
    module = openerp.IrModuleModule.browse([('name', '=', module_name)])[0]
    if module.state != 'uninstalled':
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print "Uninstalling %s" % module.name
        try:
            openerp.IrModuleModule.module_uninstall([module.id])
        except Exception:
            print "Caramba, encore raté ! "
            pass


