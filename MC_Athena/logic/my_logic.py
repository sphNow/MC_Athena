# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 09:04:57 2022

@author: n54286
"""
from datetime import datetime
import os
import shutil
import pandas as pd
from config import *
from pyQtTest.db.my_db_sqlite import exeDQLQuery, exeDMLQuery



def get_user_logged() -> object:
    return os.environ.get("username")

def get_init_PIF_path():
    #return "./Athena/doc/template"
    return app_pif_path

def get_local_dwnload_path():
    return os.path.expanduser('~') + "\Downloads\\"

def get_dwnload_path():
    #return os.path.expanduser('~') + "\Downloads\\"
    return app_net_path

def check_Athena_version():
    # Get rowid from inserted record
    msg = "ok"
    sql_sel = " SELECT VER_VERSION, VER_PATH_DISTRIBUCION, VER_NOMBRE_BD " \
              " FROM M_VER_VERSIONES " \
              " WHERE " \
              " VER_ACTIVO ='True';"

    app_version = exeDQLQuery(sql_sel, dbName)
    if len(app_version) > 0:
        # Get Athena version
        if str(app_version['VER_VERSION'][0]) != version:
            file_path = str(app_version['VER_PATH_DISTRIBUCION'][0])
            file_name = str(app_version['VER_NOMBRE_BD'][0])
            # Check if its already downloaded
            if not os.path.exists(os.getcwd() + file_name):
                # Check if its at net
                if os.path.exists(str(file_path)):
                    shutil.copy2(os.getcwd() + file_name, str(file_path))
                    msg = "Donwloaded last version [" + version + "]. Please use that one from now on, you will find it at the same path from this exe file."
                else:
                    msg = "Last version [" + version + "] is required but not found at net folder in order to provide it. This version is mandatory, sorry for any inconvenience."
            else:
                msg = "Last version [" + version + "] is required and downloaded. This version is mandatory, use that version from now on, sorry for any inconvenience."
        else:
            msg = "ok"
        return msg

def do_load_pending_mails():
    # Get rowid from inserted record
    sql_sel = " SELECT ROWID, * FROM _09_MAL_MAILS_LEIDOS; "
    return exeDQLQuery(sql_sel, dbName_GAP)
