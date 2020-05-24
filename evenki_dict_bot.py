#!/usr/bin/python
# -*- coding: utf-8 -*
import pickle
import random

import telebot
__author__ = "gisly"

bot = telebot.TeleBot('1082882518:AAHB7pDqCCPq7OCBHMtgT28eT-1huop_cXw')
evenki_dict = None
REASONS_NO_WORD = ['К сожалению, такого слова я не знаю.',
                   'Увы :( Попробуй что-нибудь еще.',
                   'Хм, в следующий раз попробую найти.',
                   'Впервые слышу такое слово. Что это?']

PREFIXES_FOUND = ['Вот какие переводы нашлись:', 'Да, что-то есть такое :)',
                  'Я справился! ', 'Удалось найти:']

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Дорово!')


@bot.message_handler(content_types=['text'])
def send_text(message):
    initialize_dict()
    evenki_words = evenki_dict.get(message.text.strip())
    if not evenki_words:
        evenki_words = evenki_dict.get(message.text.strip().lower())
    if not evenki_words:
        bot.send_message(message.chat.id, get_random_reason())
    else:
        bot.send_message(message.chat.id,  get_random_prefix() +' *' + ', '.join(sorted(evenki_words)) + '*',
                         parse_mode='Markdown')


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

initialize_dict()
bot.polling()
