from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env.cr, "payment_paypal", "16.0.2.0/noupdate_changes.xml")
