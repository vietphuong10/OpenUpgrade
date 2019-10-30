from openupgradelib import openupgrade, openupgrade_120

def fill_website_slide_google_app_key(env):
    key = env['ir.config_parameter'].sudo().get_param(
        'website_slides.google_app_key',
    )
    if key:
        env['website'].search([]).write({
            'website_slide_google_app_key': key,
        })

def set_channel_default_website(env):
    channel_ids = env['slide.channel'].with_context(active_test=False).search([('website_id', '=', False)])
    if channel_ids:
        channel_ids.write({
            'website_id': env.ref('website.default_website').id
            })

@openupgrade.migrate()
def migrate(env, version):
    fill_website_slide_google_app_key(env)
    openupgrade.delete_records_safely_by_xml_id(
        env, [
            'website_slides.google_app_key',
        ],
    )
    openupgrade_120.convert_field_bootstrap_3to4(
        env, 'slide.channel', 'description',
    )
    openupgrade.load_data(
        env.cr, 'website_slides', 'migrations/12.0.1.0/noupdate_changes.xml')
    openupgrade.delete_record_translations(
        env.cr, 'website_slides', [
            'slide_template_published',
            'slide_template_shared',
        ],
    )
    set_channel_default_website(env)
