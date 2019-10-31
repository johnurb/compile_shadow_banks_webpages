import os
from fuzzywuzzy import fuzz
import csv
import json
import re
import multiprocessing as mp
from time import sleep

class Bank_Site:
    def __init__(self, name, master_string, num_pages):
        self.bank_name = name
        self.master_text = master_string
        self.number_pages = num_pages
        self.site_dict = {
            'name': self.bank_name,
            'master_string': self.master_text,
            'num_pages': self.number_pages
        }

        self.output_info()

    def output_info(self):
        json_dir = 'bank_jsons'
        file_name = self.bank_name.replace(' ', '_') + '.json'
        outfile_path = os.path.join(json_dir, file_name)
        with open(outfile_path, 'w') as fout:
            json.dump(self.site_dict, fout)


def clean_text(text_page):
    with open(text_page, 'r') as fin:
        page_lines = fin.readlines()

        if len(page_lines) < 5:
            return ''

        else:
            cleaned_lines = []
            for line in page_lines:
                cleaned_lines.append(re.sub('[^0-9a-z.\s\n]', '',
                line.lower().lstrip().replace('!', '.').replace('?', '.').replace('\\n', '.').replace('...', '.').replace('..', '.')).lstrip())

            return (''.join(cleaned_lines))


def remove_boiler(string_list):
    print('Removing Boiler')
    
    all_lines = []
    for string in string_list:
        string_lines = string.split('\n')
        for line in string_lines:
            all_lines.append(line)

    all_lines = list(set(all_lines))
    clean_text = ''
    for line in all_lines:
        stripped_line = line.strip()
        if stripped_line == ' ' or stripped_line == '':
            pass
        else:
            if stripped_line.endswith('.'):
                clean_text += stripped_line + ' '
            else:
                clean_text += stripped_line + '. '

    return clean_text


def process_directory_pages(directory):
        bank_name = directory.replace('directory/', '').replace('_', ' ')
        bank_master_string_list = []
        site_pages = 0
        bank_saved_pages = os.listdir(directory)
        for page in bank_saved_pages:
            if page == '.DS_Store':
                pass
            else:
                bank_master_string_list.append(clean_text(os.path.join(directory, page)))

        for item in bank_master_string_list:
            if item == '':
                pass
            else:
                site_pages += 1

        bank_master_string = remove_boiler(bank_master_string_list)

        bank_obj = Bank_Site(bank_name, bank_master_string, site_pages)
        #bank_obj.ouput_info()


def main():
    main_directory = 'directory'
    directory_folders = os.listdir(main_directory)
    bank_folders = []
    for directory in directory_folders:
        if directory == '.DS_Store':
            pass
        else:
            bank_path = os.path.join(main_directory, directory)
            bank_folders.append(bank_path)

    #process_directory_pages(bank_folders[0])

    pool = mp.Pool(mp.cpu_count())
    result = pool.map(process_directory_pages, bank_folders)


main()
