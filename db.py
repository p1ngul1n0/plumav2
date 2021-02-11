import sqlite3
import uuid


def connect():
    conn = sqlite3.connect('db/database.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def initDatabase():
    conn = connect()
    conn.execute("CREATE TABLE OPTIONS (OPTION TEXT PRIMARY KEY NOT NULL, VALUE TEXT NOT NULL);")
    optionSet('proxy','')
    optionSet('payload_file','list.txt')
    conn.execute("""CREATE TABLE SCANS (UUID TEXT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, URL TEXT NOT NULL, 
                    STATUS TEXT NOT NULL, ENUMERATION INTEGER NOT NULL, SPIDERING INTEGER NOT NULL);""")
    conn.execute("""CREATE TABLE RESULTS (UUID TEXT NOT NULL, TYPE TEXT NOT NULL, 
                    KEY TEXT NOT NULL, VALUE TEXT NOT NULL);""")

    conn.commit()
    conn.close()
    return True

# Options DB functions

def optionReset():
    conn = connect()
    conn.execute("DROP TABLE OPTIONS")
    conn.execute("CREATE TABLE OPTIONS (OPTION TEXT PRIMARY KEY NOT NULL, VALUE TEXT NOT NULL);")
    conn.commit()
    conn.close()
    return True

def optionSet(option, value):
    conn = connect()
    conn.execute(f"INSERT INTO OPTIONS (OPTION, VALUE) VALUES (?, ?);", [option, value])
    conn.commit()
    conn.close()
    return True

def optionUpdate(option, value):
    conn = connect()
    conn.execute(f"UPDATE OPTIONS set VALUE = ? where OPTION = ?;", [value, option])
    conn.commit()
    conn.close()
    return True

def optionGet(option):
    conn = connect()
    cursor = conn.execute(f"SELECT VALUE from OPTIONS WHERE OPTION = ?;", [option])
    data = cursor.fetchone()[0]
    conn.close()
    return data

# Scans DB

def scanReset():
    conn = connect()
    conn.execute("DROP TABLE SCANS")
    conn.execute("""CREATE TABLE SCANS (UUID TEXT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL,
                    URL TEXT NOT NULL, STATUS TEXT NOT NULL, ENUMERATION INTEGER NOT NULL, 
                    SPIDERING INTEGER NOT NULL);""")
    conn.commit()
    conn.close()
    return True

def scanSet(name, url, enumeration):
    conn = connect()
    conn.execute(f"""INSERT INTO SCANS (UUID, NAME, URL, STATUS, ENUMERATION, SPIDERING) VALUES 
                (?, ?, ?, 'not executed', ?, '0');""", [str(uuid.uuid4()), name, url, enumeration])
    conn.commit()
    conn.close()
    return True

def scanUpdate(uuid, name, url, enumeration, spidering):
    conn = connect()
    conn.execute(f"""UPDATE SCANS set NAME = ?, URL = ?, 
                ENUMERATION = ?, SPIDERING = ? where UUID = ?;""", [name, url, enumeration, spidering, uuid])
    conn.commit()
    conn.close()
    return True

def scanStatus(uuid,status):
    conn = connect()
    conn.execute(f"UPDATE SCANS set STATUS = ? where UUID = ? ;", [status, uuid])
    conn.commit()
    conn.close()
    return True

def scanDelete(uuid):
    conn = connect()
    conn.execute(f"DELETE from SCANS where UUID = ?;", [uuid])
    conn.commit()
    conn.close()
    resultDelete(uuid)
    return True

def scanGet(uuid):
    conn = connect()
    cursor = conn.execute(f"SELECT UUID, NAME, URL, STATUS, ENUMERATION, SPIDERING from SCANS WHERE UUID = ?;", [uuid])
    scan = {}
    result = cursor.fetchone()
    for key in result.keys():
        scan[key.lower()] = result[key]
    conn.close()
    return scan

def scanGetAll():
    conn = connect()
    cursor = conn.execute("SELECT UUID, NAME, URL, STATUS, ENUMERATION, SPIDERING from SCANS;")
    scans = []
    results = cursor.fetchall()
    for row in results:
        scan = {}
        for key in row.keys():
            scan[key.lower()] = row[key]
        scans.append(scan)
    conn.close()
    return scans

# Results DB

def resultReset():
    conn = connect()
    conn.execute("DROP TABLE RESULTS")
    conn.execute("""CREATE TABLE RESULTS (UUID TEXT PRIMARY KEY NOT NULL, TYPE TEXT NOT NULL, 
                    KEY TEXT NOT NULL, VALUE TEXT NOT NULL);""")
    conn.commit()
    conn.close()
    return True

def resultSet(uuid, type, key, value):
    conn = connect()
    conn.execute("INSERT INTO RESULTS (UUID, TYPE, KEY, VALUE) VALUES (?,?,?,?);", [uuid, type, key, str(value)])
    conn.commit()
    conn.close()
    return True

def resultGet(uuid, type, key):
    conn = connect()
    cursor = conn.execute(f"SELECT VALUE from RESULTS WHERE UUID = ? AND TYPE = ? AND KEY = ?;", [uuid, type, key])
    data = cursor.fetchone()[0]
    conn.close()
    return data

def resultDelete(uuid):
    conn = connect()
    conn.execute(f"DELETE from RESULTS where UUID = ?;", [uuid])
    conn.commit()
    conn.close()
    return True