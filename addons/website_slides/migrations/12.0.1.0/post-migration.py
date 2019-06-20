from openupgradelib import openupgrade, openupgrade_120


def set_channel_default_website(env):
    channel_ids = env['slide.channel'].with_context(active_test=False).search([('website_id', '=', False)])
    if channel_ids:
        channel_ids.write({
            'website_id': env.ref('website.default_website').id
            })


def update_website_slide_google_app_key(env):
    website_ids = env['website'].search([('website_slide_google_app_key', '=', False)])
    if website_ids:
        website_ids.write({
            'website_slide_google_app_key': env['ir.config_parameter'].sudo().get_param('website_slides.google_app_key')
            })


@openupgrade.migrate()
def migrate(env, version):
    openupgrade_120.convert_field_bootstrap_3to4(
        env, 'slide.channel', 'description',
    )
    set_channel_default_website(env)
    update_website_slide_google_app_key(env)
