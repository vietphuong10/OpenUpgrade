from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr, 'l10n_vn', 'migrations/12.0.2.0/noupdate_changes.xml')
    openupgrade.delete_records_safely_by_xml_id(
        env, [
            'l10n_vn.transfer_account_id',
            ],
    )
