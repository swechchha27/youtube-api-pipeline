-- Create users for the database in an idempotent manner

DECLARE
    USERNAME VARCHAR2(20);
    EXISTS INTEGER;

    PROCEDURE proc_create_user(PIV_USER IN VARCHAR2, PON_COUNT OUT INTEGER) IS
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM dba_users WHERE username = PIV_USER) THEN
            EXECUTE IMMEDIATE 'CREATE USER :username IDENTIFIED BY oracle' USING PIV_USER;
            EXECUTE IMMEDIATE 'GRANT CONNECT, RESOURCE TO :username' USING PIV_USER;
            EXECUTE IMMEDIATE 'ALTER USER :username DEFAULT TABLESPACE users 
                                QUOTA UNLIMITED ON users' USING PIV_USER;
            IF PIV_USER = 'ETL_DEV' THEN
                EXECUTE IMMEDIATE 'GRANT CREATE SESSION TO :username' USING PIV_USER;
                EXECUTE IMMEDIATE 'GRANT CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE, 
                           CREATE TRIGGER, CREATE SYNONYM, CREATE TYPE, CREATE MATERIALIZED VIEW 
                           TO :username' USING PIV_USER;
            ELSIF PIV_USER = 'LOG' THEN
                EXECUTE IMMEDIATE 'GRANT CREATE TABLE, CREATE SEQUENCE, CREATE PROCEDURE, CREATE TRIGGER,
                           CREATE SYNONYM, CREATE TYPE TO :username' USING PIV_USER;
            ELSIF PIV_USER = 'STAGE' THEN
                EXECUTE IMMEDIATE 'GRANT CREATE TABLE, CREATE SEQUENCE TO :username' USING PIV_USER;
            END IF;
            
            -- Return a counter to verify if user created successfully.
            SELECT COUNT(username) 
            INTO PON_COUNT
            FROM dba_users 
            WHERE username = PIV_USER;

        ELSE
            DBMS_OUTPUT.PUT_LINE(PIV_USER || ' user already exists. No action needed.');
        END IF;
    EXCEPTION WHEN OTHERS THEN
        RAISE_APPLICATION_ERROR('20001', 'Unknown Exception during creation of user' || PIV_USER);
    END;
BEGIN

    -- Create ETL developer user
    USERNAME := 'ETL_DEV';
    EXISTS := 0;
    EXISTS := PROCEDURE(USERNAME);
    IF EXISTS > 0 THEN
        DBMS_OUTPUT.PUT_LINE(USERNAME || ' user created successfully.');
    ELSE
        RAISE_APPLICATION_ERROR('20001', 'Unknown error during creation of user' || USERNAME);
    END IF;


    -- Create log user
    USERNAME := 'LOG';
    EXISTS := 0;
    EXISTS := PROCEDURE(USERNAME);
    IF EXISTS > 0 THEN
        DBMS_OUTPUT.PUT_LINE(USERNAME || ' user created successfully.');
    ELSE
        RAISE_APPLICATION_ERROR('20001', 'Unknown error during creation of user' || USERNAME);
    END IF;

    -- Create staging schema
    USERNAME := 'STAGE';
    EXISTS := 0;
    EXISTS := PROCEDURE(USERNAME);
    IF EXISTS > 0 THEN
        DBMS_OUTPUT.PUT_LINE(USERNAME || ' user created successfully.');
    ELSE
        RAISE_APPLICATION_ERROR('20001', 'Unknown error during creation of user' || USERNAME);
    END IF;

EXCEPTION WHEN OTHERS THEN
    RAISE_APPLICATION_ERROR('20001', 'Unknown Exception during setting users');
END;
/