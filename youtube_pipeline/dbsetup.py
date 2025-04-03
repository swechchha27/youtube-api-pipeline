from pathlib import Path
from datetime import datetime
from config import *
from dbconnect import *

dbhost = DBCONFIG["ORACLE_HOST"]
dbport = DBCONFIG["ORACLE_PORT"]
dbservice = DBCONFIG["ORACLE_SERVICE"]
    
def get_dbbconfig(username):
    dbuser = DBCONFIG[f"{username}_USER"]
    dbrole = DBCONFIG.get(f"{username}_ROLE")
    dbpwd = DBCONFIG[f"{username}_PWD"]
    dsn_tns = oracledb.makedsn(
        host=dbhost,
        port=dbport,
        service_name=dbservice
    )
    return dbuser,dbrole,dbpwd,dsn_tns

def setup_database():
    dbfolder = DBSCRIPTFOLDER
    # Loop over all files inside folder order by sequence in their names
    for path in list(dbfolder.iterdir())[:1]:
        print(f"Executing {path.name}----------")
        username = str(path).split('_')[1]
        dbuser, dbrole, dbpwd, dsn_tns = get_dbbconfig(username)
        with get_connection(username=dbuser,password=dbpwd,dsn=dsn_tns,role=dbrole) as conn:
            execute_sql_file(conn, path)


if __name__=='__main__':
    # connect_oracle('SYS')
    setup_database()