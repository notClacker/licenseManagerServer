
import sqlite3
import time

import db_interface
import cfg


def get_response_by_request(request: str, license_key: str, hwid: str, ip: str) -> str:
    user_db = db_interface.UserDB()
    user_state = user_db.get_user_state(license_key, hwid, ip)

    response = '0'
    if user_state == cfg.g_user_state_ok:
        if request == "mo":
            response = cfg.data_to_buyers.main_offset
        elif request == "ek":
            # response = str(cfg.encrypted_key)
            pass
        else:
            response = "It's else"
    elif user_state == cfg.g_user_state_wrong_license_key:
        response = "Wrong license key"
    elif user_state == cfg.g_user_state_outdated_license_key:
        response = "Outdated license key"
    elif user_state == cfg.g_user_state_other_pc:
        response = "Other pc"
    else:
        response = "hacker?"
    return response

def processingRequest(data_bytes, ip="127.0.0.1"):
    response = '0'
    for attempts in range(cfg.g_max_attempts):  
        try:
            data = data_bytes.decode('ascii').lower()            
            data_list = data.split(cfg.separateSymbol)

            if len(data_list) < 3:
                raise Exception(cfg.g_hacker_string_warning)

            request = data_list[0]
            license_key = data_list[1]
            hwid = data_list[2]
    
            response = get_response_by_request(request, license_key, hwid, ip)

# !! should the complete coding exception handling
        except Exception as e:
            args = e.args
            if len(args) == 1 and args[0] == cfg.g_hacker_string_warning:
                # Write to hackers_db
                print("\n hacker detected \n")
                break
            else:
                print(args)
                # Handle Exception
                print(Exception)
                time.sleep(cfg.g_error_sleep_sec)
        else:
            break
        
    return bytes(response, encoding = 'ascii')