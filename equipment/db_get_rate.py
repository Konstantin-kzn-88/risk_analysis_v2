import sqlite3


def extract_rate_tables(db_path, filter_value=None):
    """
    Извлекает данные из таблиц с частотами отказов и формирует список значений.

    Параметры:
    db_path (str): Путь к файлу базы данных SQLite
    filter_value (str): Значение для фильтрации (например, "Менее 75 мм")

    Возвращает:
    list: Список [категория, значение_для_типа_1, значение_для_типа_2]
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получаем все имена таблиц из базы данных
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_tables = [table[0] for table in cursor.fetchall() if table[0].lower().endswith('rate')]

        # Список для хранения результатов
        results = []

        for table in all_tables:
            try:
                # Получаем имена столбцов таблицы
                cursor.execute(f"PRAGMA table_info('{table}')")
                columns = cursor.fetchall()

                # Ищем столбцы для категории и типа
                category_columns = [col[1] for col in columns if any(x in col[1].lower() for x in
                                                                     ['type', 'category', 'diameter', 'pressure'])]

                if category_columns:
                    # Создаем SQL запрос для получения данных
                    query = f"""
                        SELECT {category_columns[0]}, MAX(CASE WHEN type_id = 1 THEN rate_value END) as type1,
                               MAX(CASE WHEN type_id = 2 THEN rate_value END) as type2
                        FROM '{table}'
                        WHERE {category_columns[0]} = ?
                        GROUP BY {category_columns[0]}
                    """
                    cursor.execute(query, (filter_value,))
                    row = cursor.fetchone()

                    if row and row[0]:  # Если нашли данные
                        # Добавляем только если еще нет результатов или это новые данные
                        if not results:
                            results = [row[0], row[1], row[2]]

            except Exception as e:
                print(f"Ошибка при обработке таблицы {table}: {str(e)}")
                continue

        return results

    except Exception as e:
        print(f"Ошибка подключения к базе данных: {str(e)}")
        return None

    finally:
        if 'conn' in locals():
            conn.close()


# Пример использования:
if __name__ == "__main__":
    db_path = "db_eq.db"
    result = extract_rate_tables(db_path, "Менее 75 мм")
    if result:
        print(result)