# Copyright 2019 TVTMA - David Tran <https://www.tvtmarine.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def enable_digest_kpi(env):
    digest_digest_default = env.ref('digest.digest_digest_default')
    digest_digest_default.write({
        'kpi_crm_lead_created': True,
        'kpi_crm_opportunities_won': True
        })


@openupgrade.migrate()
def migrate(env, version):
    enable_digest_kpi(env)
