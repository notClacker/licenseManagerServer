import sqlite3
import time

import db_interface
import cfg
from cfg import logger


def remember_hacker():
    pass


def get_response_by_request(request: str) -> str:
    response = '0'
    if request == "mo":
        response = cfg.data_to_buyers.main_offset
    elif request == "ek":
        # response = str(cfg.encrypted_key)
        pass
    else:
        response = "It's else"
    return response


def get_response_by_user_data(request: str, license_key: str, hwid: str, ip: str) -> str:
    user_db = db_interface.UserDB()
    user_state = user_db.get_user_state(license_key, hwid, ip)

    if user_state == cfg.g_user_state_ok:
        logger.info(cfg.g_user_state_ok)
        return get_response_by_request(request)
    else:
        symbol = cfg.separateSymbol        
        user_metadata = symbol.join([license_key, hwid, ip])
        logger.warning(user_metadata)
        if user_state == cfg.g_user_state_wrong_license_key:
            logger.warning(cfg.g_user_state_wrong_license_key)
            #return cfg.g_user_state_wrong_license_key
        elif user_state == cfg.g_user_state_outdated_license_key:
            logger.warning(cfg.g_user_state_outdated_license_key)
            #return cfg.g_user_state_outdated_license_key
        elif user_state == cfg.g_user_state_other_pc:
            logger.warning(cfg.g_user_state_other_pc)
            #return cfg.g_user_state_other_pc
        elif user_state == cfg.g_user_state_hacker:
            logger.critical(user_metadata)
            logger.critical(cfg.g_user_state_hacker)           
            remember_hacker()
            #raise g_user_state_hacker
            #return cfg.g_user_state_hacker
        else:
            logger.warning(cfg.g_user_state_undefined)
            #return cfg.g_user_state_undefined
    return cfg.g_user_state_undefined


def processingRequest(data_bytes: str, ip="127.0.0.1") -> bytes:
    response = '0'
    for attempts in range(cfg.g_max_attempts):  
        try:
            data = data_bytes.decode('ascii').lower()            
            data_list = data.split(cfg.separateSymbol)

            # check for hacker
            if len(data_list) < 3:
                logger.warning([data_bytes, ip])
                logger.warning(cfg.g_user_state_hacker)
                remember_hacker()
                break

            request = data_list[0]
            license_key = data_list[1]
            hwid = data_list[2]
    
            response = get_response_by_user_data(request, license_key, hwid, ip)
            
        except Exception as e:
            args = e.args
            data = data_bytes.decode('ascii')
            user_metadata = data + cfg.separateSymbol + ip
            logger.error(user_metadata)
            logger.error(args)
            time.sleep(cfg.g_error_sleep_sec)
        else:
            break
        
    return bytes(response, encoding = 'ascii')