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
from calc import calc_1_0, calc_1_1
from calc import calc_2_0, calc_2_1
from calc import calc_3_0, calc_3_1
from calc import calc_4_0, calc_4_1
from calc import calc_10_0, calc_10_1
from calc import calc_11_5, calc_11_6
from chart import fn_fg
from tree import tree_set

path_sub_db = str(Path(os.getcwd())) + '/substance/'  # путь к базе данных с веществом.
path_equip_db = str(Path(os.getcwd())) + '/equipment/equipment.db'  # путь к базе данных с оборудованием.



scenario_num = 1

# Получим перечень оборудования
equipments = equipment_property.Equipment_DB(path_equip_db).get_all_equipment_table()
# Получим перечень трубопроводов
pipelines = equipment_property.Equipment_DB(path_equip_db).get_all_equipment_pipeline_table()
# Очистить таблицу с результатами расчета
equipment_property.Equipment_DB(path_equip_db).clear_equipment_result()

# Для каждого оборудования проведем расчет и результат запишем в Equipment_table
for equipment in equipments:
    sub = sub_property.Work_DB().find_from_db_whith_id(equipment[-2], path_sub_db)

    # if equipment[-1] == 0:  # емк.под давлением
    #     if sub[-1] == 0:  # ЛВЖ
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_0_0.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)
    #     elif sub[-1] == 1:  # ЛВЖ+токси
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_0_1.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)
    #
    # elif equipment[-1] == 1:  # РВС
    #     if sub[-1] == 0:  # ЛВЖ
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_1_0.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)
    #
    #     elif sub[-1] == 1:  # ЛВЖ+токси
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_1_1.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)
    #
    # elif equipment[-1] == 2:  # насос
    #     if sub[-1] == 0:  # ЛВЖ
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_2_0.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)
    #
    #     elif sub[-1] == 1:  # ЛВЖ+токси
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_2_1.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)

    # if equipment[-1] == 3:  # технологические аппараты elif
    #     if sub[-1] == 0:  # ЛВЖ
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_3_0.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)
    #     elif sub[-1] == 1:  # ЛВЖ+токси
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_3_1.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)

    # if equipment[-1] == 4:  # цистерны elif
    #     if sub[-1] == 0:  # ЛВЖ
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_4_0.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)
    #     elif sub[-1] == 1:  # ЛВЖ+токси
    #         tree = tree_set.Tree(sub[-1], equipment[-1]).get_tree_set()
    #         data = calc_4_1.Result(scenario_num, equipment, sub, tree).calculation()
    #         for i in data:
    #             equipment_property.Equipment_DB(path_equip_db).add_result(i)
    #         scenario_num += len(data)
    pass


# Для каждого трубопровода проведем расчет и результат запишем в Equipment_pipeline_table
for pipeline in pipelines:
    sub = sub_property.Work_DB().find_from_db_whith_id(pipeline[-2], path_sub_db)

    # if pipeline[-1] == 10:  # трубопровод
        # if sub[-1] == 0:  # ЛВЖ
        #     tree = tree_set.Tree(sub[-1], pipeline[-1]).get_tree_set()
        #     data = calc_10_0.Result(scenario_num, pipeline, sub, tree).calculation()
        #     for i in data:
        #         equipment_property.Equipment_DB(path_equip_db).add_result(i)
        #     scenario_num += len(data)
        # elif sub[-1] == 1:  # ЛВЖ+токси
        #     tree = tree_set.Tree(sub[-1], pipeline[-1]).get_tree_set()
        #     data = calc_10_1.Result(scenario_num, pipeline, sub, tree).calculation()
        #     for i in data:
        #         equipment_property.Equipment_DB(path_equip_db).add_result(i)
        #     scenario_num += len(data)
    if pipeline[-1] == 11:  # трубопровод
        if sub[-1] == 5:  # ГГ
            tree = tree_set.Tree(sub[-1], pipeline[-1]).get_tree_set()
            data = calc_11_5.Result(scenario_num, pipeline, sub, tree).calculation()
            for i in data:
                equipment_property.Equipment_DB(path_equip_db).add_result(i)
            scenario_num += len(data)
        elif sub[-1] == 6:  # ГГ+токси
            tree = tree_set.Tree(sub[-1], pipeline[-1]).get_tree_set()
            data = calc_11_6.Result(scenario_num, pipeline, sub, tree).calculation()
            for i in data:
                equipment_property.Equipment_DB(path_equip_db).add_result(i)
            scenario_num += len(data)



# Построение FN и  FG диаграмм
res = equipment_property.Equipment_DB(path_equip_db).get_equipment_result_table()
_ = fn_fg.FN_FG_chart(res).fn_chart()
_ = fn_fg.FN_FG_chart(res).fg_chart()

if __name__ == '__main__':
    pass
    # print(equipments)
