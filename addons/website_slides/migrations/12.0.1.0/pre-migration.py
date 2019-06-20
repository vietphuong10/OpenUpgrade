from openupgradelib import openupgrade

_field_renames = [
    ('slide.channel', 'slide_channel', 'website_published', 'is_published'),
    ('slide.slide', 'slide_slide', 'website_published', 'is_published'),
]


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    openupgrade.rename_fields(env, _field_renames)
