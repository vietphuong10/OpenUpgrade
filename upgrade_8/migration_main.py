# -*- coding: utf-8 -*-
from migration_function import (
    manage_odoo_process, set_upgrade_mode,
    create_new_database, execute_sql_file, update_instance)

## Stop Odoo Service
#manage_odoo_process(False)
## Use OpenUpgrade folder
#set_upgrade_mode(True)

## --- Migration
## Create new database
## new_database = create_new_database()
#new_database = 'grap_change_views'      # TODO REMOVE

## Run SQL / python Script before upgrade
#execute_sql_file(new_database, '01_script_before_upgrade_7_8.sql')

## Upgrade with OpenUpgrade
#update_instance(new_database, 'all')

## Run SQL / python Script After Uptrade
#execute_sql_file(new_database, '02_script_after_upgrade_7_8.sql')

# Use OCB folder
set_upgrade_mode(False)

# Update With OCB
update_instance(new_database, 'all')

# Run SQL / python Script After update with OCB
execute_sql_file(new_database, '03_script_after_update_8.sql')

# Install Modules
# TODO Run Instance
# TODO erppeek
# TODO Kill Instance

# Run SQL / python Script After having installed new modules
execute_sql_file(new_database, '04_script_after_install.sql')

# Uninstall Modules
# TODO Run Instance
# TODO erppeek
# TODO Kill Instance

# Run SQL / python Script After having installed new modules
execute_sql_file(new_database, '05_script_after_uninstall.sql')

## start Odoo Service
#manage_odoo_process(True)
