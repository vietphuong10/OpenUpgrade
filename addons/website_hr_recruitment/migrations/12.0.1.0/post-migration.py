# Copyright 2019 Eficent <http://www.eficent.com>
# Copyright 2019 Tecnativa - Pedro M. Baeza
# Copyright 2019 TVTMA - David Tran
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade, openupgrade_120


def set_default_website(env):
    hr_job_ids = env['hr.job'].with_context(active_test=False).search([('website_id', '=', False)])
    if hr_job_ids:
        hr_job_ids.write({
            'website_id': env.ref('website.default_website').id
            })


@openupgrade.migrate()
def migrate(env, version):
    set_default_website(env)
    openupgrade_120.convert_field_bootstrap_3to4(
        env, 'hr.job', 'website_description',
    )
