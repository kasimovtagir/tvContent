import keys

import os
import telebot
from telebot import types

import action

bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"], parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

ADMINS = ["815850294","257968418"]

@bot.message_handler(func=lambda message: str(message.chat.id) not in str( ADMINS))
def some(message):
   #bot.send_message(message.chat.id, "Sorry")
   bot.send_message(message.chat.id, "Don't access this telegram bot.")


@bot.message_handler(content_types=['document'])
def documents(message):
    action.Upload_files(bot,message)         

@bot.message_handler(commands=['start'])
def button(message):
    action.Start(bot, message)
    #bot.send_message(message.chat.id, text='Привет\nВот список доступных телевизоров.')

@bot.message_handler(commands=['update'])
def button(message):
    #srv.send_message_to_tv() #работает, раскомментировать это 
    bot.send_message(message.chat.id, text='Слайды обновлены.', reply_markup=action.button_start())

@bot.callback_query_handler(func=lambda call: True)
def Actions (call):
    if call.data == "tv1":
        action.Show_func_tv(call,bot,"tv1")
        
    if call.data == "tv2":
        bot.send_message(call.message.chat.id, f"В разработке!")
        action.Start(bot, call.message)
		#action.Show_func_tv(call,bot,"tv2")		

    if call.data == "upload_slides":
        bot.send_message(call.message.chat.id, f"Отправь файл который нужно залить на телевизоры")

    if call.data == "show_slides":
        action.show_all_slides(call, bot)

    for root, dirs, files in os.walk("/mnt/Content/tv1/"):
        for f in files:
            if call.data == f"delete_{f}":
                action.delete_slides(bot,call,f"{f}")

    if call.data == "delete_all_slides":
        for root, dirs, files in os.walk("/mnt/Content/tv1/"):
            for f in files:
                #print(f)
                os.remove(f"/mnt/Content/tv1/{f}")
        bot.send_message(call.message.chat.id, "Удалены все слайды.")
        #os.remove("/home/adminu/tvContent/mount/Content/tv1/")



bot.infinity_polling()