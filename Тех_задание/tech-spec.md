# Техническое задание
## Программа анализа риска аварий для промышленного предприятия

### 1. Общие сведения
#### 1.1. Наименование программы
"Industrial Risk Analyzer" (IRA) - Программа анализа риска аварий для промышленного предприятия

#### 1.2. Назначение и цели
Программа предназначена для:
- Визуализации планов промышленного предприятия
- Нанесения и учета объектов на территории
- Расчета зон поражающих факторов при авариях
- Создания ситуационных планов
- Формирования отчетной документации

### 2. Технические требования
#### 2.1. Требования к функциональным характеристикам

##### 2.1.1. Загрузка и отображение графической подложки
- Поддержка форматов: JPG, PNG
- Масштабирование изображения
- Навигация по изображению (перемещение, зуммирование)
- Сохранение параметров отображения между сессиями

##### 2.1.2. Работа с объектами
- Нанесение объектов следующих типов:

###### 2.1.2.1 Емкости (Tank)
- Геометрия: полигональный объект
- Параметры:
  * Тип вещества (СУГ/жидкость/газ/токсичное вещество)
  * Объем (м³)
  * Степень заполнения (%)
  * Рабочее давление (МПа)
  * Рабочая температура (°C)
  * Масса вещества (кг)
  * Агрегатное состояние
  * Физико-химические свойства вещества
  * Геометрические размеры (длина, ширина, высота)

###### 2.1.2.2 Трубопроводы (Pipeline)
- Геометрия: линейный объект
- Параметры:
  * Тип вещества (СУГ/жидкость/газ/токсичное вещество)
  * Диаметр (мм)
  * Толщина стенки (мм)
  * Рабочее давление (МПа)
  * Рабочая температура (°C)
  * Расход вещества
  * Скорость потока
  * Длина участка
  * Материал трубопровода
  * Тип соединений

###### 2.1.2.3 Насосное оборудование (Pump)
- Геометрия: точечный объект
- Параметры:
  * Тип перекачиваемого вещества (СУГ/жидкость/токсичное вещество)
  * Производительность (м³/ч)
  * Рабочее давление (МПа)
  * Мощность электродвигателя (кВт)
  * Частота вращения (об/мин)
  * Тип насоса
  * Наличие резервирования
  * Наличие систем защиты
  * Тип уплотнений

###### 2.1.2.4 Компрессорное оборудование (Compressor)
- Геометрия: точечный объект
- Параметры:
  * Тип сжимаемого вещества (газ/токсичное вещество)
  * Производительность (нм³/ч)
  * Давление всасывания (МПа)
  * Давление нагнетания (МПа)
  * Мощность электродвигателя (кВт)
  * Частота вращения (об/мин)
  * Тип компрессора (поршневой/винтовой/центробежный)
  * Число ступеней сжатия
  * Температура газа на всасывании (°C)
  * Температура газа на нагнетании (°C)
  * Тип уплотнений
  * Наличие систем охлаждения
  * Наличие систем защиты

###### 2.1.2.5 Теплообменное оборудование (HeatExchanger)
- Геометрия: полигональный объект
- Параметры:
  * Тип веществ (СУГ/жидкость/газ/токсичное вещество)
  * Тип теплообменника (кожухотрубный/пластинчатый/спиральный)
  * Площадь теплообмена (м²)
  * Рабочее давление в трубном пространстве (МПа)
  * Рабочее давление в межтрубном пространстве (МПа)
  * Рабочая температура в трубном пространстве (°C)
  * Рабочая температура в межтрубном пространстве (°C)
  * Расход веществ (м³/ч)
  * Материал теплообменных поверхностей
  * Тип соединений
  * Наличие систем защиты

###### 2.1.2.6 Железнодорожные/автомобильные цистерны (Tank Car)
- Геометрия: полигональный объект
- Параметры:
  * Тип вещества (СУГ/жидкость/токсичное вещество)
  * Тип цистерны (железнодорожная/автомобильная)
  * Объем (м³)
  * Степень заполнения (%)
  * Рабочее давление (МПа)
  * Масса вещества (кг)
  * Геометрические размеры (длина, диаметр)
  * Толщина стенки (мм)
  * Материал цистерны
  * Тип теплоизоляции
  * Наличие защитного кожуха
  * Тип сливо-наливной арматуры
  * Наличие систем защиты

###### 2.1.2.7 Люди на открытых площадках (People)
- Геометрия: полигональный объект (зона пребывания)
- Параметры:
  * Количество людей
  * Плотность распределения (чел/м²)
  * Время пребывания в зоне
  * Тип деятельности
  * График работы
  * Защищенность (наличие СИЗ)

###### 2.1.2.8 Здания (Building)
- Геометрия: полигональный объект
- Параметры:
  * Тип здания (производственное/административное/складское)
  * Категория взрывопожарной опасности
  * Степень огнестойкости
  * Количество этажей
  * Площадь застройки (м²)
  * Строительный объем (м³)
  * Количество людей в здании
  * Наличие убежищ/укрытий
  * Материал стен
  * Тип вентиляции
- Хранение для каждого объекта:
  * Координаты (x, y)
  * Тип объекта
  * Название
  * Характеристики (площадь, количество людей, тип строения)
  * Дополнительные параметры в зависимости от типа
- Редактирование объектов:
  * Перемещение
  * Изменение размеров
  * Удаление
  * Редактирование свойств

##### 2.1.3. Расчетный модуль
- Расчет зон поражающих факторов:
  * Взрыв (избыточное давление)
  * Пожар (тепловое излучение)
  * Выброс токсичных веществ (концентрация)
