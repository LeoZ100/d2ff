#!/usr/bin/env python3

import argparse
import csv
import json


def transform_to_importable_firefox_file(input_file, output_file):
    with open(input_file) as dashlane_file, open(output_file, 'w+') as firefox_file:
        password_section = get_password_section(dashlane_file)
        firefox_csv = initialize_firefox_csv(firefox_file)

        for password_entry in password_section:
            if password_entry['password'] is not '':
                url = f"https://www.{password_entry['domain']}"
                login = password_entry['login'] if password_entry['login'] is not '' else password_entry['email']
                password = password_entry['password']
                firefox_csv.writerow([url, login, password])


def initialize_firefox_csv(firefox_file):
    firefox_csv = csv.writer(firefox_file, quotechar=',', quoting=csv.QUOTE_MINIMAL)
    firefox_csv.writerow(['url', 'username', 'password'])
    return firefox_csv


def get_password_section(dashlane_file):
    try:
        return json.load(dashlane_file)['AUTHENTIFIANT']
    except:
        print(f'ERROR: {dashlane_file.name} is not a valid Dashlane JSON Export file...')
        exit(1)


def get_io_files():
    parser = get_parser()
    args = parser.parse_args()
    return args.input_file, args.output_file if args.output_file is not None else 'FirefoxImport.csv'


def get_parser():
    parser = argparse.ArgumentParser(description='Converts a Dashlane Password Manager JSON Export '
                                                 'into a compatible format for importing passwords into Firefox.')
    parser.add_argument('input_file',
                        help='The input "Dashlane JSON export" file to be processed')
    parser.add_argument('-o',
                        '--output-file',
                        help='The output Firefox CSV import file to be produced')
    return parser


def main():
    input_file, output_file = get_io_files()
    transform_to_importable_firefox_file(input_file, output_file)


if __name__ == '__main__':
    main()
