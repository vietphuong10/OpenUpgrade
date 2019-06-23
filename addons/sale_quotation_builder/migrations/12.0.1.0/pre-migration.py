from openupgradelib import openupgrade

_field_renames = [
    ('product.template', 'product_template', 'quote_description', 'quotation_only_description'),
    ('sale.order', 'sale_order', 'template_id', 'sale_order_template_id'),
]

xmlid_renames = [
    ('website_quote.website_quote_template_default', 'sale_quotation_builder.sale_order_template_default'),
]


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    openupgrade.rename_fields(env, _field_renames)
    openupgrade.rename_xmlids(cr, xmlid_renames)
