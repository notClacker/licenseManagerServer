#

def generate_license_key():


def get_license_keys(count: int) -> list:
    license_keys = []
    for i in range(count):
        key = generate_license_key()
        license_keys.append(key)
    return license_keys


def insert_key_and_days_in_db(key: str, days: int):
    # insert into user_db 
    # in column license_key the key
    # and in validity_days the days
    pass


def insert_keys_pair_in_db(pairs: dict):
    pass
    