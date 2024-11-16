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

        PD = (5e-09)* math.pow(spill_square, 3) - (3e-05)* math.pow(spill_square, 2) + 0.0808* spill_square - 0.1014

        return (LD, PD)


    def LD_PD_gas(self, mass_gas: float) -> tuple:
        """
        Расчет зон токсического поражения

        Parametrs:
        :@param spill_square площадь, м2;

        Return:
        :@return tuple(LD, PD)
        """
        if mass_gas < 20: mass_gas = 20

        LD = round(9.5409*math.log(mass_gas) - 23.086, 1)

        PD = round(79.485*math.log(mass_gas) - 226.21, 1)

        return (LD, PD)

if __name__ == '__main__':
    print(Toxi().LD_PD(10000))
