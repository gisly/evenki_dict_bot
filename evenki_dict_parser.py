#!/usr/bin/python
# -*- coding: utf-8 -*
__author__ = "gisly"
import sqlite3

def import_dictionary_to_sqlite(filename_dsl):
    import sqlite3
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute('drop table words')
    c.execute('create table words (rus text, evenki text)')
    dict_parsed = parse_dsl(filename_dsl)
    for item, value_list  in dict_parsed.items():
        for value in value_list:
            c.execute('insert into words (rus, evenki) values (?, ?)', (item, value))
    conn.commit()
    conn.close()
    print('ok')

def parse_dsl(filename_dsl):
    dict_parsed = dict()
    current_word = None
    with open(filename_dsl, 'r', encoding='utf-8') as fin:
        for line in fin:
            line = line.strip()
            if line.startswith('[m'):
                translations = line.split(']')[-1].split(';')
                if current_word:
                    for translation in translations:
                        translation_parts = translation.split(' ')
                        for translation_part in translation_parts:
                            translation_part = normalize_translation(translation_part)
                            if translation_part in dict_parsed:
                                dict_parsed[translation_part].append(current_word)
                            else:
                                dict_parsed[translation_part] = [current_word]
            elif line.startswith('[p'):
                continue
            else:
                current_word = line
    return dict_parsed

def normalize_translation(translation):
    return translation.strip('.').strip()



import_dictionary_to_sqlite('resources/vasilevich.dsl')





