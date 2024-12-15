-- Удаление таблиц с частотами отказов (сначала, так как они имеют внешние ключи)
DROP TABLE IF EXISTS Pipeline_failure_rate;
DROP TABLE IF EXISTS Pump_failure_rate;
DROP TABLE IF EXISTS Device_failure_rate;
DROP TABLE IF EXISTS Tank_failure_rate;
DROP TABLE IF EXISTS Truck_tank_failure_rate;
DROP TABLE IF EXISTS Comp_failure_rate;

-- Удаление основных таблиц оборудования
DROP TABLE IF EXISTS Pipeline;
DROP TABLE IF EXISTS Pump;
DROP TABLE IF EXISTS Technological_devices;
DROP TABLE IF EXISTS Tank;
DROP TABLE IF EXISTS Truck_tank;
DROP TABLE IF EXISTS Compressor;

-- Удаление справочной таблицы типов разгерметизации (последней, так как на неё ссылаются другие таблицы)
DROP TABLE IF EXISTS Depressurization_type;