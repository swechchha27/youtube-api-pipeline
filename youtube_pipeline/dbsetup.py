from pathlib import Path
from datetime import datetime
from config import *
from dbconnect import *

dbhost = DBCONFIG["ORACLE_HOST"]
dbport = DBCONFIG["ORACLE_PORT"]
dbservice = DBCONFIG["ORACLE_SERVICE"]
    
def connect_oracle(username):
    # oracle db config
    dbuser = DBCONFIG[f"{username}_USER"]
    dbrole = DBCONFIG.get(f"{username}_ROLE")
    dbpwd = DBCONFIG[f"{username}_PWD"]
    dsn_tns = oracledb.makedsn(
        host=dbhost,
        port=dbport,
        service_name=dbservice
    )
    try:
        connection = get_connection(
                    username=dbuser, 
                    password=dbpwd, 
                    dsn=dsn_tns, 
                    role=dbrole
                    )
        for row in execute_query(
            conn=connection,
            query='SELECT SYSDATE FROM DUAL'
            ):
            print(datetime.strptime(str(row[0]), "%Y-%m-%d %H:%M:%S"))
    except oracledb.Error as error:
        print(f"Error connecting to database: {error}")
        if connection:
            close_connection(connection)
        

def setup_database():
    dbfolder = DBSCRIPTFOLDER
    # Loop over all files inside folder order by sequence in their names
    pass

if __name__=='__main__':
    connect_oracle('SYS')