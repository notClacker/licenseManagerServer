#!/usr/bin/env python3

import license_key_generator
import generator_cfg

import os

def main_funct():
    current_dir = os.getcwd()
    current_folder = current_dir.split('/')[-1]
    print(current_folder)
    os.chdir(current_dir + generator_cfg.g_path_from_script_to_main)
    print(os.getcwd)

    count_of_keys = generator_cfg.g_count_of_new_license_keys 
    print("Enter a COUNT of license keys\nBy default %d: " % (count_of_keys), end="")
    str_count = input()
    if len(str_count) > 0: 
        count_of_keys = int(str_count)
    

    validity_days = generator_cfg.g_validity_days  
    print("Enter a VALIDITY_DAYS of license keys\nBy default %d: " % (validity_days), end="")
    str_days = input()
    if len(str_days) > 0: 
        validity_days = int(str_count)

    subscribe_type = ""
    while (len(subscribe_type) <= 1):
        subscribe_type = input("Enter the subscribe type: ")

    license_key_generator.do_job(count_of_keys, validity_days, subscribe_type)
    print("\nGenerate [", count_of_keys ,"] keys with validity days = ", validity_days)
    

if __name__ == "__main__":
    main_funct()
    