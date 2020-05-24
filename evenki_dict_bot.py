#!/usr/bin/python
# -*- coding: utf-8 -*
import sqlite3
import random

import telebot
__author__ = "gisly"

bot = telebot.TeleBot('1082882518:AAHB7pDqCCPq7OCBHMtgT28eT-1huop_cXw')
evenki_dict = None
REASONS_NO_WORD = ['К сожалению, такого слова я не знаю.',
                   'Увы \U00002639 Попробуй что-нибудь еще.',
                   'Хм, в следующий раз попробую найти.',
                   'Впервые слышу такое слово. Что это?']

PREFIXES_FOUND = ['Вот какие переводы нашлись:', 'Да, что-то есть такое \U0001F609',
                  'Я справился! ', 'Удалось найти \U0001F60A:', 'Есть такое слово! ']

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Дорово!')





@bot.message_handler(content_types=['text'])
def send_text(message):
    #initialize_dict()
    conn = None
    try:
        conn = sqlite3.connect('dictionary.db')
        evenki_words = get_word(conn, message.text.strip())
        if not evenki_words:
            evenki_words = get_word(conn, message.text.strip().lower())
        if not evenki_words:
            bot.send_message(message.chat.id, get_random_reason())
        else:
            bot.send_message(message.chat.id,  get_random_prefix() +' *' + ', '.join(sorted(evenki_words)) + '*',
                             parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, 'Что-то пошло не так :(')
    finally:
        if conn:
            conn.close()

def get_word(conn, word):
    qlite_select_query = 'SELECT evenki from words where rus = ?'
    cursor = conn.cursor()
    cursor.execute(qlite_select_query, (word,))
    records = cursor.fetchall()
    result = []
    for record in records:
        result.append(record[0])
    return result


def initialize_dict():
    global evenki_dict
    if evenki_dict is None:
        with open('vasilevich.pickle', 'rb') as handle:
            evenki_dict = pickle.load(handle)
    print('dict initialized')

def get_random_reason():
    random_num = random.randint(0,  len(REASONS_NO_WORD) - 1)
    return REASONS_NO_WORD[random_num]

def get_random_prefix():
    random_num = random.randint(0,  len(PREFIXES_FOUND) - 1)
    return PREFIXES_FOUND[random_num]

#initialize_dict()
bot.polling()
