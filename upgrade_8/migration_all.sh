#!/bin/bash
## Build environnement and switch Odoo and OpenUpgrade folders
#./migration_prepare.sh

## Run Main migration with OpenUpgrade
#./migration_update_all.sh

# Run again server with OpenUpgrade (async)
ak run &
echo $! >/tmp/openupgrade.pid
pid=`cat /tmp/openupgrade.pid`
sleep 5
echo "please './migration_uninstall_modules.py' run please press enter at the end of the uninstall scripts"
read
# Stop previous async call
kill -9 $pid


## Switch back
#./migration_unprepare.sh

## Update with last Odoo code
#./migration_update_all.sh

## TODO install new modules


