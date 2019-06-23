from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    res_config_id = env['res.config.settings'].create({
        'group_sale_order_template': True,
        'module_sale_quotation_builder': True,
        })
    res_config_id.execute()
    env['res.config.settings']._set_default_sale_order_template_id_if_empty()
