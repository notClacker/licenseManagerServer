import datetime
import sqlite3
import time

import cfg
from cfg import logger

def check_for_resolved_symbol(data: str
                            , resolved_symbols: str
                            , resolved_len: int) -> bool:   
        for symbol in data:
            if symbol not in resolved_symbols:
                return False
        return (len(data) < resolved_len)


# Should return the all data about user by license key
# Else return empty list 
def get_row_by_license_key(license_key: str) -> tuple:
    user_row = []
    conn = sqlite3.connect(cfg.g_user_db_path)
    cursor = conn.cursor()
    try:
        row = cfg.g_db_full_row
        column_name = cfg.g_db_license_key
        table_name = cfg.g_db_table_name
        request = "SELECT %s FROM %s WHERE %s = '%s'" % (row, table_name, column_name, license_key)
        cursor.execute(request)
        user_row = cursor.fetchone()      
        logger.debug(user_row)
    except sqlite3.DatabaseError as err:
        logger.error(license_key)
        logger.error(err)
        time.sleep(cfg.g_error_sleep_sec)

    conn.close()
    if user_row == None:
        user_row = []
    return user_row

    
def activate_user_by_id(id_db: int
                        , hwid_db: str, expiration_date: datetime) -> None:
    conn = sqlite3.connect(cfg.g_user_db_path)
    cursor = conn.cursor()
    try:
        table_name = cfg.g_db_table_name
        column_id = cfg.g_db_column_id
        column_hwid = cfg.g_db_column_hwid
        column_expiration_date = cfg.g_db_column_expiration_date

        request = """ UPDATE %s
            SET %s = '%s',
                %s = '%s'
            WHERE %s = %d
           """ % (table_name, column_hwid, hwid_db
                  , column_expiration_date, expiration_date
                  , column_id, id_db)
        
        cursor.execute(request)
    except sqlite3.DatabaseError as err:
        symbol = cfg.separateSymbol
        user_metadata = symbol.join([str(id_db), hwid_db, expiration_date])
        logger.error(user_metadata)
        logger.error(err)
        time.sleep(cfg.g_error_sleep_sec)
    else:
        conn.commit()
    conn.close()
    

def get_user_state(request: str, license_key: str
                    , hwid: str, ip: str) -> str:
    # THE MAIN CHECK FOR THE SQL INJECTION
    # Check for hacking the input data
    if not (check_for_resolved_symbol(license_key, 
                cfg.g_resolved_symbols_for_key, 
                cfg.g_max_license_key_len
                ) and check_for_resolved_symbol(
                        hwid,
                        cfg.g_resolved_symbols_for_hwid,
                        cfg.g_max_license_hwid_len)):
        return cfg.g_user_state_hacker
        
    # Parsing the SQL row
    user_row = get_row_by_license_key(license_key)  
        
    if len(user_row) == 0:
        return cfg.g_user_state_wrong_license_key

    if len(user_row) < cfg.db_rows.ROWS_COUNT:
        logger.critical("INVALID ROW COUNT")
        return cfg.g_user_state_undefined

    id_db = int(user_row[int(cfg.db_rows.ID)])
    hwid_db = str(user_row[cfg.db_rows.HWID])
    validity_days_db = int(user_row[cfg.db_rows.VALIDITY_DAYS])
    expiration_date = user_row[cfg.db_rows.EXPIRATION_DATE]
    subscribe_type = user_row[cfg.db_rows.SUBSCRIBE_TYPE]
    current_date = datetime.datetime.now()
    
    logger.debug(user_row)

    # Check hwid
    if hwid_db == 'None':
        # Add hwid user to db
        expiration_date = current_date + datetime.timedelta(days=validity_days_db)
        activate_user_by_id(id_db, hwid, expiration_date)     
        # Continue to check the parameters
    elif hwid != hwid_db:
        return cfg.g_user_state_other_pc

    # HWID in db
    # Check the expiration date                 
    expiration_date_obj = datetime.datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S.%f')
    if current_date > expiration_date_obj:
        return cfg.g_user_state_outdated_license_key

    # Check for BUG (subscribe_type existing)
    current_type = cfg.subcribe_types.get(subscribe_type)
    if current_type == None:                
        logger.critical("Subscribe type DOESN'T exist")
        return cfg.g_state_coder_error

    # Check the subscribe_type
    if current_type.get(request) != None:
        return cfg.g_user_state_ok
    else:
        return cfg.g_user_state_other_subscribe_type

