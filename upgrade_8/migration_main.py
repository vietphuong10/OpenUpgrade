# -*- coding: utf-8 -*-
from migration_function import (
    manage_odoo_process, set_upgrade_mode, backup_database,
    create_new_database, execute_sql_file, update_instance,
    run_instance, kill_process, install_modules, uninstall_modules)

from migration_configuration import INSTALL_MODULE_LIST, UNINSTALL_MODULE_LIST

# Stop Odoo Service
manage_odoo_process(False)

# Use OpenUpgrade folder
set_upgrade_mode(True)

# Create new database
new_database = create_new_database()

# Run SQL / python Script before upgrade
execute_sql_file(new_database, '01_script_before_upgrade_7_8.sql')

# Upgrade with OpenUpgrade and backup
update_instance(new_database, 'all')
backup_database(new_database, '02_after_upgrade')

# Run SQL / python Script After Upgrade
execute_sql_file(new_database, '02_script_after_upgrade_7_8.sql')

## Use OCB folder
set_upgrade_mode(False)

# Update With OCB and backup
update_instance(new_database, 'all')
backup_database(new_database, '03_after_update')

# Run SQL / python Script After update with OCB
execute_sql_file(new_database, '03_script_after_update_8.sql')

# Install Modules and backup
proc = run_instance()
install_modules(new_database, INSTALL_MODULE_LIST)
kill_process(proc)
backup_database(new_database, '04_after_install')

# Run SQL / python Script After having installed new modules
execute_sql_file(new_database, '04_script_after_install.sql')

# Uninstall Modules and backup
proc = run_instance()
uninstall_modules(new_database, UNINSTALL_MODULE_LIST)
kill_process(proc)
backup_database(new_database, '05_after_uninstall')

# Run SQL / python Script After having installed new modules
execute_sql_file(new_database, '05_script_after_uninstall.sql')

## Creates Inventories
#proc = run_instance()
## TODO, create inventories
#kill_process(proc)

# start Odoo Service
manage_odoo_process(True)
