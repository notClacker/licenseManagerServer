import generator_cfg
import sqlite3
import random
import time


def generate_license_key():
    symbol = generator_cfg.g_separate_symbol
    width = 5
    elems = []
    for i in range(width):
        elem = ""
        for j in range(width):
            elem += random.choice(generator_cfg.g_resolved_symbols)
        elems.append(elem)
    key = symbol.join(elems)
    return key


def get_license_keys(count: int) -> list:
    license_keys = []
    for i in range(count):
        key = generate_license_key()
        license_keys.append(key)
    return license_keys


def insert_key_and_days_in_db(key: str, days: int, subscribe_type: str) -> None:
    for attempt in range(generator_cfg.g_max_attempts):
        try:
            conn = sqlite3.connect(generator_cfg.g_path_to_db)
            cursor = conn.cursor()

            try:
                values = "%d, '%s', '%s'" % (days, key, subscribe_type)
                print(values)
                request = """insert into users_licenses
                            (validity_days, license_key, subscribe_type)
                                    values (%s);""" % values
                cursor.execute(request)
            except sqlite3.DatabaseError as err:
                print("THIS KEY IN DB?")
                print(err)
            except Exception as err:
                print(err)
            else:
                conn.commit()
            conn.close()
            break
        except Exception as err:
            print(err)
            time.sleep(generator_cfg.g_error_time_to_sleep)

def do_job(count_of_keys: int, validity_days: int, subscribe_type: str) -> None:
    keys = get_license_keys(count_of_keys)
    for key in keys:
        insert_key_and_days_in_db(key, validity_days, subscribe_type)
