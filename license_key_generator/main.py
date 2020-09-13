#!/usr/bin/env python3

import license_key_generator
import cfg

if __name__ == "__main__":
    print("Welcome to the license key generator")

    count_of_keys = cfg.g_count_of_new_license_keys 
    print("Enter a COUNT of license keys\nBy default %d: " % (count_of_keys), end="")
    str_count = input()
    if len(str_count) > 0: 
        count_of_keys = int(str_count)
    

    validity_days = cfg.g_validity_days  
    print("Enter a VALIDITY_DAYS of license keys\nBy default %d: " % (validity_days), end="")
    str_days = input()
    if len(str_count) > 0: 
        validity_days = int(str_count)

    license_key_generator.do_job(count_of_keys, validity_days)
    print("\nGenerate [", count_of_keys ,"] keys with validity days = ", validity_days)
