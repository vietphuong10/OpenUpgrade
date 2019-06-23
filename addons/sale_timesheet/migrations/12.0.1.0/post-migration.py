from openupgradelib import openupgrade


def fill_sale_line_with_project(env):
    """
    project_id is a new field in sale_order_line
    """
    openupgrade.logged_query(
        env.cr, """
        UPDATE sale_order_line sol
        SET project_id = pt.project_id
        FROM project_task as pt
        WHERE pt.id = sol.task_id AND sol.project_id is NULL
        """
        )


@openupgrade.migrate()
def migrate(env, version):
    fill_sale_line_with_project(env)