- Учет параметров:
  * Метеоусловия
  * Характеристики опасных веществ
  * Параметры источника аварии
- Построение зон на плане:
  * Цветовая градация по степени воздействия
  * Легенда
  * Масштабная линейка

##### 2.1.4. Создание ситуационных планов
- Автоматическое построение зон поражения
- Нанесение путей эвакуации
- Размещение условных обозначений
- Добавление текстовых пояснений
- Экспорт в графические форматы

##### 2.1.5. Формирование отчетов
- Создание отчетов в форматах DOC/PDF
- Включение в отчет:
  * Исходные данные
  * Результаты расчетов
  * Ситуационные планы
  * Списки объектов
  * Выводы и рекомендации

#### 2.2. Требования к надежности
- Автосохранение данных каждые 5 минут
- Создание резервных копий проекта
- Проверка целостности данных при загрузке
- Логирование действий пользователя

#### 2.3. Требования к интерфейсу
- Главное окно с областью отображения плана
- Панель инструментов для работы с объектами
- Древовидная структура объектов
- Окно свойств выбранного объекта
- Модальные окна для расчетов
- Строка состояния

### 3. Технические решения
#### 3.1. Технологии разработки
- Язык программирования: Python 3.10+
- GUI фреймворк: PyQt6
- База данных: SQLite
- Дополнительные библиотеки:
  * NumPy (расчеты)
  * Matplotlib (построение графиков)
  * Pillow (работа с изображениями)
  * ReportLab (генерация PDF)
  * python-docx (работа с DOC)

#### 3.2. Структура программы
##### 3.2.1. Модули
- main.py - точка входа
- gui/
  * main_window.py - главное окно
  * toolbars.py - панели инструментов
  * dialogs/ - модальные окна
- core/
  * project.py - управление проектом
  * objects.py - классы объектов
  * calculations.py - расчетные модули
- database/
  * db_manager.py - работа с БД
  * models.py - модели данных
- utils/
  * config.py - настройки
  * logger.py - логирование
  * exporters.py - экспорт данных

##### 3.2.2. База данных
Таблицы:

###### 3.2.2.1 Substances (Вещества)
- id (INTEGER PRIMARY KEY)
- sub_name (TEXT) - название вещества
- density_liquid (REAL) - плотность жидкости, кг/м³
- molecular_weight (REAL) - молярная масса, кг/моль
- boiling_temperature_liquid (REAL) - температура кипения, °C
- heat_evaporation_liquid (REAL) - теплота испарения, Дж/кг
- adiabatic (REAL) - показатель адиабаты
- heat_capacity_liquid (REAL) - теплоемкость жидкости, Дж/кг/°C
- class_substance (INTEGER) - класс взрывоопасности (1-4)
- heat_of_combustion (REAL) - теплота сгорания, кДж/кг
- sigma (INTEGER) - тип смеси (4-парогазовая, 7-газовая)
- energy_level (INTEGER) - тип ТВС (1-легкая, 2-тяжелая)
- flash_point (REAL) - температура вспышки, °C
- auto_ignition_temp (REAL) - температура самовоспламенения, °C
- lower_concentration_limit (REAL) - НКПР, % об.
- upper_concentration_limit (REAL) - ВКПР, % об.
- threshold_toxic_dose (REAL) - пороговая токсодоза, мг*мин/л
- lethal_toxic_dose (REAL) - смертельная токсодоза, мг*мин/л
- sub_type (INTEGER) - тип вещества:
  * 0 - ЛВЖ
  * 1 - ЛВЖ токсичная
  * 2 - СУГ
  * 3 - СУГ токсичный
  * 4 - ГЖ
  * 5 - ГГ
  * 6 - ГГ токсичный
  * 7 - Химически опасное вещество (ХОВ) без токсичного облака

###### 3.2.2.2 Projects (Проекты)
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- description (TEXT)
- creation_date (DATETIME)
- last_modified (DATETIME)

###### 3.2.2.3 Objects (Объекты)
- id (INTEGER PRIMARY KEY)
- project_id (INTEGER, FOREIGN KEY)
- type (TEXT)
- parameters (JSON)
- geometry (JSON)
- coordinates (JSON)

###### 3.2.2.4 Calculations (Расчеты)
- id (INTEGER PRIMARY KEY)
- project_id (INTEGER, FOREIGN KEY)
- object_id (INTEGER, FOREIGN KEY)
- calculation_type (TEXT)
- parameters (JSON)
- results (JSON)
- date (DATETIME)

###### 3.2.2.5 Reports (Отчеты)
- id (INTEGER PRIMARY KEY)
- project_id (INTEGER, FOREIGN KEY)
- type (TEXT)
- content (JSON)
- creation_date (DATETIME)

###### 3.2.2.6 Settings (Настройки)
- id (INTEGER PRIMARY KEY)
- key (TEXT)
- value (TEXT)
- description (TEXT)

### 4. Этапы разработки
1. Проектирование архитектуры (2 недели)
2. Разработка базового интерфейса (3 недели)
3. Реализация работы с объектами (4 недели)
4. Создание расчетного модуля (4 недели)
5. Разработка модуля отчетов (2 недели)
6. Тестирование и отладка (3 недели)
7. Документирование (2 недели)

Общий срок разработки: 20 недель

### 5. Требования к документации
- Руководство пользователя
- Руководство администратора
- Техническая документация
- Документация по API

### 6. Требования к тестированию
- Модульное тестирование
- Интеграционное тестирование
- Нагрузочное тестирование
- Тестирование пользовательского интерфейса
