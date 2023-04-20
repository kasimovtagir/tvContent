import os
import telebot
from telebot import types
import random

name_tvs = ""
delete_slides = ""

def button_start():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    button = types.KeyboardButton(text='/start')
    markup.add(button) 
    return markup


def Start(bot:telebot.TeleBot, message):
    bot.send_message(message.chat.id, text=(f'Привет, {str(message.from_user.first_name)}\nВот список доступных телевизоров.'), reply_markup= button_start())
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    tv1 = types.InlineKeyboardButton(text='TV1', callback_data='tv1')
    tv2 = types.InlineKeyboardButton(text='TV2', callback_data='tv2')
    keyboard.add(tv1,tv2)
    bot.send_message(message.chat.id, text='Выбирай:', reply_markup=keyboard)


def Show_func_tv (call, bot,name_tv):
    global name_tvs
    name_tvs = name_tv
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    download_slides = types.InlineKeyboardButton(text='Загрузить', callback_data='upload_slides')
    show_slides = types.InlineKeyboardButton(text='Показать', callback_data='show_slides')
    delete_all_slides = types.InlineKeyboardButton(text='Удалить все слайды', callback_data='delete_all_slides')
    keyboard.add(download_slides,show_slides,delete_all_slides)
    bot.send_message(call.from_user.id, text='Если хочешь загрузить новые слайды, нажми на Загрузить'
                                                'Если хочешь посмотреть какие слайды уже загружены, нажми на Показать'
                                                'Удалить все слайды - можно не объяснять что сделает :-)'
                                                'Длина имени слайда не должна превышать 10 символов!', reply_markup=keyboard)

def createFolder ():
    contentFolder = "/mnt/Content"
    if(os.path.isdir(contentFolder)):
        print("folder exist")
    else: os.mkdir(contentFolder)


def Upload_files(bot:telebot.TeleBot,message:telebot.types.Message):
    try:
        #createFolder()
        try:
            save_dir = f"/mnt/Content/{name_tvs}"
            # save_dir = message.caption
        except:
            save_dir = f"/mnt/Content/{name_tvs}"
            # save_dir = os.getcwd()
            s = "[!] you aren't entered directory, saving to {}".format(save_dir)
            bot.send_message(message.chat.id, str(s))
        file_name = message.document.file_name

        file_id = message.document.file_name
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        print(f"Пользователь {str(message.from_user.first_name)} загрузил файл: {str(file_name)}" )

        with open(save_dir + "/" + file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
        #bot.reply_to(message, f"Файл {file_name} загружен на ТВ", replay_markup=send_to_tv())
        bot.send_message(message.chat.id,f"Файл загружен на ТВ", reply_markup=button_start())
        os.rename(save_dir + "/" + file_name, save_dir + "/" + renameFile()+".jpg")
        # os.remove(tagir)
    except Exception as ex:
        bot.send_message(message.chat.id, f"{ex}Неизвестная ошибка\nНажми на кнопку START", reply_markup= button_start())

def renameFile():
    return ''.join(random.choice("qwertyyuuiiop[lkjhgfdsmnbvcxzme") for _ in range(6))

def show_all_slides(call, bot):
    for root, dirs, files in os.walk(f"/mnt/Content/{name_tvs}"):
        for f in files:
            filename, file_extension = os.path.splitext(f)
            if file_extension == ".jpg":
                #if f.find(choose_printer_for_scan) >= 0:
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                slides = types.InlineKeyboardButton(text=f'удалить {f}', callback_data=f'delete_{f}')
                keyboard.add(slides)
                bot.send_document(call.from_user.id, open(root + "//" + f, 'rb'), reply_markup=keyboard)
            else: continue

def delete_slides(bot,call,delete_slide):
    os.remove(f"/mnt/Content/{name_tvs}/{delete_slide}")
    bot.send_message(call.from_user.id,f"Файл {delete_slide} удален. Нажми start.", reply_markup=button_start())


