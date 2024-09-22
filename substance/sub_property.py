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
#     class_substance - класс взрывоопасности вещества (1-4)
#     heat_of_combustion - теплота сгорания, кДж/кг
#     sigma - тип смеси  (4- парогазовая, 7 - газовая)
#     energy_level - тип ТВС  (1- легкая, 2 - тяжелая)
#     sub_type - 0-ЛВЖ, 1-ЛВЖ_токси, 2-СУГ, 3-СУГ_токси, 4-ГЖ, 5-ГГ, 5-ГГ_токси

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
        cursor.execute('DROP TABLE if exists Subs')

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
        heat_capacity_liquid INTEGER NOT NULL,
        class_substance INTEGER NOT NULL,
        heat_of_combustion INTEGER NOT NULL,
        sigma INTEGER NOT NULL,
        energy_level INTEGER NOT NULL,
        sub_type INTEGER NOT NULL)
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
                'INSERT INTO Subs (sub_name, density_liquid, molecular_weight, '
                'boiling_temperature_liquid, heat_evaporation_liquid, adiabatic, '
                'heat_capacity_liquid,class_substance,'
                'heat_of_combustion,sigma,energy_level, sub_type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
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
            # Удаляем вещество
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
            cursor.execute(
                'UPDATE Subs SET sub_name= ?, density_liquid= ?, molecular_weight= ?, '
                'boiling_temperature_liquid= ?, heat_evaporation_liquid= ?, adiabatic= ?, '
                'heat_capacity_liquid= ?, class_substance= ?, heat_of_combustion= ?,'
                'sigma= ?,energy_level= ?,sub_type=? WHERE id = ?',
                update_sub)
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
        return (1, 'model_sub', 840, 0.03, 150, 356000, 1.02, 1200, 3, 46000, 7, 1, 0)

    def find_from_db_whith_id(self, sub_id: str, db_path: str):
        # Устанавливаем соединение с базой данных
        connection, cursor = self.connection_to_db(db_path + 'sub.db')

        # Выбираем все вещества
        cursor.execute('SELECT * FROM Subs')
        subs = cursor.fetchall()

        # Выводим результаты
        for sub in subs:
            if sub[0] == sub_id:
                connection.close()
                return sub
        # Сохраняем изменения и закрываем соединение
        self.save_to_db(connection)
        # если ничего не нашли возвращаем модельное вещество
        return (1, 'model_sub', 840, 0.03, 150, 356000, 1.02, 1200, 3, 46000, 7, 1, 0)


if __name__ == '__main__':
    # os.remove('sub.db')
    # Create_DB().create_db()
    # Create_DB().create_table()
    print(Work_DB().add_in_db(sub=('model_sub', 840, 0.03, 150, 356000, 1.02, 1200, 3, 46000, 7, 1, 0), db_path=''))
    print(Work_DB().add_in_db(sub=('Бензин', 840, 0.03, 150, 356000, 1.02, 1200, 3, 46000, 7, 1, 0), db_path=''))
    print(Work_DB().add_in_db(sub=('Бензин_токси', 840, 0.03, 150, 356000, 1.02, 1200, 3, 46000, 7, 1, 1), db_path=''))
    print(Work_DB().find_from_db(name_sub='Бензин', db_path=''))
    print(Work_DB().update_in_db(sub_with_id=(1, 'Бензин', 850, 0.03, 150, 356000, 1.02, 1200, 3, 46000, 7, 1, 0), db_path=''))
    print(Work_DB().del_in_db(id=1, db_path=''))


