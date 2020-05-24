#!/usr/bin/python
# -*- coding: utf-8 -*
import telebot
__author__ = "gisly"

bot = telebot.TeleBot('1082882518:AAHB7pDqCCPq7OCBHMtgT28eT-1huop_cXw')
evenki_dict = {'олень': ['орон', 'багдака'],
               }

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Дорово!')


@bot.message_handler(content_types=['text'])
def send_text(message):
    evenki_words = evenki_dict.get(message.text)
    if not evenki_words:
        bot.send_message(message.chat.id, 'Такого слова я не знаю. Попробуй поискать что-нибудь другое.')
    else:
        bot.send_message(message.chat.id, 'Вот какие переводы нашлись: *' + ', '.join(evenki_words) + '*',
                         parse_mode='Markdown')

bot.polling()
