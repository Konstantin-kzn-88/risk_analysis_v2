# Модуль работы с базой данных оборудования.
# @version: 1.0
# @date: 2024-08-29
# ------------------------------------------------------------------------------------
#     eq_name - название оборудования,
#     volume_equipment - объем, м3,
#     degree_filling - cтепень заполения, доли единицы
#     spill_square
#     pressure_equipment - давление, МПа
#     temperature_equipment - температура, градусов Цельсия,
#     eq_type - тип оборудования 0 - емк.под давлением, 1 - РВС, 2 - насос, 3 - технол.аппарат, 4 - цистерна
#     lenght_pipeline - длина трубопровода, км,
#     diameter_pipeline - диаметр трубопровода, мм
#     eq_type - тип оборудования 10 - жидкость, 11 - газ, 12 - СУГ

#     part_opo - составляющая ОПО
#     dead_people_max - максимально прогнозируемое количество погибших
#     inj_people_max - максимально прогнозируемое количество пострадавших

# ------------------------------------------------------------------------------------
# @author: Kuznetsov Konstantin, kuznetsov@yandex.ru
# (C) 2024
# ------------------------------------------------------------------------------------

import sqlite3
import os


class Equipment_DB:
    """Класс создания базы данных и таблицы в ней"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_db(self):
        # Создаем подключение к базе данных
        connection = sqlite3.connect(self.db_path)
        connection.close()

    def create_table(self):
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Создаем таблицу Equipment
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Equipment (
        id INTEGER PRIMARY KEY,
        eq_name TEXT NOT NULL,
        volume_equipment REAL NOT NULL,
        degree_filling REAL NOT NULL,       
        spill_square INTEGER NOT NULL,       
        pressure_equipment REAL NOT NULL,
        temperature_equipment INTEGER NOT NULL,
        part_opo TEXT NOT NULL,
        dead_people_max INTEGER NOT NULL,
        inj_people_max INTEGER NOT NULL,
        sub_id INTEGER NOT NULL,
        eq_type INTEGER NOT NULL)
        ''')

        # Сохраняем изменения и закрываем соединение
        connection.commit()

        # Создаем таблицу Equipment_pipeline
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Equipment_pipeline (
        id INTEGER PRIMARY KEY,
        eq_name TEXT NOT NULL,
        lenght_pipeline REAL NOT NULL,
        diameter_pipeline REAL NOT NULL,        
        pressure_equipment REAL NOT NULL,
        temperature_equipment INTEGER NOT NULL,
        part_opo TEXT NOT NULL,
        dead_people_max INTEGER NOT NULL,
        inj_people_max INTEGER NOT NULL,
        sub_id INTEGER NOT NULL,
        eq_type INTEGER NOT NULL)
        ''')

        # Сохраняем изменения и закрываем соединение
        connection.commit()

        # Создаем таблицу Equipment_result
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Equipment_result (
        id INTEGER PRIMARY KEY,
        id_equipment INTEGER NOT NULL,
        name_equipment_or_pipeline TEXT NOT NULL,
        part_opo TEXT NOT NULL,
        scnario TEXT NOT NULL,
        scnario_value REAL NOT NULL,
        mass_all REAL NOT NULL,
        mass_pf REAL NOT NULL,
        q_10 REAL NOT NULL,
        q_7 REAL NOT NULL,        
        q_4 REAL NOT NULL,
        q_1 REAL NOT NULL,
        p_70 REAL NOT NULL,
        p_28 REAL NOT NULL,        
        p_14 REAL NOT NULL,
        p_5 REAL NOT NULL,
        p_2 REAL NOT NULL,
        Lf REAL NOT NULL,        
        Df REAL NOT NULL,
        Rnkpr REAL NOT NULL,
        Rvsp REAL NOT NULL,
        LPt REAL NOT NULL,
        PPt REAL NOT NULL,        
        Q600 REAL NOT NULL,
        Q320 REAL NOT NULL,
        Q220 REAL NOT NULL,
        Q120 REAL NOT NULL,        
        St REAL NOT NULL,
        direct_losses INTEGER NOT NULL,
        localization INTEGER NOT NULL,        
        socio INTEGER NOT NULL,
        ecolog INTEGER NOT NULL,
        indirect INTEGER NOT NULL,
        sum_damage INTEGER NOT NULL,
        dead INTEGER NOT NULL,        
        injured INTEGER NOT NULL,
        collective_dead REAL NOT NULL,
        collective_injured REAL NOT NULL,        
        math_expectation REAL NOT NULL)
        ''')

        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()

    def connection_to_db(self):
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        return (connection, cursor)

    def save_to_db(self, connection):
        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()

    # Функции оборудования
    def add_in_Equipment_table(self, equipment: tuple):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db()
            # Добавляем оборудование
            cursor.execute(
                'INSERT INTO Equipment (eq_name, volume_equipment, degree_filling, spill_square, pressure_equipment, temperature_equipment, part_opo, dead_people_max, inj_people_max, sub_id, eq_type) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                equipment)
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def del_in_Equipment_table(self, id: int):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db()
            # Удаляем оборудование
            cursor.execute('DELETE FROM Equipment WHERE id = ?', (id,))
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def update_in_Equipment_table(self, eqp_with_id: tuple):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db()
            # Обновляем
            update_eqp = list(eqp_with_id)
            update_eqp.pop(0)
            update_eqp.append(eqp_with_id[0])
            cursor.execute(
                'UPDATE Equipment SET eq_name = ?, volume_equipment = ?, degree_filling = ?, spill_square = ?, pressure_equipment = ?, temperature_equipment = ?, part_opo= ?, dead_people_max= ?, inj_people_max= ?, sub_id = ?, eq_type=? WHERE id = ?',
                update_eqp)
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def find_from_Equipment_table(self, id: int):
        # Устанавливаем соединение с базой данных
        connection, cursor = self.connection_to_db()

        # Выбираем все
        cursor.execute('SELECT * FROM Equipment')
        equips = cursor.fetchall()

        # Выводим результаты
        for equip in equips:
            if equip[0] == id:
                connection.close()
                return equip
        # Сохраняем изменения и закрываем соединение
        self.save_to_db(connection)
        # если ничего не нашли возвращаем модельное вещество
        return 400

    def get_all_equipment_table(self):
        # Устанавливаем соединение с базой данных
        connection, cursor = self.connection_to_db()
        # Выбираем все
        cursor.execute('SELECT * FROM Equipment')
        equips = cursor.fetchall()
        return equips

    def get_all_equipment_pipeline_table(self):
        # Устанавливаем соединение с базой данных
        connection, cursor = self.connection_to_db()
        # Выбираем все
        cursor.execute('SELECT * FROM Equipment_pipeline')
        pipelines = cursor.fetchall()
        return pipelines

    def get_equipment_result_table(self):
        # Устанавливаем соединение с базой данных
        connection, cursor = self.connection_to_db()
        # Выбираем все
        cursor.execute('SELECT * FROM Equipment_result')
        result = cursor.fetchall()
        return result


    # def get_fieldnames(self):
    #     # Получить наименование полей
    #     # Устанавливаем соединение с базой данных
    #     connection, cursor = self.connection_to_db()
    #     cursor.execute("select * from Equipment_result")
    #     fieldnames = [f[0] for f in cursor.description]
    #     return fieldnames
    #
    def table(self):
        # Устанавливаем соединение с базой данных
        connection, cursor = self.connection_to_db()
        cursor.execute('DROP TABLE if exists Equipment_pipeline')
        # Создаем таблицу Equipment_pipeline
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Equipment_pipeline (
        id INTEGER PRIMARY KEY,
        eq_name TEXT NOT NULL,
        lenght_pipeline REAL NOT NULL,
        diameter_pipeline REAL NOT NULL,        
        pressure_equipment REAL NOT NULL,
        temperature_equipment INTEGER NOT NULL,
        time_off INTEGER NOT NULL,
        part_lenght_pipeline REAL NOT NULL,
        part_opo TEXT NOT NULL,
        dead_people_max INTEGER NOT NULL,
        inj_people_max INTEGER NOT NULL,
        sub_id INTEGER NOT NULL,
        eq_type INTEGER NOT NULL)
        ''')
        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()

    # Функции трубопроводов
    def add_in_Equipment_pipeline(self, pipeline: tuple):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db()
            # Добавляем оборудование
            cursor.execute(
                'INSERT INTO Equipment_pipeline (eq_name, lenght_pipeline, diameter_pipeline, pressure_equipment, temperature_equipment, time_off, part_lenght_pipeline, part_opo, dead_people_max, inj_people_max, sub_id, eq_type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                pipeline)
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def del_in_Equipment_pipeline(self, id: int):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db()
            # Удаляем оборудование
            cursor.execute('DELETE FROM Equipment_pipeline WHERE id = ?', (id,))
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def update_in_Equipment_pipeline(self, eqp_with_id: tuple):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db()
            # Обновляем
            update_eqp = list(eqp_with_id)
            update_eqp.pop(0)
            update_eqp.append(eqp_with_id[0])
            cursor.execute(
                'UPDATE Equipment_pipeline SET eq_name= ?, lenght_pipeline= ?, diameter_pipeline= ?, pressure_equipment= ?, temperature_equipment= ?, , time_off= ?, part_lenght_pipeline= ?, part_opo= ?, dead_people_max= ?, inj_people_max= ?, sub_id= ?, eq_type= ? WHERE id = ?',
                update_eqp)
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def find_from_Equipment_pipeline(self, id: int):
        # Устанавливаем соединение с базой данных
        connection, cursor = self.connection_to_db()

        # Выбираем все
        cursor.execute('SELECT * FROM Equipment_pipeline')
        equips = cursor.fetchall()

        # Выводим результаты
        for equip in equips:
            if equip[0] == id:
                connection.close()
                return equip
        # Сохраняем изменения и закрываем соединение
        self.save_to_db(connection)
        # если ничего не нашли возвращаем модельное вещество
        return 400

    def add_result(self, data):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db()
            # Добавляем оборудование
            cursor.execute(
                'INSERT INTO Equipment_result (id_equipment, name_equipment_or_pipeline, part_opo, scnario, scnario_value,scnario_description, '
                'mass_all, mass_pf, q_10, q_7, q_4, q_1, '
                'p_70, p_28, p_14, p_5, p_2, Lf, '
                'Df, Rnkpr, Rvsp, LPt, PPt, Q600, '
                'Q320, Q220, Q120, St, direct_losses, localization, '
                'socio, ecolog, indirect, sum_damage, dead, injured, '
                'collective_dead, collective_injured, math_expectation) VALUES (?,?,?,?,?,?,'
                '?,?,?,?,?,?,'
                '?,?,?,?,?,?,'
                '?,?,?,?,?,?,'
                '?,?,?,?,?,?,'
                '?,?,?,?,?,?,'
                '?,?,?)', data)
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400

    def clear_equipment_result(self):
        try:
            # Устанавливаем соединение с базой данных
            connection, cursor = self.connection_to_db()
            # Очищаем
            cursor.execute('DELETE FROM Equipment_result')
            # Сохраняем изменения и закрываем соединение
            self.save_to_db(connection)
            return 200
        except:
            return 400


if __name__ == '__main__':
    print(Equipment_DB('equipment.db').table())
