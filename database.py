from re import I
import sqlite3
import math


# Cоздание таблицы если не существует
class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS character (
            id text,
            Name text,
            Class text,
            Race text,
            Level text,

            Hit_dice text,
            HP_maximum text,
            Armor_class text,

            Initiative text,
            Proficiency_bonus text,

            Strength text,
            Dexterity text,
            Constitution text,
            Intelligence text,
            Wisdom text,
            Charisma text,

            Strength_modifier text,
            Dexterity_modifier text,
            Constitution_modifier text,
            Intelligence_modifier text,
            Wisdom_modifier text,
            Charisma_modifier text,

            Acrobatics text,
            Investigation text,
            Athletics text,
            Perception text,
            Survival text,
            Performance text,
            Intimidation text,
            History text,
            Sleight_of_hand text,
            Arcana text,
            Medicine text,
            Deception text,
            Nature text,
            Insight text,
            Religion text,
            Stealth text,
            Persuasion text,
            Animal_handling text,

            HP_current text
        )""")


    # Проверка существует ли персонаж
    def if_character_exist(self, chat_id):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM character WHERE id = {chat_id}")
            unic_chat_id = self.cursor.fetchone()
            if unic_chat_id is None:
                return "does_not_exist"
            else:
                return "exist"


    # Создание учетки
    def create_character(self, chat_id):
        with self.connection:
            # Заполняем табличку характеристик и навыков стартовыми значениями
            self.cursor.execute("INSERT INTO character VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f'{chat_id}', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'))
            
            # Создаём табличку умений и особенностей
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{chat_id}_features` (
                    Feature TEXT,
                    Description TEXT
                )""")
            # Заполняем табличку умений и особенностей стартовыми значениями
            self.cursor.execute(f"INSERT INTO `{chat_id}_features`(Feature, Description) VALUES(?, ?)", ('Это стоит заполнить', 'Или удалить'))

            # Создаём табличку оружия
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{chat_id}_weapons` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Weapon TEXT,
                    Description TEXT
                )""")
            # Заполняем табличку оружия стартовыми значениями
            self.cursor.execute(f"INSERT INTO `{chat_id}_weapons`(Weapon, Description) VALUES(?, ?)", ('4', '5'))

            # Создаём табличку шмоток
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{chat_id}_equipments` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Equipment TEXT,
                    Description TEXT
                )""")
            # Заполняем табличку шмоток стартовыми значениями
            self.cursor.execute(f"INSERT INTO `{chat_id}_equipments`(Equipment, Description) VALUES(?, ?)", ('6', '7'))


    # Ввод данных персонажа
    def input_character_data(self, msg, col):
        with self.connection:
            self.cursor.execute(f"UPDATE character SET {col} = '{msg.text}' WHERE id = {msg.chat.id}")

    
    # Создание нового умения
    def create_feature(self, msg, feature_name):
        with self.connection:
            self.cursor.execute(f"INSERT INTO `{msg.chat.id}_features`(Feature, Description) VALUES(?, ?)", (feature_name, f'{msg.text}'))

    # Удаление умения
    def delete_feature(self, msg):
        with self.connection:
            self.cursor.execute(f"DELETE FROM `{msg.chat.id}_features` WHERE rowid = '{msg.text}'")
            self.connection.commit()
    

    # Создание Бонуса мастерства
    def create_proficiency_bonus(self, msg):
        # Создаём бонус мастерства
        PB = str(math.ceil((int(msg.text))/4 + 1))
        # Заводим БМ в БД
        self.cursor.execute((f"UPDATE character SET `Proficiency_bonus` = ? WHERE `id` = ?"), (PB, msg.chat.id))


    # Создание модификатора и занесение его в БД 
    def create_modifier(self, msg, col):
        # Создаём модификатор
        modifier = str(math.floor((int(msg.text)-10)/2))
        # Заполняем навыки
        if col == 'Strength':
            self.cursor.execute((f"UPDATE character SET `Strength_modifier` = ?, `Athletics` = ? WHERE `id` = ?"), (modifier, modifier, msg.chat.id))
        elif col == 'Dexterity':
            self.cursor.execute((f"UPDATE character SET `Dexterity_modifier` = ?, `Acrobatics` = ?, `Sleight_of_hand` = ?, `Stealth` = ?, `Initiative` = ? WHERE `id` = ?"), (modifier, modifier, modifier, modifier, modifier, msg.chat.id))
        elif col == 'Constitution':
            self.cursor.execute((f"UPDATE character SET `Constitution_modifier` = ? WHERE `id` = ?"), (modifier, msg.chat.id))
        elif col == 'Intelligence':
            self.cursor.execute((f"UPDATE character SET `Intelligence_modifier` = ?, `Arcana` = ?, `History` = ?, `Investigation` = ?, `Nature` = ?, `Religion` = ? WHERE `id` = ?"), (modifier, modifier, modifier, modifier, modifier, modifier, msg.chat.id))
        elif col == 'Wisdom':
            self.cursor.execute((f"UPDATE character SET `Wisdom_modifier` = ?, `Animal_handling` = ?, `Insight` = ?, `Medicine` = ?, `Perception` = ?, `Survival` = ? WHERE `id` = ?"), (modifier, modifier, modifier, modifier, modifier, modifier, msg.chat.id))
        elif col == 'Charisma':
            self.cursor.execute((f"UPDATE character SET `Charisma_modifier` = ?, `Deception` = ?, `Intimidation` = ?, `Performance` = ?, `Persuasion` = ? WHERE `id` = ?"), (modifier, modifier, modifier, modifier, modifier, msg.chat.id))

           
    # # Изменение данных
    # def update_character(self, message):
    #     with self.connection:
    #         self.cursor.execute(f"UPDATE character SET Имя = '{message.text}' WHERE id = {message.chat.id}")


    # Удаление персонажа
    def delete_character(self, chat_id):
        with self.connection:
            return self.cursor.execute(f"DELETE FROM character WHERE id = {chat_id}")


    # Запрос характеристик
    def request_for_characteristics(self, chat_id):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM character WHERE id = {chat_id}")
            # Достаём значения характеристик (кортеж)
            characteristics = self.cursor.fetchall()[0][1:22]

            # Достаём модификаторы
            list_of_modifier = characteristics[15:21]
            # Приводим к готовым строкам
            list_of_modifier_cooked = list()
            for i in list_of_modifier:
                if int(i) >= 0:
                    list_of_modifier_cooked.append(f' (+{i})')
                else:
                    list_of_modifier_cooked.append(f' ({i})')

            characteristics_ru = ["Имя", "Класс", "Раса", "Уровень", "Кость хитов", "Максимум хитов", "КД",\
                 "Инициатива", "Бонус мастерства", "Сила", "Ловкость", "Телосложение", "Интеллект", "Мудрость", "Харизма"]

            # Соединяем столбцы с характеристиками
            characteristics_precooked1 = [(characteristics_ru[i] + ' - ' + characteristics[i]) for i in range(4)]
            characteristics_precooked2 = [(characteristics_ru[4:7][i] + ' - ' + characteristics[4:7][i]) for i in range(3)]
            characteristics_precooked3 = [(characteristics_ru[7:9][i] + ' - ' + characteristics[7:9][i]) for i in range(2)]
            characteristics_precooked4 = [(characteristics_ru[9:15][i] + ' - ' + characteristics[9:15][i] + list_of_modifier_cooked[i]) for i in range(6)]
            
            # Переводим в строку для return
            characteristics_text = '\n'.join(characteristics_precooked1 + list(' ') + characteristics_precooked2 + list(' ')\
                + characteristics_precooked3 + list(' ') + characteristics_precooked4)

            return characteristics_text


    # Запрос навыков
    def request_for_skills(self, chat_id):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM character WHERE id = {chat_id}")
            # Достаём значения навыков (кортеж)
            skills = self.cursor.fetchall()[0][22:40]

            # Приводим к готовым строкам
            skills_cooked = list()
            for i in skills:
                if int(i) >= 0:
                    skills_cooked.append(f' (+{i})')
                else:
                    skills_cooked.append(f' ({i})')

            skills_ru = ["Акробатика", "Анализ", "Атлетика", "Внимательность", "Выживание", "Выступление", "Запугивание", "История", \
                "Ловкость рук", "Магия", "Медицина", "Обман", "Природа", "Проницательность", "Религия", "Скрытность", "Убеждение", "Уход за животными"]

            # Соединяем столбцы с характеристиками
            skills_cooked = [(skills_ru[i] + skills_cooked[i]) for i in range(18)]
            
            # Переводим в строку для return
            skills_text = '\n'.join(skills_cooked)

            return skills_text


    # Запрос умений и особенностей
    def features_traits(self, chat_id):
        with self.connection:
            self.cursor.execute(f"SELECT rowid, * FROM `{chat_id}_features`")
            # Достаём умения (список кортежей)
            features = self.cursor.fetchall()
            print(features)
            features_cooked = list()
            # Приводим к готовым строкам
            for el in features:
                feature_precooked = str(el[0]) + '. ' + el[1] + '\n' + el[2]
                features_cooked.append(feature_precooked)
            # Переводим в строку для return
            features_text = '\n\n'.join(features_cooked)

            return features_text
    

# db.commit()

# db.close()
