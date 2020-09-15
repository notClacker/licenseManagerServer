try:
    from logger import logger
except Exception:
    from server_license_manager.logger import logger

# data to configurate server to working
separateSymbol = '|'
HOST = '0.0.0.0'
PORT = 2222
g_count_of_received_symbols = 100
g_user_db_path = "user_db.sql"
g_empty_response = '0'

# security variables
g_error_sleep_sec = 0.04        
g_hacker_string_warning = "hacker"
g_max_attempts = 10

g_user_state_ok = "ok"
g_user_state_other_subscribe_type = "other_subscribe_type"
g_user_state_outdated_license_key = "outdated_license_key"
g_user_state_wrong_license_key = "wrong_license_key"
g_user_state_other_pc = "other_pc"
g_user_state_hacker = "hacker"
g_user_state_undefined = "undefined_behavior"

class db_rows(object):
    ID = 0
    LICENSE_KEY = 1
    HWID = 2
    VALIDITY_DAYS = 3
    EXPIRATION_DATE = 4
    SUBSCRIBE_TYPE = 5
    ROWS_COUNT = 6

g_db_full_row = "*"
g_db_table_name = "users_licenses"
g_db_license_key = "license_key"
g_db_column_id = "user_id"
g_db_column_hwid = "hwid"
g_db_column_expiration_date = "expiration_date"

g_resolved_symbols_for_hwid =   "0123456789-abcdef"   # hexdigits + '-'
g_max_license_hwid_len = 22  # example of hwid is BFEBFBFF00040651

g_resolved_symbols_for_key =    "0123456789-abcdef"    # hexdigits + '-'
g_max_license_key_len = 30  # example of key is 01234-56789-abcde-f0123-45678


#map_base = ("mo0", "332241")
#player_base = ("mo1", "445566")

#type_snav_trial = ("type_0", dict(map_base))
#type_snav_full = ("type_1", dict(map_base, player_base))

#g_allowed_commands_by_subscribe_type = dict(type_snav_trial, type_snav_full)

g_main_offsets = ['250', '251', '252', '253']
class data_to_buyers(object):    
    #main_offset = '255'          #0xFF
    encrypted_key = '789'

    @staticmethod
    def get_main_offset(index) -> str:
        main_offsets = g_main_offsets
        return main_offsets[index]



