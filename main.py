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
from calc import calc_0_0

path_sub_db = str(Path(os.getcwd())) + '/substance/'  # путь к базе данных с веществом.
path_equip_db = str(Path(os.getcwd())) + '/equipment/equipment.db'  # путь к базе данных с оборудованием.

equipments = equipment_property.Equipment_DB(path_equip_db).get_all_equipment_table()
# equipments = equipment_property.Equipment_DB(path_equip_db).table()

# ['id', 'id_equipment', 'name_equipment_or_pipeline', 'part_opo', 'scnario', 'scnario_value', 'mass_all', 'mass_pf', 'q_10', 'q_7', 'q_4', 'q_1', 'p_100', 'p_70', 'p_28', 'p_14', 'p_2', 'Lf', 'Df', 'Rnkpr', 'Rvsp', 'LPt', 'PPt', 'Q600', 'Q320', 'Q220', 'Q120', 'St', 'direct_losses', 'localization', 'socio', 'ecolog', 'indirect', 'dead', 'injured', 'collective_dead', 'collective_injured', 'math_expectation']
scenario_num = 1
#
for equipment in equipments:
    if equipment[-1] == 0:  # емк.под давлением
        if equipment[-2] == 0:  # ЛВЖ
            data = calc_0_0.Result(scenario_num, equipment).calculation()
            for i in data:
                equipment_property.Equipment_DB(path_equip_db).add_result(i)
            scenario_num += len(data) - 1

if __name__ == '__main__':
    print(equipments)
