from openupgradelib import openupgrade


def active_group_project_milestone(env):
    env["res.config.settings"].create({"group_project_milestone": True}).execute()


@openupgrade.migrate()
def migrate(env, version):
    active_group_project_milestone(env)
    openupgrade.load_data(env.cr, "project", "16.0.1.2/noupdate_changes.xml")
