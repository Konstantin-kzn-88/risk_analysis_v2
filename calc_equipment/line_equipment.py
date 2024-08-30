# ------------------------------------------------------------------------------------
# Класс предназначен для обработки технологических объектов
#
# ------------------------------------------------------------------------------------
# @author: Kuznetsov Konstantin, kuznetsov@yandex.ru
# (C) 2024
# ------------------------------------------------------------------------------------

import math

class Pipeline:
    """Класс предназначен для обработки технологических объектов"""
    def __init__(self, name: str, cloud: float,
                 wind_speed: float,
                 is_night: float, is_urban_area: float, ejection_height: float,
                 gas_temperature: float, gas_weight: float, gas_flow: float, closing_time: float,
                 molecular_weight: float):
        """
        :param name - наименование трубопровода, строка
        :param cloud - облачность от 0 до 8, -
        :param wind_speed - скорость ветра, м/с
        :param is_night - ночное время суток, -
        :param is_urban_area - городская застройка, -
        :param ejection_height - высота выброса, м
        :param gas_temperature - температура газа, град.С
        :param gas_weight - масса газа, кг
        :param gas_flow - расход газа, кг/с
        :param closing_time - время отсечения, с
        :param molecular_weight - молекулярная масса, кг/кмоль (метан 18)

        """
        self.ambient_temperature = ambient_temperature
        self.cloud = cloud if cloud in [i for i in range(0, 9)] else 0
        self.wind_speed = wind_speed
        self.is_night = is_night if is_night in (0, 1) else 0
        self.is_urban_area = is_urban_area if is_urban_area in (0, 1) else 0
        self.ejection_height = ejection_height
        self.gas_temperature = gas_temperature
        self.gas_weight = gas_weight
        self.gas_flow = gas_flow
        self.closing_time = closing_time
        self.molecular_weight = molecular_weight


if __name__ == '__main__':
    print('PyCharm')