class UserDB(object):
    __db_path = cfg.g_user_db_path

    def __init__(self):
        pass


    def __check_for_resolved_symbol(self, data: str
                                    , resolved_symbols: str
                                    , resolved_len: int) -> bool:   
        for symbol in data:
            if symbol not in resolved_symbols:
                return False
        return (len(data) < resolved_len)


    # Should return the all data about user by license key
    # Else return empty list 
    def __get_row_by_license_key(self, license_key: str) -> tuple:
        user_row = []
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        try:
            row = cfg.g_db_full_row
            column_name = cfg.g_db_license_key
            table_name = cfg.g_db_table_name
            request = "SELECT %s FROM %s WHERE %s = '%s'" % (row, table_name, column_name, license_key)
            cursor.execute(request)
            user_row = cursor.fetchone()      
            logger.debug(user_row)
        except sqlite3.DatabaseError as err:
            logger.error(license_key)
            logger.error(err)
            time.sleep(cfg.g_error_sleep_sec)

        conn.close()
        user_row = [] if user_row == None else user_row
        return user_row

    
    def __activate_user_by_id(self, id_db: int
                              , hwid_db: str, expiration_date: datetime) -> None:
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        try:
            table_name = cfg.g_db_table_name
            column_id = cfg.g_db_column_id
            column_hwid = cfg.g_db_column_hwid
            column_expiration_date = cfg.g_db_column_expiration_date

            request = """ UPDATE %s
            SET %s = '%s',
                %s = '%s'
            WHERE %s = %d
           """ % (table_name, column_hwid, hwid_db
                  , column_expiration_date, expiration_date
                  , column_id, id_db)
        
            cursor.execute(request)
        except sqlite3.DatabaseError as err:
            symbol = cfg.separateSymbol
            user_metadata = symbol.join([str(id_db), hwid_db, expiration_date])
            logger.error(user_metadata)
            logger.error(err)
            time.sleep(cfg.g_error_sleep_sec)
        else:
            conn.commit()
        conn.close()
    

    def get_user_state(self, request: str, license_key: str
                       , hwid: str, ip: str) -> str:
        # THE MAIN CHECK FOR THE SQL INJECTION
        # Check for hacking the input data
        if not (self.__check_for_resolved_symbol(license_key, 
                            cfg.g_resolved_symbols_for_key, 
                            cfg.g_max_license_key_len
                        ) and self.__check_for_resolved_symbol(
                            hwid,
                            cfg.g_resolved_symbols_for_hwid,
                            cfg.g_max_license_hwid_len)): 
            return cfg.g_user_state_hacker
        
        # Parsing the SQL row
        user_row = self.__get_row_by_license_key(license_key)  
        
        if len(user_row) == 0:
            return cfg.g_user_state_wrong_license_key

        if len(user_row) < cfg.db_rows.ROWS_COUNT:
            logger.critical("INVALID ROW COUNT")
            return cfg.g_user_state_undefined

        id_db = int(user_row[int(cfg.db_rows.ID)])
        hwid_db = str(user_row[cfg.db_rows.HWID])
        validity_days_db = int(user_row[cfg.db_rows.VALIDITY_DAYS])
        expiration_date = user_row[cfg.db_rows.EXPIRATION_DATE]
        subscribe_type = user_row[cfg.db_rows.SUBSCRIBE_TYPE]
        current_date = datetime.datetime.now()
        
        logger.debug(user_row)

        # Check hwid
        if hwid_db == 'None':
            # Add hwid user to db
            expiration_date = current_date + datetime.timedelta(days=validity_days_db)
            self.__activate_user_by_id(id_db, hwid, expiration_date)     
            # Continue to check the parameters
        elif hwid != hwid_db:
            return cfg.g_user_state_other_pc

        # HWID in db
        # Check the expiration date                 
        expiration_date_obj = datetime.datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S.%f')
        if current_date > expiration_date_obj:
            return cfg.g_user_state_outdated_license_key

        # Check for BUG (subscribe_type existing)
        allowed_cmds = cfg.g_allowed_commands_by_subscribe_type.get(subscribe_type)
        if allowed_cmds == None:                
            logger.critical("Subscribe type DOESN'T exist")
            return cfg.g_user_state_undefined

        # Check the subscribe_type
        if allowed_cmds.get(request) != None:
            return cfg.g_user_state_ok
        else:
            return cfg.g_user_state_other_subscribe_type


