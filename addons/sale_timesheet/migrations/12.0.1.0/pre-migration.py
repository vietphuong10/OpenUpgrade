from psycopg2.extensions import AsIs
from openupgradelib import openupgrade


def fill_project_sale_order_id(env):
    if not openupgrade.column_exists(env.cr, 'project_project', 'sale_order_id'):
        openupgrade.add_fields(
            env, [
                ('sale_order_id', 'project.project', 'project_project', 'many2one',
                 'integer', 'sale_timesheet'),
            ],
        )
        openupgrade.logged_query(
            env.cr, """
            UPDATE project_project p
            SET sale_order_id = sol.order_id
            FROM sale_order_line sol
            WHERE p.sale_line_id IS NOT NULL
                AND sol.id = p.sale_line_id
            """
        )


def fill_project_task_sale_order_id(env):
    if not openupgrade.column_exists(env.cr, 'project_task', 'sale_order_id'):
        openupgrade.add_fields(
            env, [
                ('sale_order_id', 'project.task', 'project_task', 'many2one',
                 'integer', 'sale_timesheet'),
            ],
        )
        openupgrade.logged_query(
            env.cr, """
            UPDATE project_task t
            SET sale_order_id = sol.order_id
            FROM sale_order_line sol
            WHERE t.sale_line_id IS NOT NULL
                AND sol.id = t.sale_line_id
            """
        )

@openupgrade.migrate()
def migrate(env, version):
    fill_project_sale_order_id(env)
    fill_project_task_sale_order_id(env)
