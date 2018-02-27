#!/usr/bin/env python3

import telebot
from telebot import types
from concert_spb import *

token=''
bot=telebot.TeleBot(token)

keyboard = types.InlineKeyboardMarkup()
keyboard.row(types.InlineKeyboardButton(text='A2',callback_data='A2'))
keyboard.row(types.InlineKeyboardButton(text='Космонавт',callback_data='kosmo'))
keyboard.row(types.InlineKeyboardButton(text='Аврора',callback_data='aurora'))
keyboard.row(types.InlineKeyboardButton(text='Зал ожидания',callback_data='zal'))


@bot.message_handler(commands=['start'])
def command_start(m):
    text='\tПриветствую тебя, мой концертный задрот!\n' \
         ' Я покажу тебе афишу ближайших концертов СПБ\nВыбери клуб:'
    bot.send_message(m.chat.id,text=text,reply_markup=keyboard)

def send_billboard(club,m):
    billboard = read_of_file(club+'.txt')
    text = ''
    for artist in billboard:
        text += str(artist) + '\n'
    bot.send_message(m.chat.id, text,reply_markup=keyboard)

@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    if c.data == 'aurora':
         bot.send_message(c.message.chat.id,text='Афиша клуба АВРОРА:\n')
         send_billboard(c.data,c.message)
    elif c.data == 'kosmo':
         bot.send_message(c.message.chat.id, text='Афиша клуба Космонавт:\n')
         send_billboard(c.data, c.message)
    elif c.data == 'A2':
        pass
    else:
        pass
def main():
    print('Парсинг афиш')
    write_in_file('aurora.txt',pars_aurora())
    write_in_file('kosmo.txt', pars_kosmonavt())
    print("concert-bot запущен")
    # Начинаем
    bot.polling(none_stop=True)

main()