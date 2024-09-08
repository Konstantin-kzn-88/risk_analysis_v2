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

sub = input('Введите вещество: ')
square = input('Введите площадь: ')
temp = int(input('Введите температуру: '))

path_sub_db = str(Path(os.getcwd())) + '/substance/' # путь к базе данных с веществом.

sub_property = get_sub_property.get_in_db(name_sub=sub, db_path=path_sub_db)

steam_pressure = get_sub_property.calc_steam_pressure(sub_property=sub_property, temperature=temp)

if __name__ == '__main__':
    print(steam_pressure)
