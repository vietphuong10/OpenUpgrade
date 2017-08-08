# -*- coding: utf-8 -*-
import os
from subprocess import call
from datetime import datetime

from secret_configuration import (
    ODOO_FOLDER_BACKUP, ODOO_FOLDER_NORMAL, ODOO_FOLDER_UPGRADE,
    ODOO_LOCAL_DATABASE, ODOO_LOCAL_URL,
    ODOO_EXTERNAL_DATABASE, ODOO_EXTERNAL_URL,
    ODOO_USER, ODOO_PASSWORD, USE_SUDO)

ODOO_UPDATE_SCRIPT = "../bin/start_openerp --stop-after-init"\
    " -u {module_list} -d {database_name}"

def _log(text):
    res = '%s - %s' % (datetime.today().strftime("%d-%m-%y - %H:%M:%S"), text)
    print res


def _bash_execute(bash, user=False, raise_error=True):
    my_list = []
    if USE_SUDO:
        my_list.append('sudo')
        if user:
            my_list += ['su', user]
    my_list += bash.split(' ')
    _log("CALLING %s" % (' '.join(my_list)))
    if raise_error:
        call(my_list)
    else:
        try:
            call(my_list)
        except e as exception:
            _log("ERROR : %s" % e.description)
            return False
    return True


def manage_odoo_process(active=False):
    _log("%s Odoo Process" % ('Start' if active else 'Stop'))
    if active:
        _bash_execute("service odoo start", raise_error=False)
    else:
        _bash_execute("service odoo stop", raise_error=False)


def set_upgrade_mode(upgrade_mode=False):
    _log("Set Upgrade mode to %s" % upgrade_mode)
    if upgrade_mode and not os.path.isdir(ODOO_FOLDER_BACKUP):
        os.rename(ODOO_FOLDER_NORMAL, ODOO_FOLDER_BACKUP)
        os.rename(ODOO_FOLDER_UPGRADE, ODOO_FOLDER_NORMAL)
    elif not upgrade_mode and os.path.isdir(ODOO_FOLDER_BACKUP):
        os.rename(ODOO_FOLDER_NORMAL, ODOO_FOLDER_UPGRADE)
        os.rename(ODOO_FOLDER_BACKUP, ODOO_FOLDER_NORMAL)


def execute_sql_file(database, sql_file):
    return _bash_execute(
        "psql -f %s %s -o zz_result_%s" % (sql_file, database, sql_file),
        user='postgres')


def create_new_database():
    _bash_execute("psql -l -o xx_database_list", user='postgres')
    file_database_list = open('xx_database_list', 'r')
    content = file_database_list.readlines()
    found = True
    i = 1
    database_name = False
    while found:
        database_name = '%s_%s' % (ODOO_LOCAL_DATABASE, str(i).zfill(3))
        found = ' %s ' % database_name in ''.join(content)
        i += 1
    _bash_execute(
        "createdb %s --template %s --owner odoo" % (
            database_name, ODOO_LOCAL_DATABASE), user='postgres')
    _bash_execute("rm xx_database_list")
    return database_name

def update_instance(database_name, module_list):
    _bash_execute(ODOO_UPDATE_SCRIPT.format(
        database_name=database_name, module_list=module_list))
