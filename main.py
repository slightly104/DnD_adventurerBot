import telebot
import sqlite3
import config
import random
from telebot import types
from database import Database


db = Database("adventurers.db")
bot = telebot.TeleBot(config.TOKEN)


answers_for_dices = ["А пожалуйста!", "Да на здоровье!", "Получай!", \
"Что ещё хочешь?", "Может этого хватит?", "Сколько тебе ещё надо?", \
"А вот в наше время людям хватало одного кубика d6", "Серьёзно?", "Астанавись!"]



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('Персонаж')
    item2 = types.KeyboardButton('Оружие и шмотки')
    item3 = types.KeyboardButton('Кубики')
    item4 = types.KeyboardButton('Заметки')
    item5 = types.KeyboardButton('Создать персонажа')
    item6 = types.KeyboardButton('Удалить персонажа')
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nПогнали?', reply_markup=markup)
    


# Заполнение характеристик персонажа
def create_name(message):
    try:    
        db.input_character_data(message, 'Name')
        msg = bot.send_message(message.chat.id, 'Класс:')
        bot.register_next_step_handler(msg, create_class)
    except Exception as e:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_name)

def create_class(message):
    try:
        db.input_character_data(message, 'Class')
        msg = bot.send_message(message.chat.id, 'Раса:')
        bot.register_next_step_handler(msg, create_race)
    except Exception as e:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_class)

def create_race(message):
    try:    
        db.input_character_data(message, 'Race')
        msg = bot.send_message(message.chat.id, 'Сила:')
        bot.register_next_step_handler(msg, create_strength)      
    except Exception as e:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_race)

def create_strength(message):
    if message.text.isdigit() == True and int(message.text) <= 20:
        db.input_character_data(message, 'Strength')
        db.create_modifier(message, 'Strength')
        msg = bot.send_message(message.chat.id, 'Ловкость:')
        bot.register_next_step_handler(msg, create_dexterity)
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_strength)

def create_dexterity(message):
    if message.text.isdigit() == True and int(message.text) <= 20:
        db.input_character_data(message, 'Dexterity')
        db.create_modifier(message, 'Dexterity')
        msg = bot.send_message(message.chat.id, 'Телосложение:')
        bot.register_next_step_handler(msg, create_constitution)      
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_dexterity)

def create_constitution(message):
    if message.text.isdigit() == True and int(message.text) <= 20:
        db.input_character_data(message, 'Constitution')
        db.create_modifier(message, 'Constitution')
        msg = bot.send_message(message.chat.id, 'Интеллект:')
        bot.register_next_step_handler(msg, create_intelligence)      
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_constitution)

def create_intelligence(message):
    if message.text.isdigit() == True and int(message.text) <= 20:
        db.input_character_data(message, 'Intelligence')
        db.create_modifier(message, 'Intelligence')
        msg = bot.send_message(message.chat.id, 'Мудрость:')
        bot.register_next_step_handler(msg, create_wisdom)      
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_intelligence)

def create_wisdom(message):
    if message.text.isdigit() == True and int(message.text) <= 20:
        int(message.text)
        db.input_character_data(message, 'Wisdom')
        db.create_modifier(message, 'Wisdom')
        msg = bot.send_message(message.chat.id, 'Харизма:')
        bot.register_next_step_handler(msg, create_charisma)      
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_wisdom)

def create_charisma(message):
    if message.text.isdigit() == True and int(message.text) <= 20:
        int(message.text)
        db.input_character_data(message, 'Charisma')
        db.create_modifier(message, 'Charisma')
        msg = bot.send_message(message.chat.id, 'Уровень:')
        bot.register_next_step_handler(msg, create_level)      
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_charisma)

def create_level(message):
    if message.text.isdigit() == True and int(message.text) <= 20:
        int(message.text)
        db.input_character_data(message, 'Level')
        db.create_proficiency_bonus(message)
        msg = bot.send_message(message.chat.id, 'КД:')
        bot.register_next_step_handler(msg, create_armor_class)      
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_level)

def create_armor_class(message):
    if message.text.isdigit() == True:
        int(message.text)
        db.input_character_data(message, 'Armor_class')
        msg = bot.send_message(message.chat.id, 'Максимум хитов:')
        bot.register_next_step_handler(msg, create_HP_max)
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_armor_class)

