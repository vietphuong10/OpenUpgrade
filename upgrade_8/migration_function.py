# -*- coding: utf-8 -*-
import os
from subprocess import call
from datetime import datetime 

from secret_configuration import (
    ODOO_FOLDER_BACKUP, ODOO_FOLDER_NORMAL, ODOO_FOLDER_UPGRADE,
    ODOO_LOCAL_DATABASE, ODOO_LOCAL_URL,
    ODOO_EXTERNAL_DATABASE, ODOO_EXTERNAL_DATABASE,
    ODOO_USER, ODOO_PASSWORD)

def log(text):
    print '%s - %s' %(datetime.today().strftime("%d-%m-%y - %H:%M:%S"), text)

def manage_odoo_process(active=False):
    log("%s Odoo Process" % ('Start' if active else 'Stop'))
    if active:
        call(['sudo', 'service', 'odoo', 'start'])
    else:
        call(['sudo', 'service', 'odoo', 'stop'])

def set_upgrade_mode(upgrade_mode=False):
    log("Set Upgrade mode to %s" % upgrade_mode)
    if upgrade_mode and not os.path.isdir(ODOO_FOLDER_BACKUP):
        os.rename(ODOO_FOLDER_NORMAL, ODOO_FOLDER_BACKUP)
        os.rename(ODOO_FOLDER_UPGRADE, ODOO_FOLDER_NORMAL) 
    elif not upgrade_mode and os.path.isdir(ODOO_FOLDER_BACKUP): 
        os.rename(ODOO_FOLDER_NORMAL, ODOO_FOLDER_UPGRADE)
        os.rename(ODOO_FOLDER_BACKUP, ODOO_FOLDER_NORMAL)

def execute_sql_file(sql_file):
    log("Execute SQL File : %s" % (sql_file)
    call(['sudo', 'su', 'postgres', '"psql -f %s %s"' %(sql_file, ODOO_LOCAL_DATABASE)
