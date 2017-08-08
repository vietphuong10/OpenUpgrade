# -*- coding: utf-8 -*-
from migration_function import (
    manage_odoo_process, set_upgrade_mode,
    create_new_database)

# Stop Odoo Service
manage_odoo_process(False)
# Use OpenUpgrade folder
set_upgrade_mode(True)
# Create new database
new_database = create_new_database()
# Use OCB folder
set_upgrade_mode(False)
# start Odoo Service
manage_odoo_process(True)
