#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import subprocess

def ExecuteCommand(cmd):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>> %s" % cmd
    subprocess.call(cmd, shell=True)

for modules in sys.argv[1:]:
    # Drop Database if exists
    dbName = "test__%s" % (modules.replace(',', '_'))
    try:
        ExecuteCommand("dropdb %s" % dbName)
    except:
        pass
    ExecuteCommand("createdb %s" % dbName)

    ExecuteCommand("ak run -d %s -i %s --stop-after-init" % (dbName, modules))
