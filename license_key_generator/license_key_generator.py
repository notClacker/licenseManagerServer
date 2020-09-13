import cfg
import sqlite3
import random


def generate_license_key():
    symbol = cfg.g_separate_symbol
    width = 5
    elems = []
    for i in range(width):
        elem = ""
        for j in range(width):
            elem += random.choice(cfg.g_resolved_symbols)
        elems.append(elem)
    key = symbol.join(elems)
    return key


def get_license_keys(count: int) -> list:
    license_keys = []
    for i in range(count):
        key = generate_license_key()
        license_keys.append(key)
    return license_keys


def insert_key_and_days_in_db(key: str, days: int):
    conn = sqlite3.connect(cfg.g_path_to_db)
    cursor = conn.cursor()

    try:
        values = "%d, '%s'" % (days, key)
        print(values)
        request = """insert into users_licenses
                    (validity_days, license_key)
                            values (%s);""" % values
        cursor.execute(request)
        print(values)
    except sqlite3.DatabaseError as err:
        print("THIS KEY IN DB")
    except Exception as err:
        print(err)
    else:
        conn.commit()
    conn.close()


def do_job():
    keys = get_license_keys(cfg.g_count_of_new_license_keys)
    validity_days = cfg.g_validity_days
    for key in keys:
        insert_key_and_days_in_db(key, validity_days)
    input("Press any key to exit...")
