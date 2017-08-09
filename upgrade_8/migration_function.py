# -*- coding: utf-8 -*-
import os
import signal
import time
import traceback

from subprocess import call, Popen
from datetime import datetime

from migration_import import erppeek

from secret_configuration import (
    ODOO_FOLDER_BACKUP, ODOO_FOLDER_NORMAL, ODOO_FOLDER_UPGRADE,
    ODOO_LOCAL_DATABASE, ODOO_LOCAL_URL,
    #    ODOO_EXTERNAL_DATABASE, ODOO_EXTERNAL_URL,
    ODOO_USER, ODOO_PASSWORD, USE_SUDO)


ODOO_UPDATE_SCRIPT = "../bin/start_openerp --stop-after-init"\
    " -u {module_list} -d {database}"


ODOO_RUN_SCRIPT = "../bin/start_openerp"


def _log(text, error=False):
    res = '%s - %s' % (datetime.today().strftime("%d-%m-%y - %H:%M:%S"), text)
    print res
    if error:
        traceback.print_stack()
        print error


def _generate_command(command, user):
    if not USE_SUDO:
        return command
    elif not user:
        return 'sudo %s' % command
    else:
        return 'sudo su %s -c "%s"' % (user, command)


def _bash_execute(command, user=False):
    full_command = _generate_command(command, user)
    _log("CALLING (Sync) %s" % full_command)
    try:
        call(full_command, shell=True)
    except Exception as e:
        _log("ERROR during the execution", e)
        return False
    return True


def _bash_subprocess(command, user=False):
    full_command = _generate_command(command, user)
    _log("CALLING (async) %s" % full_command)
    try:
        res = Popen(full_command, shell=True)
    except Exception as e:
        _log("ERROR during the execution", e)
        return False
    return res


def manage_odoo_process(active=False):
    _log("%s Odoo Process" % ('Start' if active else 'Stop'))
    if active:
        _bash_execute("service odoo start")
    else:
        _bash_execute("service odoo stop")


def set_upgrade_mode(upgrade_mode):
    _log("Set Upgrade mode to %s" % upgrade_mode)
    if upgrade_mode and not os.path.isdir(ODOO_FOLDER_BACKUP):
        os.rename(ODOO_FOLDER_NORMAL, ODOO_FOLDER_BACKUP)
        os.rename(ODOO_FOLDER_UPGRADE, ODOO_FOLDER_NORMAL)
        os.mkdir(ODOO_FOLDER_UPGRADE)
    elif not upgrade_mode and os.path.isdir(ODOO_FOLDER_BACKUP):
        os.rmdir(ODOO_FOLDER_UPGRADE)
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
    database = False
    while found:
        database = '%s_%s' % (ODOO_LOCAL_DATABASE, str(i).zfill(3))
        found = ' %s ' % database in ''.join(content)
        i += 1
    _bash_execute(
        "createdb %s --template %s --owner odoo" % (
            database, ODOO_LOCAL_DATABASE), user='postgres')
    _bash_execute("rm xx_database_list")
    return database


def backup_database(database, step_name):
    backup = '%s___%s' % (database, step_name)
    # Search for previous backup
    _bash_execute("psql -l -o xx_database_list", user='postgres')
    file_database_list = open('xx_database_list', 'r')
    content = file_database_list.readlines()
    found = ' %s ' % backup in ''.join(content)
    if found:
        # Drop previous backup
        _bash_execute("dropdb %s" % backup, user='postgres')
    # Backup Database
    _bash_execute(
        "createdb %s --template %s --owner odoo" % (
            backup, database), user='postgres')
    _bash_execute("rm xx_database_list")


def update_instance(database, module_list):
    _bash_execute(
        ODOO_UPDATE_SCRIPT.format(database=database, module_list=module_list))


def run_instance():
    res = _bash_subprocess(ODOO_RUN_SCRIPT)
    time.sleep(5)
    return res


def kill_process(process):
    pid = process.pid
    _log("KILL Process #%d" % (pid))
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(5)
        if process.poll() is None:  # Force kill if process is still alive
            os.killpg(pid, signal.SIGKILL)
    except Exception as e:
        _log("ERROR during the kill of #d process" % pid, e)


def _connect_instance(url, database, login, password):
    try:
        openerp = erppeek.Client(url)
    except Exception as e:
        _log("ERROR : Connection to odoo instance '%s' failed" % url, e)
        return False
    try:
        openerp.login(
            login, password=password, database=database)
    except Exception as e:
        _log("ERROR : Authentication failed on %s with %s login" % (
            url, login), e)
        return False
    return openerp


def install_modules(database, module_list):
    # Update module list
    openerp = _connect_instance(
        ODOO_LOCAL_URL, database, ODOO_USER, ODOO_PASSWORD)
    if not openerp:
        _log("FATAL : install process aborted")
        return
    _log("Update modules list...")
    openerp.IrModuleModule.update_list()

    # Install each module
    for module_name in module_list:
        openerp = _connect_instance(
            ODOO_LOCAL_URL, database, ODOO_USER, ODOO_PASSWORD)
        if not openerp:
            _log("FATAL : install process aborted")
            return
        modules = openerp.IrModuleModule.browse([('name', '=', module_name)])
        if len(modules) == 0:
            _log("ERROR : Module not found %s" % module_name)
        else:
            module = modules[0]
            if modules[0].state in ['uninstalled', 'to install']:
                _log("Installing... %s" % module.name)
                try:
                    openerp.IrModuleModule.button_immediate_install(
                        [module.id])
                except Exception as e:
                    _log("ERROR during '%s' installation" % module_name, e)
            else:
                _log("WARNING : '%s' module in '%s' state" % (
                    module.name, module.state))

def uninstall_modules(database, module_list):
    # Uninstall each module
    for module_name in module_list:
        openerp = _connect_instance(
            ODOO_LOCAL_URL, database, ODOO_USER, ODOO_PASSWORD)
        if not openerp:
            _log("FATAL : uninstall process aborted")
            return
        modules = openerp.IrModuleModule.browse([('name', '=', module_name)])
        if len(modules) == 0:
            _log("ERROR : Module not found %s" % module_name)
        else:
            module = modules[0]
            if modules[0].state not in ['uninstalled']:
                _log("Uninstalling... %s" % module.name)
                try:
                    openerp.IrModuleModule.module_uninstall([module.id])
                except Exception as e:
                    _log("ERROR during '%s' uninstallation" % module_name, e)
            else:
                _log("WARNING : '%s' module in '%s' state" % (
                    module.name, module.state))