def create_HP_max(message):
    if message.text.isdigit() == True:
        int(message.text)
        db.input_character_data(message, 'HP_maximum')
        msg = bot.send_message(message.chat.id, 'Кость хитов:')
        bot.register_next_step_handler(msg, create_hit_dice)
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_HP_max)

def create_hit_dice(message):
    try:
        db.input_character_data(message, 'Hit_dice')
        bot.send_message(message.chat.id, 'Поздравляю, персонаж добавлен!')
    except Exception as e:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Отменить и удалить перса", callback_data='delete_character')
        markup.add(item1)
        msg = bot.reply_to(message, 'Ты втираешь мне какую-то дичь! Введи нормально', reply_markup=markup)
        bot.register_next_step_handler(msg, create_hit_dice)


def create_feature_name(message):
    feature_name = message.text
    msg = bot.send_message(message.chat.id, f'Описание умения:')
    bot.register_next_step_handler(msg, create_feature_description, feature_name)

def create_feature_description(message, feature_name):
    db.create_feature(message, feature_name)
    bot.send_message(message.chat.id, 'Умение добавлено!')

def delete_feature_number(message):
    db.delete_feature(message)
    bot.send_message(message.chat.id, 'Умение потёрто')


# CallBack запросы
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            # Удаляем перса
            if call.data == 'delete_character':
                db.delete_character(call.message.chat.id)
                bot.clear_step_handler(call.message)
                bot.send_message(call.message.chat.id, 'Был пацан, и нет пацана...')    
                # Приколдэс после удаления
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                    text="ГДЕ ЛЁХА???")

            # Повторный бросок кубика
            if call.data in ('d4', 'd6', 'd8', 'd10', 'd12', 'd20'):
                if call.data == 'd4':
                    bot.send_message(call.message.chat.id, f'd4: {str(random.randint(1,4))}')
                elif call.data == 'd6':
                    bot.send_message(call.message.chat.id, f'd6: {str(random.randint(1,6))}')
                elif call.data == 'd8':
                    bot.send_message(call.message.chat.id, f'd8: {str(random.randint(1,8))}')
                elif call.data == 'd10':
                    bot.send_message(call.message.chat.id, f'd10: {str(random.randint(0,9))}')
                elif call.data == 'd12':
                    bot.send_message(call.message.chat.id, f'd12: {str(random.randint(1,12))}')
                elif call.data == 'd20':
                    bot.send_message(call.message.chat.id, f'd20: {str(random.randint(1,20))}')
                # Приколдэс на переброс кубика
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                    text=random.choice(answers_for_dices))


            # Добавляем умение
            if call.data == "add_feature":
                msg = bot.send_message(call.message.chat.id, 'Название умения:')
                bot.register_next_step_handler(msg, create_feature_name)


            # Удаляем умение
            if call.data == "delete_feature":
                msg = bot.send_message(call.message.chat.id, 'Номер умения которое удаляем (около названия)')
                bot.register_next_step_handler(msg, delete_feature_number)

    except Exception as e:
        print(repr(e))


