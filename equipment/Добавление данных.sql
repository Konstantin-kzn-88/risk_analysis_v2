-- Заполнение таблицы Pipeline_failure_rate
INSERT INTO Pipeline_failure_rate (diameter_category, type_id, rate_value) VALUES
('Менее 75 мм', 1, 5.7E-7),
('Менее 75 мм', 2, 2.4E-6),
('От 75 до 150 мм', 1, 2.7E-7),
('От 75 до 150 мм', 2, 1.1E-6),
('Более 150 мм', 1, 8.8E-8),
('Более 150 мм', 2, 3.7E-7);

-- Заполнение таблицы Pump_failure_rate
INSERT INTO Pump_failure_rate (pump_type, type_id, rate_value) VALUES
('Центробежные герметичные', 1, 1.0E-4),
('Центробежные герметичные', 2, 5.0E-4),
('Центробежные с уплотнениями', 1, 5.0E-4),
('Центробежные с уплотнениями', 2, 2.5E-3),
('Поршневые', 1, 5.0E-4),
('Поршневые', 2, 2.5E-3);

-- Заполнение таблицы Device_failure_rate
INSERT INTO Device_failure_rate (device_type, type_id, rate_value) VALUES
('Сосуды хранения под давлением', 1, 5.7E-7),
('Сосуды хранения под давлением', 2, 1.0E-4),
('Технологические аппараты', 1, 1.0E-4),
('Технологические аппараты', 2, 5.0E-4),
('Химические реакторы', 1, 1.0E-4),
('Химические реакторы', 2, 5.0E-4);

-- Заполнение таблицы Tank_failure_rate
INSERT INTO Tank_failure_rate (tank_type, type_id, rate_value) VALUES
('Одностенный', 1, 1.0E-4),
('Одностенный', 2, 5.0E-4),
('С внешней защитной оболочкой', 1, 5.7E-7),
('С внешней защитной оболочкой', 2, 5.0E-4),
('С двойной оболочкой', 1, 2.5E-5),
('С двойной оболочкой', 2, 5.0E-4),
('Полной герметизации', 1, 1.0E-5),
('Полной герметизации', 2, 5.0E-4);

-- Заполнение таблицы Truck_tank_failure_rate
INSERT INTO Truck_tank_failure_rate (pressure_type, type_id, rate_value) VALUES
('Под избыточным давлением', 1, 5.0E-7),
('Под избыточным давлением', 2, 5.0E-7),
('При атмосферном давлении', 1, 1.0E-4),
('При атмосферном давлении', 2, 5.0E-7);

-- Создание оборудования с реалистичными параметрами

-- Pipeline
INSERT INTO Pipeline (pipeline_name, diameter_category, length_meters, diameter_pipeline, flow, time_out, pressure, temperature, component_enterprise, sub_id, coordinate) VALUES
('Трубопровод-1', 'Менее 75 мм', 150.5, 50.0, 2.5, 1.5, 1.5, 25.0, 'Установка переработки', 1, '55.751244, 37.618423'),
('Трубопровод-2', 'От 75 до 150 мм', 200.0, 100.0, 5.0, 2.0, 2.0, 30.0, 'Установка синтеза', 2, '55.752144, 37.619523'),
('Трубопровод-3', 'Более 150 мм', 300.0, 200.0, 10.0, 2.5, 2.5, 35.0, 'Установка хранения', 3, '55.753044, 37.620623'),
('Трубопровод-4', 'От 75 до 150 мм', 250.0, 125.0, 7.5, 2.0, 2.2, 32.0, 'Установка отгрузки', 4, '55.754944, 37.621723');

-- Pump
INSERT INTO Pump (pump_name, pump_type, volume, flow, time_out, pressure, temperature, component_enterprise, sub_id, coordinate) VALUES
('Насос-1', 'Центробежные герметичные', 0.5, 10.0, 0.5, 2.0, 30.0, 'Насосная станция 1', 1, '55.755844, 37.622823'),
('Насос-2', 'Центробежные с уплотнениями', 0.8, 15.0, 0.8, 2.5, 35.0, 'Насосная станция 2', 2, '55.756744, 37.623923'),
('Насос-3', 'Поршневые', 1.2, 20.0, 1.0, 3.0, 40.0, 'Насосная станция 3', 3, '55.757644, 37.625023'),
('Насос-4', 'Центробежные герметичные', 0.6, 12.0, 0.6, 2.2, 32.0, 'Насосная станция 4', 4, '55.758544, 37.626123');

