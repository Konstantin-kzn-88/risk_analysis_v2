# Документация базы данных веществ

## Содержание
1. [Общее описание](#общее-описание)
2. [Установка](#установка)
3. [Структура базы данных](#структура-базы-данных)
4. [API](#api)
5. [Примеры использования](#примеры-использования)

## Общее описание

База данных веществ представляет собой SQLite базу данных для хранения и управления информацией о различных химических веществах, включая их физические свойства, параметры взрывоопасности и токсичности.

### Основные возможности:
- Создание, чтение, обновление и удаление записей о веществах (CRUD операции)
- Поиск веществ по названию и типу
- Импорт/экспорт данных в форматах JSON, CSV и Excel
- Логирование операций
- Проверка целостности данных

## Установка

### Зависимости
```bash
pip install pandas
pip install openpyxl
```

### Создание базы данных
```python
from substances_db import SubstanceDatabase

# Создание новой базы данных
db = SubstanceDatabase("substances.db")
```

## Структура базы данных

### Таблица substances

| Поле                        | Тип      | Описание                         | Ограничения |
|----------------------------|----------|----------------------------------|-------------|
| id                         | INTEGER  | Первичный ключ                   | PRIMARY KEY |
| sub_name                   | TEXT     | Название вещества                | NOT NULL    |
| density_liquid             | REAL     | Плотность жидкости, кг/м³        |             |
| molecular_weight           | REAL     | Молярная масса, кг/моль          |             |
| boiling_temperature_liquid | REAL     | Температура кипения, °C          |             |
| heat_evaporation_liquid    | REAL     | Теплота испарения, Дж/кг         |             |
| adiabatic                  | REAL     | Показатель адиабаты              |             |
| heat_capacity_liquid       | REAL     | Теплоемкость жидкости, Дж/кг/°C  |             |
| class_substance           | INTEGER  | Класс взрывоопасности           | 1-4         |
| heat_of_combustion        | REAL     | Теплота сгорания, кДж/кг        |             |
| sigma                     | INTEGER  | Тип смеси                       | 4 или 7     |
| energy_level              | INTEGER  | Тип ТВС                         | 1 или 2     |
| flash_point              | REAL     | Температура вспышки, °C         |             |
| auto_ignition_temp       | REAL     | Температура самовоспламенения, °C|             |
| lower_concentration_limit | REAL     | НКПР, % об.                     |             |
| upper_concentration_limit | REAL     | ВКПР, % об.                     |             |
| threshold_toxic_dose     | REAL     | Пороговая токсодоза, мг*мин/л   |             |
| lethal_toxic_dose       | REAL     | Смертельная токсодоза, мг*мин/л |             |
| sub_type                | INTEGER  | Тип вещества                    | 0-7         |

### Типы веществ (sub_type):
- 0: ЛВЖ (Легковоспламеняющаяся жидкость)
- 1: ЛВЖ токсичная
- 2: СУГ (Сжиженный углеводородный газ)
- 3: СУГ токсичный
- 4: ГЖ (Горючая жидкость)
- 5: ГГ (Горючий газ)
- 6: ГГ токсичный
- 7: Химически опасное вещество (ХОВ) (если токсодоза смертельная == 0 то без токсичного облака)

## API

### Основные операции

#### Создание вещества
```python
create_substance(substance_data: Dict[str, Any]) -> Optional[int]
```
Создает новую запись о веществе. Возвращает ID созданной записи или None в случае ошибки.

#### Получение вещества
```python
get_substance(substance_id: int) -> Optional[Dict[str, Any]]
```
Получает данные о веществе по ID.

#### Получение списка веществ
```python
get_substances(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]
```
Получает список веществ с пагинацией.

#### Обновление вещества
```python
update_substance(substance_id: int, substance_data: Dict[str, Any]) -> bool
```
Обновляет данные о веществе. Возвращает True в случае успеха.

#### Удаление вещества
```python
delete_substance(substance_id: int) -> bool
```
Удаляет вещество из базы данных. Возвращает True в случае успеха.

#### Поиск веществ
```python
search_substances(name: Optional[str] = None, sub_type: Optional[int] = None, limit: int = 100) -> List[Dict[str, Any]]
```
Поиск веществ по имени и/или типу.

### Импорт/Экспорт

#### Экспорт
```python
export_to_csv(filepath: str) -> bool
export_to_json(filepath: str) -> bool
export_to_excel(filepath: str) -> bool
```
Экспорт всех данных в различные форматы.

#### Импорт
```python
import_from_csv(filepath: str, skip_errors: bool = False) -> tuple[int, int]
import_from_json(filepath: str, skip_errors: bool = False) -> tuple[int, int]
import_from_excel(filepath: str, skip_errors: bool = False) -> tuple[int, int]
```
Импорт данных из различных форматов. Возвращает кортеж (количество успешно импортированных записей, количество ошибок).

## Примеры использования

### Создание нового вещества
```python
substance_data = {
    "sub_name": "Бензин АИ-92",
    "density_liquid": 750.0,
    "molecular_weight": 0.095,
    # ... остальные поля
}
substance_id = db.create_substance(substance_data)
```

### Поиск веществ
```python
# Поиск по названию
substances = db.search_substances(name="бензин")

# Поиск по типу
substances = db.search_substances(sub_type=0)  # Поиск всех ЛВЖ
```

### Импорт/экспорт данных
```python
# Экспорт
db.export_to_json("substances_backup.json")
db.export_to_excel("substances_backup.xlsx")
db.export_to_csv("substances_backup.csv")

# Импорт
success, errors = db.import_from_json("substances_backup.json")
print(f"Импортировано: {success}, ошибок: {errors}")
```
