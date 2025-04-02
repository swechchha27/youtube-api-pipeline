-- Create admin user for data warehouse ETL
DECLARE
    USERNAME VARCHAR2(20) := 'ETL_ADMIN';
BEGIN
    IF NOT EXISTS (SELECT 1 FROM dba_users WHERE username = USERNAME) THEN
        EXECUTE IMMEDIATE 'CREATE USER :username IDENTIFIED BY oracle' USING USERNAME;
        EXECUTE IMMEDIATE 'GRANT DBA TO :username' USING USERNAME;
        EXECUTE IMMEDIATE 'ALTER USER :username DEFAULT TABLESPACE users 
                            QUOTA UNLIMITED ON users' USING USERNAME;
        
        -- Verify if the user created successfully
        IF (SELECT username FROM dba_users WHERE username = USERNAME) = USERNAME THEN
            DBMS_OUTPUT.PUT_LINE(USERNAME || ' user created successfully.');
        ELSE
            RAISE_APPLICATION_ERROR('20001', 'Unknown error during creation of user' || USERNAME);
        END IF;
    ELSE
        DBMS_OUTPUT.PUT_LINE(USERNAME || ' user already exists. No action needed.');
    END IF;
EXCEPTION WHEN OTHERS THEN
    RAISE_APPLICATION_ERROR('20001', 'Unknown Exception during creation of user' || USERNAME);
END;
/