# ------------------------------------------------------------------------------------
# Программа для разработки разделов по промышленной безопасности (ДПБ, ГОЧС, ПБ).
# @version: 2.0
# @date: 2024-08-29
#
# ------------------------------------------------------------------------------------
# @author: Kuznetsov Konstantin, kuznetsov@yandex.ru
# (C) 2024
# ------------------------------------------------------------------------------------

import substance
import os
from pathlib import Path

from substance import sub_property
from equipment import equipment_property
from calc import calc_0_0, calc_0_1
from tree import tree_set

path_sub_db = str(Path(os.getcwd())) + '/substance/'  # путь к базе данных с веществом.
path_equip_db = str(Path(os.getcwd())) + '/equipment/equipment.db'  # путь к базе данных с оборудованием.

equipments = equipment_property.Equipment_DB(path_equip_db).get_all_equipment_table()

scenario_num = 1

# Очистить таблицу с результатами расчета
equipment_property.Equipment_DB(path_equip_db).clear_equipment_result()
# Для каждого оборудования проведем расчет и результат запишем в Equipment_table
for equipment in equipments:
    sub = sub_property.Work_DB().find_from_db_whith_id(equipment[-2], path_sub_db)
    if equipment[-1] == 0:  # емк.под давлением
        if sub[-1] == 0:  # ЛВЖ
            tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
            data = calc_0_0.Result(scenario_num, equipment, sub, tree).calculation()
            for i in data:
                equipment_property.Equipment_DB(path_equip_db).add_result(i)
            scenario_num += len(data)
        # elif sub[-1] == 1:  # ЛВЖ + токси
        #     data = calc_0_1.Result(scenario_num, equipment, sub).calculation()
        #     for i in data:
        #         equipment_property.Equipment_DB(path_equip_db).add_result(i)
        #     scenario_num += len(data)

if __name__ == '__main__':
    print(equipments)
