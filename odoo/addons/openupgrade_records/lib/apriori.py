""" Encode any known changes to the database here
to help the matching process
"""

renamed_modules = {
    # Odoo
    'base_vat_autocomplete': 'partner_autocomplete',
    'mrp_repair': 'repair',
    'product_extended': 'mrp_bom_cost',
    # OCA/account-payment
    'account_payment_return_import_sepa_pain': (
        'account_payment_return_import_iso20022'
    ),
    # OCA/community-data-files
    'product_uom_unece': 'uom_unece',
    # OCA/crm > OCA/partner-contact
    'crm_deduplicate_acl': 'partner_deduplicate_acl',
    'crm_deduplicate_filter': 'partner_deduplicate_filter',

    # erponline-enterprise
    'account_accountant': 'to_account_accountant',
    'account_asset': 'to_account_asset',
    'mrp_account': 'to_mrp_account',
    'quality': 'to_quality',
    'stock_barcode': 'to_stock_barcode',
    # OCA/stock-logistics-workflow
    'stock_pack_operation_auto_fill': 'stock_move_line_auto_fill',
    
    # tvtmaaddons
    'to_odoo_module_website_quote': 'to_odoo_module_sale_template',
    # tvtma
    'to_refesh_sale_order': 'to_refresh_sale_order',
}

merged_modules = {
    # Odoo
    'auth_crypt': 'base',
    'account_cash_basis_base_account': 'account',
    'account_invoicing': 'account',
    'rating_project': 'project',
    'sale_order_dates': 'sale',
    'sale_payment': 'sale',
    'sale_service_rating': 'sale_timesheet',
    'web_planner': 'web',
    'website_quote': 'sale_quotation_builder',
    'website_rating_project': 'project',
    'website_sale_options': 'website_sale',
    'website_sale_stock_options': 'website_sale_stock',
    'test_pylint': 'test_lint',
    # OCA/account-financial-reporting
    'customer_activity_statement': 'partner_statement',
    'customer_outstanding_statement': 'partner_statement',
    # OCA/account-financial-tools
    'account_reversal': 'account',
    # OCA/e-commerce
    'website_sale_default_country': 'website_sale',
    # OCA/event
    'event_registration_mass_mailing': 'mass_mailing_event',
    # OCA/manufacture-reporting
    'mrp_bom_structure_html': 'mrp',
    'mrp_bom_structure_report': 'mrp',
    # OCA/partner-contact
    'base_country_state_translatable': 'l10n_multilang',
    'base_partner_merge': 'base',
    # OCA/server-auth
    'auth_brute_force': 'base',
    # OCA/stock-logistics-warehouse
    'stock_putaway_product': 'stock',
    # OCA/web
    'web_no_bubble': 'web',
    'web_sheet_full_width': 'web_responsive',
    # OCA/website
    'website_form_metadata': 'website_form',
    
    # tvtmaaddons
    'to_vietnam_states': 'l10n_vn',
    'to_account_invoice_tax_analytic_tags': 'account',
    'to_sale_auto_sections': 'sale',
    'to_purchase_reports': 'purchase',
    'to_sale_backdate_delivery': 'to_sale_backdate',
    'to_sale_backdate_timesheet': 'to_sale_backdate',
    'to_sale_backdate_website_quote': 'to_sale_backdate',
    
    # joomla2odoo
    'to_multi_website': 'website',
    'to_multi_website_blog': 'website_blog',
    'to_multi_website_slide': 'website_slides',
}

# only used here for openupgrade_records analysis:
renamed_models = {
    # Odoo
    'hr.holidays': 'hr.leave',
    'hr.holidays.status': 'hr.leave.type',
    'mrp.repair': 'repair.order',
    'mrp.repair.fee': 'repair.fee',
    'mrp.repair.line': 'repair.line',
    'procurement.rule': 'stock.rule',
    'product.attribute.line': 'product.template.attribute.line',
    'product.attribute.price': 'product.template.attribute.value',
    'product.uom': 'uom.uom',
    'product.uom.categ': 'uom.category',
    'sale.quote.line': 'sale.order.template.line',
    'sale.quote.option': 'sale.order.template.option',
    'sale.quote.template': 'sale.order.template',
    'stock.incoterms': 'account.incoterms',
    # 'stock.location.path': 'stock.rule', handled in 'stock'
}