-- Technological_devices
INSERT INTO Technological_devices (device_name, device_type, volume, degree_filling, pressure, temperature, component_enterprise, spill_square, sub_id, coordinate) VALUES
('Аппарат-1', 'Сосуды хранения под давлением', 10.0, 0.85, 1.5, 25.0, 'Установка 1', 50.0, 1, '55.759444, 37.627223'),
('Аппарат-2', 'Технологические аппараты', 15.0, 0.80, 2.0, 30.0, 'Установка 2', 75.0, 2, '55.760344, 37.628323'),
('Аппарат-3', 'Химические реакторы', 20.0, 0.75, 2.5, 35.0, 'Установка 3', 100.0, 3, '55.761244, 37.629423'),
('Аппарат-4', 'Технологические аппараты', 12.0, 0.82, 1.8, 28.0, 'Установка 4', 60.0, 4, '55.762144, 37.630523');

-- Tank
INSERT INTO Tank (tank_name, tank_type, volume, degree_filling, pressure, temperature, component_enterprise, spill_square, sub_id, coordinate) VALUES
('Резервуар-1', 'Одностенный', 1000.0, 0.85, 0.2, 25.0, 'Резервуарный парк 1', 200.0, 1, '55.763044, 37.631623'),
('Резервуар-2', 'С внешней защитной оболочкой', 2000.0, 0.80, 0.3, 30.0, 'Резервуарный парк 2', 300.0, 2, '55.763944, 37.632723'),
('Резервуар-3', 'С двойной оболочкой', 3000.0, 0.75, 0.4, 35.0, 'Резервуарный парк 3', 400.0, 3, '55.764844, 37.633823'),
('Резервуар-4', 'Полной герметизации', 1500.0, 0.82, 0.25, 28.0, 'Резервуарный парк 4', 250.0, 4, '55.765744, 37.634923');

-- Truck_tank
INSERT INTO Truck_tank (truck_tank_name, pressure_type, volume, degree_filling, pressure, temperature, component_enterprise, spill_square, sub_id, coordinate) VALUES
('Автоцистерна-1', 'Под избыточным давлением', 20.0, 0.85, 1.5, 25.0, 'Площадка налива 1', 40.0, 1, '55.766644, 37.636023'),
('Автоцистерна-2', 'При атмосферном давлении', 25.0, 0.80, 0.1, 30.0, 'Площадка налива 2', 50.0, 2, '55.767544, 37.637123'),
('Автоцистерна-3', 'Под избыточным давлением', 30.0, 0.75, 1.8, 35.0, 'Площадка налива 3', 60.0, 3, '55.768444, 37.638223'),
('Автоцистерна-4', 'При атмосферном давлении', 22.0, 0.82, 0.1, 28.0, 'Площадка налива 4', 45.0, 4, '55.769344, 37.639323');

-- Compressor
INSERT INTO Compressor (comp_name, comp_type, volume, flow, time_out, pressure, temperature, component_enterprise, sub_id, coordinate) VALUES
('Компрессор-1', 'Поршневой', 2.0, 100.0, 0.5, 10.0, 40.0, 'Компрессорная станция 1', 1, '55.770244, 37.640423'),
('Компрессор-2', 'Центробежный', 3.0, 150.0, 0.8, 12.0, 45.0, 'Компрессорная станция 2', 2, '55.771144, 37.641523'),
('Компрессор-3', 'Поршневой', 2.5, 120.0, 0.6, 11.0, 42.0, 'Компрессорная станция 3', 3, '55.772044, 37.642623'),
('Компрессор-4', 'Центробежный', 3.5, 180.0, 0.9, 13.0, 47.0, 'Компрессорная станция 4', 4, '55.772944, 37.643723');