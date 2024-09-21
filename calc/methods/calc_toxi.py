# -----------------------------------------------------------
# Класс предназначен для токсического поражения
#
# (C) 2024 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------
import math


class Toxi:

    def LD_PD(self, spill_square: float) -> tuple:
        """
        Расчет зон токсического поражения нефти

        Parametrs:
        :@param spill_square площадь, м2;

        Return:
        :@return tuple(LD, PD)
        """

        LD = round(0.0088 * spill_square + 0.8056, 1)
        PD = round((-1e-12) * math.pow(spill_square, 5) + (3e-09) * math.pow(spill_square, 4) - \
                   (3e-06) * math.pow(spill_square, 3) + \
                   0.0012 * math.pow(spill_square, 2) - 0.1529 * spill_square + 16.167, 1)

        return (LD, PD)


# 100	2	10
# 200	3	14
# 300	3	21
# 400	4	26
# 500	5	32
# 600	6	37
# 700	7	43
# 800	8	51
# 900	9	55


if __name__ == '__main__':
    print(Toxi().LD_PD(0.2*20))
