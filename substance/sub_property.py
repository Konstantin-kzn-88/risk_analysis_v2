import sqlite3
from typing import Optional, List, Dict, Any
import logging
import os
# Добавить в начало файла импорты:
import csv
import json
from typing import List, Dict, Any, Optional, TextIO
import pandas as pd



class SubstanceDatabase:
    def __init__(self, db_path: str):
        """
        Инициализация подключения к базе данных

        Args:
            db_path (str): Путь к файлу базы данных SQLite
        """
        self.db_path = db_path
        self.logger = self._setup_logger()

        # Создаем базу данных и таблицу при первом подключении
        self._initialize_database()

    def _setup_logger(self) -> logging.Logger:
        """Настройка логгера"""
        logger = logging.getLogger('SubstanceDB')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _get_connection(self) -> sqlite3.Connection:
        """Получение подключения к базе данных"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Для получения словарей вместо кортежей
            return conn
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка подключения к базе данных: {e}")
            raise

    def _initialize_database(self) -> None:
        """Создание таблицы если она не существует"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS substances (
            id INTEGER PRIMARY KEY,
            sub_name TEXT NOT NULL,
            density_liquid REAL,
            molecular_weight REAL,
            boiling_temperature_liquid REAL,
            heat_evaporation_liquid REAL,
            adiabatic REAL,
            heat_capacity_liquid REAL,
            class_substance INTEGER CHECK (class_substance BETWEEN 1 AND 4),
            heat_of_combustion REAL,
            sigma INTEGER CHECK (sigma IN (4, 7)),
            energy_level INTEGER CHECK (energy_level IN (1, 2)),
            flash_point REAL,
            auto_ignition_temp REAL,
            lower_concentration_limit REAL,
            upper_concentration_limit REAL,
            threshold_toxic_dose REAL,
            lethal_toxic_dose REAL,
            sub_type INTEGER CHECK (sub_type BETWEEN 0 AND 7),

            CHECK (lower_concentration_limit < upper_concentration_limit),
            CHECK (flash_point < auto_ignition_temp)
        );

        CREATE INDEX IF NOT EXISTS idx_substance_name ON substances(sub_name);
        CREATE INDEX IF NOT EXISTS idx_substance_type ON substances(sub_type);
        """

        try:
            with self._get_connection() as conn:
                conn.executescript(create_table_sql)
                self.logger.info("База данных инициализирована успешно")
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка при инициализации базы данных: {e}")
            raise

    def get_connection_info(self) -> Dict[str, Any]:
        """Получение информации о подключении к базе данных"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM substances;")
                record_count = cursor.fetchone()[0]

                return {
                    "database_path": self.db_path,
                    "sqlite_version": version,
                    "record_count": record_count,
                    "status": "connected"
                }
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка при получении информации о подключении: {e}")
            return {
                "database_path": self.db_path,
                "status": "error",
                "error_message": str(e)
            }

    # Добавить в класс SubstanceDatabase:

    def create_substance(self, substance_data: Dict[str, Any]) -> Optional[int]:
        """
        Создание новой записи о веществе

        Args:
            substance_data (dict): Словарь с данными о веществе

        Returns:
            Optional[int]: ID созданной записи или None в случае ошибки
        """
        insert_sql = """
        INSERT INTO substances (
            sub_name, density_liquid, molecular_weight, boiling_temperature_liquid,
            heat_evaporation_liquid, adiabatic, heat_capacity_liquid, class_substance,
            heat_of_combustion, sigma, energy_level, flash_point, auto_ignition_temp,
            lower_concentration_limit, upper_concentration_limit, threshold_toxic_dose,
            lethal_toxic_dose, sub_type
        ) VALUES (
            :sub_name, :density_liquid, :molecular_weight, :boiling_temperature_liquid,
            :heat_evaporation_liquid, :adiabatic, :heat_capacity_liquid, :class_substance,
            :heat_of_combustion, :sigma, :energy_level, :flash_point, :auto_ignition_temp,
            :lower_concentration_limit, :upper_concentration_limit, :threshold_toxic_dose,
            :lethal_toxic_dose, :sub_type
        )
        """

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(insert_sql, substance_data)
                self.logger.info(f"Создана новая запись о веществе: {substance_data['sub_name']}")
                return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка при создании записи: {e}")
            return None

    def get_substance(self, substance_id: int) -> Optional[Dict[str, Any]]:
        """
        Получение данных о веществе по ID

        Args:
            substance_id (int): ID вещества

        Returns:
            Optional[Dict[str, Any]]: Словарь с данными о веществе или None
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM substances WHERE id = ?", (substance_id,))
                row = cursor.fetchone()

                if row:
                    return dict(row)
                self.logger.warning(f"Вещество с ID {substance_id} не найдено")
                return None
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка при получении данных о веществе: {e}")
            return None

    def get_substances(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Получение списка веществ с пагинацией

        Args:
            limit (int): Количество записей на странице
            offset (int): Смещение от начала

        Returns:
            List[Dict[str, Any]]: Список словарей с данными о веществах
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM substances LIMIT ? OFFSET ?",
                    (limit, offset)
                )
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка при получении списка веществ: {e}")
            return []

    def update_substance(self, substance_id: int, substance_data: Dict[str, Any]) -> bool:
        """
        Обновление данных о веществе

        Args:
            substance_id (int): ID вещества
            substance_data (dict): Словарь с обновленными данными

        Returns:
            bool: True если обновление успешно, False в случае ошибки
        """
        update_sql = """
        UPDATE substances SET
            sub_name = :sub_name,
            density_liquid = :density_liquid,
            molecular_weight = :molecular_weight,
            boiling_temperature_liquid = :boiling_temperature_liquid,
            heat_evaporation_liquid = :heat_evaporation_liquid,
            adiabatic = :adiabatic,
            heat_capacity_liquid = :heat_capacity_liquid,
            class_substance = :class_substance,
            heat_of_combustion = :heat_of_combustion,
            sigma = :sigma,
            energy_level = :energy_level,
            flash_point = :flash_point,
            auto_ignition_temp = :auto_ignition_temp,
            lower_concentration_limit = :lower_concentration_limit,
            upper_concentration_limit = :upper_concentration_limit,
            threshold_toxic_dose = :threshold_toxic_dose,
            lethal_toxic_dose = :lethal_toxic_dose,
            sub_type = :sub_type
        WHERE id = :id
        """

        try:
            with self._get_connection() as conn:
                substance_data['id'] = substance_id
                cursor = conn.cursor()
                cursor.execute(update_sql, substance_data)

                if cursor.rowcount > 0:
                    self.logger.info(f"Обновлены данные о веществе с ID {substance_id}")
                    return True
                self.logger.warning(f"Вещество с ID {substance_id} не найдено")
                return False
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка при обновлении данных о веществе: {e}")
            return False

    def delete_substance(self, substance_id: int) -> bool:
        """
        Удаление вещества из базы данных

        Args:
            substance_id (int): ID вещества

        Returns:
            bool: True если удаление успешно, False в случае ошибки
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM substances WHERE id = ?", (substance_id,))

                if cursor.rowcount > 0:
                    self.logger.info(f"Удалено вещество с ID {substance_id}")
                    return True
                self.logger.warning(f"Вещество с ID {substance_id} не найдено")
                return False
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка при удалении вещества: {e}")
            return False

    def search_substances(
            self,
            name: Optional[str] = None,
            sub_type: Optional[int] = None,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Поиск веществ по имени и/или типу

        Args:
            name (Optional[str]): Часть названия вещества
            sub_type (Optional[int]): Тип вещества
            limit (int): Максимальное количество результатов

        Returns:
            List[Dict[str, Any]]: Список найденных веществ
        """
        query = "SELECT * FROM substances WHERE 1=1"
        params = []

        if name:
            query += " AND sub_name LIKE ?"
            params.append(f"%{name}%")

        if sub_type is not None:
            query += " AND sub_type = ?"
            params.append(sub_type)

        query += " LIMIT ?"
        params.append(limit)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка при поиске веществ: {e}")
            return []

    # Добавить в класс SubstanceDatabase:

    def export_to_csv(self, filepath: str) -> bool:
        """
        Экспорт всех данных в CSV файл

        Args:
            filepath (str): Путь к файлу для сохранения

        Returns:
            bool: True если экспорт успешен, False в случае ошибки
        """
        try:
            with self._get_connection() as conn:
                # Получаем все данные
                df = pd.read_sql_query("SELECT * FROM substances", conn)

                # Сохраняем в CSV
                df.to_csv(filepath, index=False, encoding='utf-8')
                self.logger.info(f"Данные успешно экспортированы в {filepath}")
                return True
        except Exception as e:
            self.logger.error(f"Ошибка при экспорте в CSV: {e}")
            return False

    def export_to_json(self, filepath: str) -> bool:
        """
        Экспорт всех данных в JSON файл

        Args:
            filepath (str): Путь к файлу для сохранения

        Returns:
            bool: True если экспорт успешен, False в случае ошибки
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM substances")
                rows = [dict(row) for row in cursor.fetchall()]

                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(rows, f, ensure_ascii=False, indent=2)

                self.logger.info(f"Данные успешно экспортированы в {filepath}")
                return True
        except Exception as e:
            self.logger.error(f"Ошибка при экспорте в JSON: {e}")
            return False

    def export_to_excel(self, filepath: str) -> bool:
        """
        Экспорт всех данных в Excel файл

        Args:
            filepath (str): Путь к файлу для сохранения

        Returns:
            bool: True если экспорт успешен, False в случае ошибки
        """
        try:
            with self._get_connection() as conn:
                # Получаем все данные
                df = pd.read_sql_query("SELECT * FROM substances", conn)

                # Сохраняем в Excel
                df.to_excel(filepath, index=False, engine='openpyxl')
                self.logger.info(f"Данные успешно экспортированы в {filepath}")
                return True
        except Exception as e:
            self.logger.error(f"Ошибка при экспорте в Excel: {e}")
            return False

    def import_from_csv(self, filepath: str, skip_errors: bool = False) -> tuple[int, int]:
        """
        Импорт данных из CSV файла

        Args:
            filepath (str): Путь к файлу для импорта
            skip_errors (bool): Пропускать ошибочные записи

        Returns:
            tuple[int, int]: (количество успешно импортированных записей, количество ошибок)
        """
        success_count = 0
        error_count = 0

        try:
            df = pd.read_csv(filepath)

            # Проверяем наличие всех необходимых колонок
            required_columns = [
                'sub_name', 'density_liquid', 'molecular_weight',
                'boiling_temperature_liquid', 'heat_evaporation_liquid',
                'adiabatic', 'heat_capacity_liquid', 'class_substance',
                'heat_of_combustion', 'sigma', 'energy_level', 'flash_point',
                'auto_ignition_temp', 'lower_concentration_limit',
                'upper_concentration_limit', 'threshold_toxic_dose',
                'lethal_toxic_dose', 'sub_type'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}")

            for _, row in df.iterrows():
                try:
                    substance_data = row.to_dict()
                    # Удаляем id если он есть в данных
                    substance_data.pop('id', None)

                    if self.create_substance(substance_data):
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    self.logger.error(f"Ошибка при импорте строки: {e}")
                    error_count += 1
                    if not skip_errors:
                        raise

            self.logger.info(f"Импорт завершен: {success_count} успешно, {error_count} ошибок")
            return success_count, error_count

        except Exception as e:
            self.logger.error(f"Ошибка при импорте из CSV: {e}")
            return success_count, error_count

    def import_from_json(self, filepath: str, skip_errors: bool = False) -> tuple[int, int]:
        """
        Импорт данных из JSON файла

        Args:
            filepath (str): Путь к файлу для импорта
            skip_errors (bool): Пропускать ошибочные записи

        Returns:
            tuple[int, int]: (количество успешно импортированных записей, количество ошибок)
        """
        success_count = 0
        error_count = 0

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                substances = json.load(f)

            for substance_data in substances:
                try:
                    # Удаляем id если он есть в данных
                    substance_data.pop('id', None)

                    if self.create_substance(substance_data):
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    self.logger.error(f"Ошибка при импорте записи: {e}")
                    error_count += 1
                    if not skip_errors:
                        raise

            self.logger.info(f"Импорт завершен: {success_count} успешно, {error_count} ошибок")
            return success_count, error_count

        except Exception as e:
            self.logger.error(f"Ошибка при импорте из JSON: {e}")
            return success_count, error_count

    def import_from_excel(self, filepath: str, skip_errors: bool = False) -> tuple[int, int]:
        """
        Импорт данных из Excel файла

        Args:
            filepath (str): Путь к файлу для импорта
            skip_errors (bool): Пропускать ошибочные записи

        Returns:
            tuple[int, int]: (количество успешно импортированных записей, количество ошибок)
        """
        success_count = 0
        error_count = 0

        try:
            df = pd.read_excel(filepath, engine='openpyxl')

            # Проверяем наличие всех необходимых колонок
            required_columns = [
                'sub_name', 'density_liquid', 'molecular_weight',
                'boiling_temperature_liquid', 'heat_evaporation_liquid',
                'adiabatic', 'heat_capacity_liquid', 'class_substance',
                'heat_of_combustion', 'sigma', 'energy_level', 'flash_point',
                'auto_ignition_temp', 'lower_concentration_limit',
                'upper_concentration_limit', 'threshold_toxic_dose',
                'lethal_toxic_dose', 'sub_type'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}")

            for _, row in df.iterrows():
                try:
                    substance_data = row.to_dict()
                    # Удаляем id если он есть в данных
                    substance_data.pop('id', None)

                    if self.create_substance(substance_data):
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    self.logger.error(f"Ошибка при импорте строки: {e}")
                    error_count += 1
                    if not skip_errors:
                        raise

            self.logger.info(f"Импорт завершен: {success_count} успешно, {error_count} ошибок")
            return success_count, error_count

        except Exception as e:
            self.logger.error(f"Ошибка при импорте из Excel: {e}")
            return success_count, error_count


if __name__ == '__main__':
    import os
    from pprint import pprint

    # Инициализация базы данных
    db = SubstanceDatabase("substances.db")

    # print("1. Добавление веществ")
    # # Бензин АИ-92
    # benzine = {
    #     "sub_name": "Бензин АИ-92",
    #     "density_liquid": 750.0,
    #     "molecular_weight": 0.095,
    #     "boiling_temperature_liquid": 35.0,
    #     "heat_evaporation_liquid": 372000.0,
    #     "adiabatic": 1.1,
    #     "heat_capacity_liquid": 2100.0,
    #     "class_substance": 4,
    #     "heat_of_combustion": 43600.0,
    #     "sigma": 4,
    #     "energy_level": 2,
    #     "flash_point": -27.0,
    #     "auto_ignition_temp": 255.0,
    #     "lower_concentration_limit": 0.76,
    #     "upper_concentration_limit": 8.0,
    #     "threshold_toxic_dose": None,
    #     "lethal_toxic_dose": None,
    #     "sub_type": 0  # ЛВЖ
    # }
    # benzine_id = db.create_substance(benzine)
    # print(f"Создан бензин с ID: {benzine_id}")
    #
    # # Дизельное топливо
    # diesel = {
    #     "sub_name": "Дизельное топливо",
    #     "density_liquid": 840.0,
    #     "molecular_weight": 0.172,
    #     "boiling_temperature_liquid": 180.0,
    #     "heat_evaporation_liquid": 210000.0,
    #     "adiabatic": 1.1,
    #     "heat_capacity_liquid": 1850.0,
    #     "class_substance": 4,
    #     "heat_of_combustion": 43600.0,
    #     "sigma": 4,
    #     "energy_level": 2,
    #     "flash_point": 35.0,
    #     "auto_ignition_temp": 210.0,
    #     "lower_concentration_limit": 0.52,
    #     "upper_concentration_limit": 4.0,
    #     "threshold_toxic_dose": None,
    #     "lethal_toxic_dose": None,
    #     "sub_type": 4  # ГЖ
    # }
    # diesel_id = db.create_substance(diesel)
    # print(f"Создано дизельное топливо с ID: {diesel_id}")
    #
    # # Окись этилена
    # ethylene_oxide = {
    #     "sub_name": "Окись этилена",
    #     "density_liquid": 882.0,
    #     "molecular_weight": 0.044,
    #     "boiling_temperature_liquid": 10.7,
    #     "heat_evaporation_liquid": 578000.0,
    #     "adiabatic": 1.2,
    #     "heat_capacity_liquid": 1930.0,
    #     "class_substance": 2,
    #     "heat_of_combustion": 29000.0,
    #     "sigma": 4,
    #     "energy_level": 1,
    #     "flash_point": -18.0,
    #     "auto_ignition_temp": 429.0,
    #     "lower_concentration_limit": 2.3,
    #     "upper_concentration_limit": 100.0,
    #     "threshold_toxic_dose": 2.2,
    #     "lethal_toxic_dose": 4.4,
    #     "sub_type": 1  # ЛВЖ токсичная
    # }
    # ethylene_id = db.create_substance(ethylene_oxide)
    # print(f"Создана окись этилена с ID: {ethylene_id}")
    #
    # print("\n2. Получение свойств по ID")
    # substance = db.get_substance(diesel_id)
    # print("Свойства дизельного топлива:")
    # pprint(substance)
    #
    # print("\n3. Получение списка всех веществ")
    # substances = db.get_substances()
    # print(f"Всего веществ в базе: {len(substances)}")
    # for substance in substances:
    #     print(f"- {substance['sub_name']}")
    #
    # print("\n4. Обновление данных о веществе (изменение на ДТ зимнее)")
    # winter_diesel = substance.copy()
    # winter_diesel.update({
    #     "sub_name": "ДТ зимнее",
    #     "density_liquid": 820.0,
    #     "flash_point": 30.0,
    #     "auto_ignition_temp": 220.0
    # })
    # success = db.update_substance(diesel_id, winter_diesel)
    # print(f"Обновление {'успешно' if success else 'не удалось'}")
    #
    # print("\n5. Удаление вещества с ID=1")
    # success = db.delete_substance(1)
    # print(f"Удаление {'успешно' if success else 'не удалось'}")
    #
    # print("\n6. Поиск вещества 'бензин'")
    # found = db.search_substances(name='бензин')
    # print("Найдены вещества:")
    # for substance in found:
    #     print(f"- {substance['sub_name']}")
    #
    # print("\n7. Экспорт данных")
    db.export_to_json("substances_backup.json")
    # db.export_to_excel("substances_backup.xlsx")
    # db.export_to_csv("substances_backup.csv")
    # print("Данные экспортированы")

    # print("\n8. Удаление всех веществ и импорт из JSON")
    # # Удаляем все записи путем пересоздания таблицы
    # with db._get_connection() as conn:
    #     conn.execute("DROP TABLE substances")
    # db._initialize_database()
    #
    # success, errors = db.import_from_json("substances_backup.json")
    # print(f"Импорт из JSON: успешно - {success}, ошибок - {errors}")

    # print("\n9. Удаление всех веществ и импорт из Excel")
    # with db._get_connection() as conn:
    #     conn.execute("DROP TABLE substances")
    # db._initialize_database()
    #
    # success, errors = db.import_from_excel("substances_backup.xlsx")
    # print(f"Импорт из Excel: успешно - {success}, ошибок - {errors}")

    print("\nГотово!")