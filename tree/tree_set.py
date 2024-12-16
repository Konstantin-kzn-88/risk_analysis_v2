# Модуль работы с деревьями событий
# @version: 1.0
# @date: 2024-08-29
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# @author: Kuznetsov Konstantin, kuznetsov@yandex.ru
# (C) 2024
# ------------------------------------------------------------------------------------


# Типы веществ (sub_type)
# 0: ЛВЖ (Легковоспламеняющаяся жидкость)
# 1: ЛВЖ токсичная
# 2: СУГ (Сжиженный углеводородный газ)
# 3: СУГ токсичный
# 4: ГЖ (Горючая жидкость)
# 5: ГГ (Горючий газ)
# 6: ГГ токсичный
# 7: Химически опасное вещество (ХОВ) без токсичного облака

# Структура: equipment_type -> substance_type -> (partial_depressurization, full_depressurization)
# Где partial_depressurization и full_depressurization - кортежи ((...вероятность событий...)(...методы расчета...))

equipment_substance_mapping = {
    'Technological_devices': {
        0: {  # ЛВЖ
            'partial': ((0.04, 0.16, 0.04, 0.152, 0.608), ('liguid_jet', 'no_factors','gas_jet','flash', 'no_factors')),
            'full': ((0.05, 0.19, 0.76), ('strait_fire', 'explosion', 'no_factors')),
        },
        1: {  # ЛВЖ токсичная
            'partial': ((0.04, 0.16, 0.04, 0.152, 0.608), ('liguid_jet', 'toxi','gas_jet','flash', 'toxi')),
            'full': ((0.05, 0.19, 0.76), ('strait_fire', 'explosion', 'toxi')),
        },
        2: {  # СУГ
            'partial': ((0.04, 0.16, 0.04, 0.152, 0.608), ('liguid_jet', 'no_factors','gas_jet','flash', 'no_factors')),
            'full': ((0.05, 0.19, 0.76), ('fire_ball', 'explosion', 'no_factors')),
        },
        3: {  # СУГ токсичный
            'partial': ((0.04, 0.16, 0.04, 0.152, 0.608), ('liguid_jet', 'toxi','gas_jet','flash', 'toxi')),
            'full': ((0.05, 0.19, 0.76), ('fire_ball', 'explosion', 'toxi')),
        },
        4: {  # ГЖ
            'partial': ((0.1, 0.045, 0.855), ('strait_fire', 'strait_fire', 'no_factors')),
            'full': ((0.1, 0.045, 0.855), ('strait_fire', 'strait_fire', 'no_factors')),
        },
        5: {  # ГГ
            'partial': ((0.0350, 0.0083, 0.0264, 0.9303), ('gas_jet', 'explosion','flash', 'no_factors')),
            'full': ((0.2, 0.1152, 0.0768, 0.6080), ('fire_ball', 'explosion','flash', 'no_factors')),
        },
        6: {  # ГГ токсичный
            'partial': ((0.0350, 0.0083, 0.0264, 0.9303), ('gas_jet', 'explosion','flash', 'toxi')),
            'full': ((0.2, 0.1152, 0.0768, 0.6080), ('fire_ball', 'explosion','flash', 'toxi')),
        },
        7: {  # ХОВ
            'partial': ((1),('toxi_spill')),
            'full': ((1),('toxi_spill'))
        }
    },
    'Tank': {
        0: {    # ЛВЖ
            'partial': ((0.1, 0.0450, 0.8550),('strait_fire', 'flash','no_factors')),
            'full': ((0.1, 0.18, 0.72),('strait_fire', 'explosion','no_factors')),
        },
        1: {  # ЛВЖ токсичная
            'partial': ((0.1, 0.0450, 0.8550),('strait_fire', 'flash','toxi')),
            'full': ((0.1, 0.18, 0.72),('strait_fire', 'explosion','toxi')),
        },
        2: {  # СУГ (не может хранится в резервуаре без давления)
            'partial': None,
            'full': None
        },
        3: {  # СУГ токсичный
            'partial': None,
            'full': None
        },
        4: {  # ГЖ
            'partial': ((0.05, 0.0475, 0.9025), ('strait_fire', 'strait_fire', 'no_factors')),
            'full': ((0.05, 0.0475, 0.9025), ('strait_fire', 'strait_fire', 'no_factors')),
        },
        5: {  # ГГ
            'partial': None,
            'full': None
        },
        6: {  # ГГ токсичный
            'partial': None,
            'full': None
        },
        7: {  # ХОВ
            'partial': ((1),('toxi_spill')),
            'full': ((1),('toxi_spill'))
        }
    },
    'Pump': {
        0: {    # ЛВЖ
            'partial': ((0.0350, 0.0333, 0.6318), ('strait_fire', 'flash','no_factors')),
            'full': ((0.015, 0.0143, 0.2708), ('liguid_jet', 'explosion', 'no_factors')),
        },
        1: {    # ЛВЖ токсичная
            'partial': ((0.0350, 0.0333, 0.6318), ('strait_fire', 'flash','toxi')),
            'full': ((0.015, 0.0143, 0.2708), ('liguid_jet', 'explosion', 'toxi')),
        },
        2: {    # СУГ
            'partial': ((0.0350, 0.0333, 0.6318), ('strait_fire', 'flash','no_factors')),
            'full': ((0.015, 0.0143, 0.2708), ('liguid_jet', 'explosion', 'no_factors')),
        },
        3: {    # СУГ токсичный
            'partial': ((0.0350, 0.0333, 0.6318), ('strait_fire', 'flash','toxi')),
            'full': ((0.015, 0.0143, 0.2708), ('liguid_jet', 'explosion', 'toxi')),
        },
        4: {    # ГЖ
            'partial': ((0.0350, 0.0333, 0.6318), ('strait_fire', 'strait_fire','no_factors')),
            'full': ((0.015, 0.0143, 0.2708), ('strait_fire', 'strait_fire', 'no_factors')),
        },
        5: {  # ГГ
            'partial': None,
            'full': None
        },
        6: {  # ГГ токсичный
            'partial': None,
            'full': None
        },
        7: {
            'partial': ((1),('toxi_spill')),
            'full': ((1),('toxi_spill'))
        }
    },
    'Truck_tank': {
        0: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        1: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        2: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        3: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        4: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        5: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        6: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        7: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        }
    },
    'Pipeline': {
        0: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        1: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        2: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        3: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        4: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        5: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        6: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        7: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        }
    },
    'Compressor': {
        5: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        6: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        },
        7: {
            'partial': (1, 2, 3, 4),
            'full': (5, 6, 7, 8)
        }
    }
}


