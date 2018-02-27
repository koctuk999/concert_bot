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
    global billboard
    billboard=[]
    text='\tПриветствую тебя, мой концертный задрот!\n' \
         ' Я покажу тебе афишу ближайших концертов СПБ\nВыбери клуб:'
    bot.send_message(m.chat.id,text=text,reply_markup=keyboard)

def pages_keyboard(start, stop,billboard):
    pag_key = types.InlineKeyboardMarkup()
    btns = []
    if start > 0: btns.append(types.InlineKeyboardButton(
        text='⬅', callback_data='to_{}'.format(start - 4)))
    if stop < len(billboard): btns.append(types.InlineKeyboardButton(
        text='➡', callback_data='to_{}'.format(stop)))
    pag_key.add(*btns)
    return pag_key

def send_billboard(club,m):
    global billboard
    billboard = read_of_file(club+'.txt')
    text = ''
    for artist in billboard[:4]:
        text += str(artist) + '\n'
    bot.edit_message_text(chat_id=m.chat.id,
                          message_id=m.message_id,
                          text='АФИША '+club+'\n'+text,
                          reply_markup=pages_keyboard(0,4,billboard))

@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    if c.data == 'aurora':
         send_billboard(c.data,c.message)
    elif c.data == 'kosmo':
         send_billboard(c.data, c.message)
    elif c.data == 'A2':
        pass
    elif c.data =='zal':
        pass
    else: #для пролистывания афишы
        text=''
        for artist in billboard[int(c.data[3:]):int(c.data[3:])+4]:
            text+=str(artist)+'\n'
        bot.edit_message_text(chat_id=c.message.chat.id,
                              message_id=c.message.message_id,
                              text=text,
                              reply_markup=pages_keyboard(int(c.data[3:]),int(c.data[3:])+4,billboard))


def main():
    print('Парсинг афиш')
    write_in_file('aurora.txt',pars_aurora())
    write_in_file('kosmo.txt', pars_kosmonavt())
    print('афиши добавлены в базу')
    print("concert-bot запущен")
    bot.polling(none_stop=True)

main()