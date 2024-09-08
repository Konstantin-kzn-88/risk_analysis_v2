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
#     molecular_weight - молярная масса, кг/моль)
#     adiabatic - адиабата

# ------------------------------------------------------------------------------------
# @author: Kuznetsov Konstantin, kuznetsov@yandex.ru
# (C) 2024
# ------------------------------------------------------------------------------------

import sqlite3
import os


class Create_DB:
    """Класс создания базы данных и таблицы в ней"""

    def create_db(self):
        # Создаем подключение к базе данных
        connection = sqlite3.connect('sub.db')
        connection.close()

    def create_table(self):
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect('sub.db')
        cursor = connection.cursor()

        # Создаем таблицу Subs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Subs (
        id INTEGER PRIMARY KEY,
        sub_name TEXT NOT NULL,
        density_liquid INTEGER NOT NULL,
        molecular_weight INTEGER NOT NULL,
        boiling_temperature_liquid INTEGER NOT NULL,
        heat_evaporation_liquid INTEGER NOT NULL,
        adiabatic REAL NOT NULL, 
        heat_capacity_liquid INTEGER NOT NULL)
        ''')

        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()


class Work_DB:

    def connection_to_db(self, db: str):
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        return (connection, cursor)

    def save_to_db(self, connection):
        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()

    def add_in_db(self, sub: tuple, db_path: str):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db(db_path + 'sub.db')
            # Добавляем вещество
            cursor.execute(
                'INSERT INTO Subs (sub_name, density_liquid, molecular_weight, boiling_temperature_liquid, heat_evaporation_liquid, adiabatic, heat_capacity_liquid) VALUES (?,?,?,?,?,?,?)',
                sub)
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def del_in_db(self, id: int, db_path: str):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db(db_path + 'sub.db')
            # Добавляем вещество
            cursor.execute('DELETE FROM Subs WHERE id = ?', (id,))
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def update_in_db(self, sub_with_id: tuple, db_path: str):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db(db_path + 'sub.db')
            # Обновляем
            update_sub = list(sub_with_id)
            update_sub.pop(0)
            update_sub.append(sub_with_id[0])
            cursor.execute('UPDATE Subs SET sub_name= ?, density_liquid= ?, molecular_weight= ?, boiling_temperature_liquid= ?, heat_evaporation_liquid= ?, adiabatic= ?, heat_capacity_liquid= ? WHERE id = ?', update_sub)
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def find_from_db(self, name_sub: str, db_path: str):
        # Устанавливаем соединение с базой данных
        connection, cursor = self.connection_to_db(db_path + 'sub.db')

        # Выбираем все вещества
        cursor.execute('SELECT * FROM Subs')
        subs = cursor.fetchall()

        # Выводим результаты
        for sub in subs:
            if sub[1] == name_sub:
                connection.close()
                return sub
        # Сохраняем изменения и закрываем соединение
        self.save_to_db(connection)
        # если ничего не нашли возвращаем модельное вещество
        return (1, 'model_sub', 851, 0.04, 151, 356001, 1.02, 1201)


if __name__ == '__main__':
    # os.remove('sub.db')
    # create_db()
    # create_table()
    print(Work_DB().add_in_db(sub=('model_sub', 840, 0.03, 150, 356000, 1.02, 1200), db_path=''))
    print(Work_DB().find_from_db(name_sub='Бензин', db_path=''))
    print(Work_DB().update_in_db(sub_with_id=(1, 'model_sub', 851, 0.04, 151, 356001, 1.02, 1201), db_path=''))
    print(Work_DB().del_in_db(id=1, db_path=''))