# Текстовые запросы
@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':

        # Добавление персонажа
        if message.text == 'Создать персонажа':
            
            if db.if_character_exist(message.chat.id) == "exist":
                bot.send_message(message.chat.id, 'Сначала загуби предыдущего')
            else:
                db.create_character(message.chat.id)
                msg = bot.send_message(message.chat.id, f'Имя:')
                bot.register_next_step_handler(msg, create_name)
                
        # # Изменение вручную
        # if message.text == 'aaa':
        #     db.update_character(message)
        #     bot.send_message(message.chat.id, 'Поменяно')

        # Удаление персонажа
        elif message.text == 'Удалить персонажа':
            # Аннигилирование перса
            if db.if_character_exist(message.chat.id) == "does_not_exist":
                bot.send_message(message.chat.id, 'В этом мире у тебя никого нет. Ты полностью один. Смирись или создай себе перса через /start')
            else:
                # Уточнение запроса
                markup = types.InlineKeyboardMarkup()
                item1 = types.InlineKeyboardButton("Загубить своего перса", callback_data='delete_character')
                markup.add(item1)
                bot.send_message(message.chat.id, 'Может не стоит?', reply_markup=markup)

        # Основное меню
        elif message.text == 'На главную':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton('Персонаж')
            item2 = types.KeyboardButton('Оружие и шмотки')
            item3 = types.KeyboardButton('Кубики')
            item4 = types.KeyboardButton('Заметки')
            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, 'Главное тебю', reply_markup=markup)

        # Кубики
        elif message.text == 'Кубики':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            d4 = types.KeyboardButton('d4')
            d6 = types.KeyboardButton('d6')
            d8 = types.KeyboardButton('d8')
            d10 = types.KeyboardButton('d10')
            d12 = types.KeyboardButton('d12')
            d20 = types.KeyboardButton('d20')
            back = types.KeyboardButton('На главную')
            markup.add(d4, d6, d8, d10, d12, d20, back)
            bot.send_message(message.chat.id, 'Какой кубик кидаешь?', reply_markup=markup)
            
        elif message.text == 'd4':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Ещё один?", callback_data='d4')
            markup.add(item1)
            bot.send_message(message.chat.id, f'd4: {str(random.randint(1,4))}', reply_markup=markup)

        elif message.text == 'd6':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Ещё один?", callback_data='d6')
            markup.add(item1)
            bot.send_message(message.chat.id, f'd6: {str(random.randint(1,6))}', reply_markup=markup)

        elif message.text == 'd8':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Ещё один?", callback_data='d8')
            markup.add(item1)
            bot.send_message(message.chat.id, f'd8: {str(random.randint(1,8))}', reply_markup=markup)

        elif message.text == 'd10':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Ещё один?", callback_data='d10')
            markup.add(item1)
            bot.send_message(message.chat.id, f'd10: {str(random.randint(0,9))}', reply_markup=markup)

        elif message.text == 'd12':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Ещё один?", callback_data='d12')
            markup.add(item1)
            bot.send_message(message.chat.id, f'd12: {str(random.randint(1,12))}', reply_markup=markup)

        elif message.text == 'd20':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Ещё один?", callback_data='d20')
            markup.add(item1)
            bot.send_message(message.chat.id, f'd20: {str(random.randint(1,20))}', reply_markup=markup)
        
        # Обзор персонажа
        elif message.text == 'Персонаж':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton('Навыки')
            item2 = types.KeyboardButton('Характеристики')
            item3 = types.KeyboardButton('Умения')
            item4 = types.KeyboardButton('Редактировать')
            back = types.KeyboardButton('На главную')
            markup.add(item1, item2, item3, item4, back)
            bot.send_message(message.chat.id, 'Персонаж', reply_markup=markup)
        
        # Обзор оружия и шмоток
        elif message.text == 'Оружие и шмотки':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton('Оружие')
            item2 = types.KeyboardButton('Шмотки')
            item3 = types.KeyboardButton('Редактировать')
            back = types.KeyboardButton('На главную')
            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, 'Оружие и шмотки', reply_markup=markup)
        
        # Обзор заметок
        elif message.text == 'Заметки':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton('Добавить')
            item2 = types.KeyboardButton('Редактировать')
            item3 = types.KeyboardButton('Удалить')
            back = types.KeyboardButton('На главную')
            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, 'Заметки', reply_markup=markup)

        # Вывод характеристик
        elif message.text == 'Характеристики':
            if db.if_character_exist(message.chat.id) == "does_not_exist":
                bot.send_message(message.chat.id, 'В этом мире у тебя никого нет. Ты полностью один. Смирись или создай себе перса через /start')
            else:
                bot.send_message(message.chat.id, db.request_for_characteristics(message.chat.id))

        # Вывод навыков
        elif message.text == 'Навыки':
            if db.if_character_exist(message.chat.id) == "does_not_exist":
                bot.send_message(message.chat.id, 'В этом мире у тебя никого нет. Ты полностью один. Смирись или создай себе перса через /start')
            else:
                bot.send_message(message.chat.id, db.request_for_skills(message.chat.id))
            

        # Умения 
        elif message.text == 'Умения':
            if db.if_character_exist(message.chat.id) == "does_not_exist":
                bot.send_message(message.chat.id, 'В этом мире у тебя никого нет. Ты полностью один. Смирись или создай себе перса через /start')
            else:
                markup = types.InlineKeyboardMarkup()
                item1 = types.InlineKeyboardButton("Добавить", callback_data="add_feature")
                item2 = types.InlineKeyboardButton("Удалить", callback_data="delete_feature")
                markup.add(item1, item2)
                bot.send_message(message.chat.id, db.features_traits(message.chat.id), reply_markup=markup)
            

        # В разработке
        else:
            bot.send_message(message.chat.id, 'Много хочешь (скоро получишь)')

       
        


bot.polling(none_stop=True)