# ------------------------------------------------------------------------------------
# Модуль работы с базой данных веществ.
# @version: 1.0
# @date: 2024-08-29
# ------------------------------------------------------------------------------------
#     sub_name - название вещества,
#     density_liquid - плотность жидкости, кг/м3,
#     heat_capacity_liquid - теплоемкость жидкости, Дж/кг/град.
#     boiling_point - температура кипения, градусов Цельсия,
#     heat_evaporation - теплота испарения, Дж/кг,
#     molecular_weight - молярная масса, г/моль)
#     cont_A - константа А, (константы Антуана)
#     cont_B - константа B,
#     cont_Ca - константа Ca,

# ------------------------------------------------------------------------------------
# @author: Kuznetsov Konstantin, kuznetsov@yandex.ru
# (C) 2024
# ------------------------------------------------------------------------------------

import sqlite3
import os


def create_db():
    # Создаем подключение к базе данных
    connection = sqlite3.connect('sub.db')
    connection.close()


def create_table():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('sub.db')
    cursor = connection.cursor()

    # Создаем таблицу Subs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Subs (
    id INTEGER PRIMARY KEY,
    sub_name TEXT NOT NULL,
    density_liquid INTEGER NOT NULL,
    heat_capacity_liquid INTEGER NOT NULL,
    boiling_point INTEGER NOT NULL,
    heat_evaporation INTEGER NOT NULL,
    molecular_weight INTEGER NOT NULL,
    cont_A REAL NOT NULL,
    cont_B REAL NOT NULL,
    cont_Ca REAL NOT NULL)
    ''')

    # Добавляем новое вещество
    cursor.execute(
        'INSERT INTO Subs (sub_name, density_liquid, heat_capacity_liquid, boiling_point, heat_evaporation, molecular_weight, cont_A, cont_B, cont_Ca) VALUES (?, ?, ?,?,?,?,?,?,?)',
        ('model_sub', 850, 2100, 150, 300000, 100, 7.54424, 2629.65, 387.195))

    cursor.execute(
        'INSERT INTO Subs (sub_name, density_liquid, heat_capacity_liquid, boiling_point, heat_evaporation, molecular_weight, cont_A, cont_B, cont_Ca) VALUES (?, ?, ?,?,?,?,?,?,?)',
        ('Бензин', 860, 2000, 150, 280000, 90, 7.54424, 2629.65, 387.195))

    # Сохраняем изменения и закрываем соединение
    connection.commit()

    connection.close()


def get_in_db(name_sub: str, db_path: str):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect(db_path + 'sub.db')
    cursor = connection.cursor()

    # Выбираем все вещества
    cursor.execute('SELECT * FROM Subs')
    subs = cursor.fetchall()

    # Выводим результаты
    for sub in subs:
        if sub[1] == name_sub:
            connection.close()
            return sub
    # Закрываем соединение
    connection.close()
    return (1, 'model_sub', 850, 2100, 150, 300000, 100, 7.54424, 2629.65, 387.195)


def calc_steam_pressure(sub_property: tuple, temperature: float = 10):
    '''
    Опрелеляет давление насыщенного пара вещества
    :param sub_property: свойства вещества (ф-ция get_in_db
    :param temperature: градусов Цельсия
    :return: давление насыщенного пара вещества, кПа
    '''
    # Получим константы Антуана из кортежа свойств
    cont_A = sub_property[7]
    cont_B = sub_property[8]
    cont_Ca = sub_property[9]

    return pow(10, cont_A - (cont_B / (temperature + cont_Ca)))


if __name__ == '__main__':
    # os.remove('sub.db')
    # create_db()
    # create_table()
    # get_in_db(name_sub='model_sub', db_path='')
    print(calc_steam_pressure((1, 'model_sub', 850, 2100, 150, 300000, 100, 7.54424, 2629.65, 387.195), 100))
