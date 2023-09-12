from openupgradelib import openupgrade
from openupgradelib.openupgrade_160 import convert_string_bootstrap_4to5


def _mig_bs5_post_content(env):
    for post in env["blog.post"].with_context(active_test=False).search([]):
        converted_content = convert_string_bootstrap_4to5(post.content)
        if post.content != converted_content:
            post.content = converted_content


@openupgrade.migrate()
def migrate(env, version):
    _mig_bs5_post_content(env)
