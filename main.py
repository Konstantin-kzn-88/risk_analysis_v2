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
from equipment import db_CRUD_tank


path_sub_db = str(Path(os.getcwd())) + '/substance/substances.db'  # путь к базе данных с веществом.
path_equip_db = str(Path(os.getcwd())) + '/equipment/db_eq.db'  # путь к базе данных с оборудованием.



# Получим перечень оборудования
equipments = db_CRUD_tank.TankCRUD(path_equip_db).list_all()

for equipment in equipments:
    # получим вещество
    sub = sub_property.SubstanceDatabase(path_sub_db).get_substance(equipment['sub_id'])
    print('sub: ',sub)


if __name__ == '__main__':
    # pass
    print(equipments)
