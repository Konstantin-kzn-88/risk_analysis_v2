# Модуль работы с деревьями событий
# @version: 1.0
# @date: 2024-08-29
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# @author: Kuznetsov Konstantin, kuznetsov@yandex.ru
# (C) 2024
# ------------------------------------------------------------------------------------


class Tree:
    """Класс формирования вероятностей деревьев событий"""

    def __init__(self, sub_type: int, eq_type: int):
        self.sub_type = sub_type
        self.eq_type = eq_type

        self.data = {
            0: {  # ЛВЖ
                0: (0.05, 0.19, 0.76, 0.04, 0.16, 0.04, 0.152, 0.608, 1E-6, 1E-5),  # емк. под давлением
                1: (0.1, 0.18, 0.72, 0.1, 0.045, 0.855, 1E-5, 1E-4),  # РВС
                2: (0.015,0.01425,0.27075,0.035,0.03325,0.63175, 1E-5, 5E-5),  # насос
                3: (0.05, 0.19, 0.76, 0.04, 0.16, 0.04, 0.152, 0.608, 1E-5, 1E-4),  # технол.аппараты
                4: (0.05, 0.0475, 0.9025,0.05,0.0475,0.9025, 5E-7, 5E-7),  # цистерна
                10: (0.2, 0.04, 0.76, 0.2, 0.04, 0.76, 1E-6, 5E-6, 3E-7, 2E-6, 1E-7, 5E-7),  # труба ЛВЖ
                11: (0.2, 0.1152, 0.0768, 0.608, 0.035, 0.0083376, 0.0264024, 0.93026, 1E-6, 5E-6, 3E-7, 2E-6, 1E-7, 5E-7)  # труба ГГ
            },
            1: {  # ЛВЖ+токси
                0: (0.05, 0.19, 0.76, 0.04, 0.16, 0.04, 0.152, 0.608, 1E-6, 1E-5),  # емк. под давлением
                1: (0.1, 0.18, 0.72, 0.1, 0.045, 0.855, 1E-5, 1E-4),  # РВС
                2: (0.015, 0.01425, 0.27075, 0.035, 0.03325, 0.63175, 1E-5, 5E-5),  # насос
                3: (0.05, 0.19, 0.76, 0.04, 0.16, 0.04, 0.152, 0.608, 1E-5, 1E-4),  # технол.аппараты
                4: (0.05, 0.0475, 0.9025, 0.05, 0.0475, 0.9025, 5E-7, 5E-7),  # цистерна
                10: (0.2, 0.04, 0.76, 0.2, 0.04, 0.76, 1E-6, 5E-6, 3E-7, 2E-6, 1E-7, 5E-7),  # труба ЛВЖ
                11: (0.2, 0.1152, 0.0768, 0.608, 0.035, 0.0083376, 0.0264024, 0.93026, 1E-6, 5E-6, 3E-7, 2E-6, 1E-7, 5E-7)  # труба ГГ
            }
        }

    def get_tree_set(self):
        return self.data[self.sub_type][self.eq_type]

if __name__ == '__main__':
    print(Tree(0,0).get_tree_set())



