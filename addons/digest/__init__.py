# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models
from odoo import api, SUPERUSER_ID


def subscribe_employee_users(env):
    """ Automatically subscribe employee users to default digest if activated """
    default_digest_emails = env['ir.config_parameter'].get_param('digest.default_digest_emails')
    default_digest_id = env['ir.config_parameter'].get_param('digest.default_digest_id')
    user_ids = env['res.users'].search([('share', '=', False)])
    if user_ids and default_digest_emails and default_digest_id:
        digest = env['digest.digest'].browse(int(default_digest_id))
        digest.user_ids |= user_ids


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    subscribe_employee_users(env)
