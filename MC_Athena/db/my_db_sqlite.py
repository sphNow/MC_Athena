# -*- coding: utf-8 -*-

"""
LEFT ==> subst( campo, 1, fin)
MID ==>  subst( campo, inicio, fin)
LEN ==> LENGTH
IIF ==> CASE WHEN condicion THEN true ELSE false END
INSTR ==> INSTR( campo, valor_buscado)

"""


import sqlite3
import pandas as pd
from config import *

def openConnection(database=dbName):
    try:
        sqliteConnection = sqlite3.connect(database)  # ('Car_Database.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        # print("SQLite Database Version is: ", record)
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def exeDQLQuery(query, database=dbName):
    df = None
    con = None
    try:
        con = sqlite3.connect(database, timeout=toMax)
        df = pd.read_sql_query(query, con)
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if con:
            con.close()
    return df

def exeDMLQuery(query, database=dbName):
    changes = 0
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        cursor.execute(query)
        sqliteConnection.commit()
        cursor.close()
        changes = sqliteConnection.total_changes
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    return changes

def exeManyQuery(query, data, database=dbName):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(database, timeout=toMax)
        cursor = sqliteConnection.cursor()
        cursor.executemany(query, data)
        cursor.close()
        # cursor.commit()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.commit()
            sqliteConnection.close()

def importFromDataFrame(df, tableName, database=dbName):
    sqliteConnection = None
    changes = 0
    try:
        sqliteConnection = sqlite3.connect(database, timeout=toMax)
        cursor = sqliteConnection.cursor()
        for row in df.values.tolist():
            sql_insert2 = "INSERT INTO QEF_REPORT VALUES ('" + "','".join(row) + "')"
            cursor.execute(sql_insert2)
            changes = changes + 1
        # cursor.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.commit()
            sqliteConnection.close()
    return changes

def importFromDataFrameMail(df, database=dbName):
    sqliteConnection = None
    changes = 0
    try:
        sqliteConnection = sqlite3.connect(database, timeout=toMax)
        cursor = sqliteConnection.cursor()
        for row in df.values.tolist():
            sql_insert2 = "INSERT INTO QEF_MAIL VALUES ('" + "','".join(row) + "')"
            cursor.execute(sql_insert2)
            changes = changes + 1
        # cursor.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.commit()
            sqliteConnection.close()
    return changes

def save_email_unit_report_time(unit, calc_date, mail_time, database=dbName):
    sqliteConnection = None
    changes = 0
    try:
        sqliteConnection = sqlite3.connect(database, timeout=toMax)
        cursor = sqliteConnection.cursor()
        sql_insert2 = "INSERT INTO QEF_MAIL_RECEIVED VALUES ('" + unit + "','" + calc_date + "','" + mail_time + "')"
        cursor.execute(sql_insert2)
        # cursor.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.commit()
            sqliteConnection.close()
    return changes
