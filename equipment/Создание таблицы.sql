-- Создание справочной таблицы для типов разгерметизации
CREATE TABLE Depressurization_type (
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name VARCHAR(50) NOT NULL
);

-- Заполнение справочника типов разгерметизации
INSERT INTO Depressurization_type (type_name) VALUES 
    ('Полное разрушение'),
    ('Частичное разрушение');

-- Создание таблицы трубопроводов
CREATE TABLE Pipeline (
    pipeline_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_name VARCHAR(100) NOT NULL,
    diameter_category VARCHAR(20) NOT NULL, -- Менее 75 мм, От 75 до 150 мм, Более 150 мм
    length_meters REAL, -- Длина в метрах для расчета частоты
    diameter_pipeline REAL,
    flow REAL,
    time_out REAL,
    pressure REAL,
    temperature REAL,
    component_enterprise VARCHAR(100),
    sub_id INTEGER NOT NULL DEFAULT 0,
    coordinate VARCHAR(300)
);

-- Создание таблицы частот разгерметизации трубопроводов
CREATE TABLE Pipeline_failure_rate (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    diameter_category VARCHAR(20) NOT NULL,
    type_id INTEGER,
    rate_value REAL NOT NULL, -- Частота разгерметизации, 1/(год·м)
    UNIQUE (diameter_category, type_id),
    FOREIGN KEY (type_id) REFERENCES Depressurization_type(type_id)
);

-- Создание таблицы насосов
CREATE TABLE Pump (
    pump_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pump_name VARCHAR(100) NOT NULL,
    pump_type VARCHAR(50) NOT NULL, -- Центробежные герметичные, Центробежные с уплотнениями, Поршневые
    volume REAL,
    flow REAL,
    time_out REAL,
    pressure REAL,
    temperature REAL,
    component_enterprise VARCHAR(100),
    sub_id INTEGER NOT NULL DEFAULT 0,
    coordinate VARCHAR(300)
);

-- Создание таблицы частот разгерметизации насосов
CREATE TABLE Pump_failure_rate (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pump_type VARCHAR(50) NOT NULL,
    type_id INTEGER,
    rate_value REAL NOT NULL, -- Частота разгерметизации, 1/год
    UNIQUE (pump_type, type_id),
    FOREIGN KEY (type_id) REFERENCES Depressurization_type(type_id)
);

-- Создание таблицы технологических устройств
CREATE TABLE Technological_devices (
    device_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_name VARCHAR(100) NOT NULL,
    device_type VARCHAR(100) NOT NULL, -- Сосуды хранения под давлением, Технологические аппараты, Химические реакторы
    volume REAL,
    degree_filling REAL,
    pressure REAL,
    temperature REAL,
    component_enterprise VARCHAR(100),
    spill_square REAL,
    sub_id INTEGER NOT NULL DEFAULT 0,
    coordinate VARCHAR(300)
);

-- Создание таблицы частот разгерметизации технологических устройств
CREATE TABLE Device_failure_rate (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_type VARCHAR(100) NOT NULL,
    type_id INTEGER,
    rate_value REAL NOT NULL, -- Частота разгерметизации, 1/год
    UNIQUE (device_type, type_id),
    FOREIGN KEY (type_id) REFERENCES Depressurization_type(type_id)
);

-- Создание таблицы стационарных резервуаров
CREATE TABLE Tank (
    tank_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tank_name VARCHAR(100) NOT NULL,
    tank_type VARCHAR(100) NOT NULL, -- Одностенный, С внешней защитной оболочкой, С двойной оболочкой и т.д.
    volume REAL,
    degree_filling REAL,
    pressure REAL,
    temperature REAL,
    component_enterprise VARCHAR(100),
    spill_square REAL,
    sub_id INTEGER NOT NULL DEFAULT 0,
    coordinate VARCHAR(300)
);

-- Создание таблицы частот разгерметизации резервуаров
CREATE TABLE Tank_failure_rate (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tank_type VARCHAR(100) NOT NULL,
    type_id INTEGER,
    rate_value REAL NOT NULL, -- Частота разгерметизации, 1/год
    UNIQUE (tank_type, type_id),
    FOREIGN KEY (type_id) REFERENCES Depressurization_type(type_id)
);

-- Создание таблицы автоцистерн
CREATE TABLE Truck_tank (
    truck_tank_id INTEGER PRIMARY KEY AUTOINCREMENT,
    truck_tank_name VARCHAR(100) NOT NULL,
    pressure_type VARCHAR(50) NOT NULL, -- Под избыточным давлением, При атмосферном давлении
    volume REAL,
    degree_filling REAL,
    pressure REAL,
    temperature REAL,
    component_enterprise VARCHAR(100),
    spill_square REAL,
    sub_id INTEGER NOT NULL DEFAULT 0,
    coordinate VARCHAR(300)
);

-- Создание таблицы частот разгерметизации автоцистерн
CREATE TABLE Truck_tank_failure_rate (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pressure_type VARCHAR(50) NOT NULL,
    type_id INTEGER,
    rate_value REAL NOT NULL, -- Частота разгерметизации, 1/год
    UNIQUE (pressure_type, type_id),
    FOREIGN KEY (type_id) REFERENCES Depressurization_type(type_id)
);

-- Создание таблицы компрессоров
CREATE TABLE Compressor (
    comp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    comp_name VARCHAR(100) NOT NULL,
    comp_type VARCHAR(50) NOT NULL,
    volume REAL,
    flow REAL,
    time_out REAL,
    pressure REAL,
    temperature REAL,
    component_enterprise VARCHAR(100),
    sub_id INTEGER NOT NULL,
    coordinate VARCHAR(300)
);

-- Создание таблицы частот разгерметизации компрессоров
CREATE TABLE Comp_failure_rate (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    comp_type VARCHAR(50) NOT NULL,
    type_id INTEGER,
    rate_value REAL NOT NULL, -- Частота разгерметизации, 1/год
    UNIQUE (comp_type, type_id),
    FOREIGN KEY (type_id) REFERENCES Depressurization_type(type_id)
);