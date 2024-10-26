from .methods import calc_strait_fire
from .methods import calc_damage
from .methods import calc_evaporation
from .methods import calc_tvs_explosion
from .methods import calc_lower_concentration
from .methods import calc_toxi
import math

# from
M_SG = 0.06  # удельная массовая скорость выгорания
WIND = 1  # скорость ветра
KG_TO_T = 0.001
KM_TO_M = 1000
KMOLE_TO_MOLE = 0.001
MM_TO_M = 0.001
MOLE_TO_KMOLE = 1000
PART_TO_EXPLOSION = 0.1
T_TO_KG = 1000
PART_FULL_DAMAGE = 0.5
PART_NOFULL_DAMAGE = 0.15
PART_ECOLOG = 0.125
SPILL_COEF = 20  # коэффициент пролива на грунт, м-1


class Result:
    def __init__(self, scenario_num, pipeline, sub, tree):
        self.pipeline = pipeline
        self.scenario_num = scenario_num
        self.sub = sub
        self.tree = tree

    def _volume_pipe(self, diametr, lenght):
        '''
        Функция вычисленя объема (м3) трубопровода
        diametr - мм, lenght - км
        '''
        return math.pi * (math.pow(diametr * MM_TO_M, 2) / 4) * lenght * KM_TO_M

    def _select_probability_pipe(self, diametr, lenght):
        '''
        Функция вычисленя вероятности трубопровода
        diametr - мм, lenght - м
        '''
        if diametr <= 75:
            return (self.tree[-6] * lenght * KM_TO_M, self.tree[-5] * lenght * KM_TO_M)
        elif diametr > 75 and diametr <= 150:
            return (self.tree[-4] * lenght * KM_TO_M, self.tree[-3] * lenght * KM_TO_M)
        elif diametr > 150:
            return (self.tree[-2] * lenght * KM_TO_M, self.tree[-1] * lenght * KM_TO_M)
        else:
            return (self.tree[-2] * lenght * KM_TO_M, self.tree[-1] * lenght * KM_TO_M)

    def _flow_in_pipe(self, diametr, pressure):
        '''
        Функция вычисленя аварийного расхода
        diametr - мм, pressure - МПа
        '''
        if diametr <= 100:
            return 153.19 * math.pow(pressure, 0.4976)
        else:
            return 251.93 * math.pow(pressure, 0.4967)

    def calculation(self):
        # 1. Полное разрушение
        _volume_pipe = self._volume_pipe(self.pipeline[3], self.pipeline[2])
        _part_volume = self.pipeline[9]
        _time_off = self.pipeline[9]
        _flow = self._flow_in_pipe(self.pipeline[3], self.pipeline[4])

        mass_all = (_volume_pipe * self.sub[2] + _time_off * _flow) * KG_TO_T  # объем*плотность вещества+расход*время

        # 1.1. Расчет пожара пролива (полное)
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[0] * self._select_probability_pipe(self.pipeline[3], self.pipeline[2])[-2]
        mass_pf = mass_all
        scnario_description = 'Разрыв трубопровода на сечение→ мгновенное воспламенение→ пожар пролива'
        general = [self.pipeline[0], self.pipeline[1], self.pipeline[10], scenario, scnario_value,
                   scnario_description,
                   mass_all, mass_pf]
        spill_fire = list(calc_strait_fire.Strait_fire().termal_class_zone(S_spill=mass_all * SPILL_COEF, m_sg=M_SG,
                                                                           mol_mass=self.sub[3], t_boiling=self.sub[4],
                                                                           wind_velocity=WIND))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = (self.pipeline[9] - 1) if (self.pipeline[9] - 1) > 0 else 0
        injured_man = (self.pipeline[10] - 1) if (self.pipeline[10] - 1) > 0 else 0

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=0, diametr_pipe=self.pipeline[3],
                                           lenght_pipe=self.pipeline[2],
                                           degree_damage=0.5, m_out_spill=0, m_in_spill=mass_all,
                                           S_spill=mass_all * SPILL_COEF).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_1 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 1.2. Расчет взрыва (полное)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[1] * self._select_probability_pipe(self.pipeline[3], self.pipeline[2])[-2]

        mass_gas = calc_evaporation.Evaporation(volume_equipment=mass_all, degree_filling=1,
                                                spill_square=mass_all * SPILL_COEF,
                                                pressure_equipment=self.pipeline[4],
                                                temperature_equipment=self.pipeline[5], density_liquid=self.sub[2],
                                                molecular_weight=self.sub[3], boiling_temperature_liquid=self.sub[4],
                                                heat_evaporation_liquid=self.sub[5],
                                                adiabatic=self.sub[6], heat_capacity_liquid=self.sub[7]).calculation()

        mass_pf = round(PART_TO_EXPLOSION * mass_gas * KG_TO_T, 4)

        scnario_description = 'Разрыв трубопровода на сечение→ отсутствие мгновенного воспламенения→возможность образования взрывоопасного облака→ отсроченное воспламенение → взрыв облака ТВС'
        general = [self.pipeline[0], self.pipeline[1], self.pipeline[10], scenario, scnario_value,
                   scnario_description,
                   mass_all, mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list(
            calc_tvs_explosion.Explosion().explosion_class_zone(self.sub[8], 4, mass_pf * T_TO_KG, self.sub[9],
                                                                self.sub[10], self.sub[11]))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = self.pipeline[9]
        injured_man = self.pipeline[10]

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=0, diametr_pipe=self.pipeline[3],
                                           lenght_pipe=self.pipeline[2],
                                           degree_damage=0.5, m_out_spill=0, m_in_spill=mass_all,
                                           S_spill=mass_all * SPILL_COEF).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_2 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 1.3. Токсическое поражение (полное)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[2] * self._select_probability_pipe(self.pipeline[3], self.pipeline[2])[-2]
        mass_gas = calc_evaporation.Evaporation(volume_equipment=mass_all, degree_filling=1,
                                                spill_square=mass_all * SPILL_COEF,
                                                pressure_equipment=self.pipeline[4],
                                                temperature_equipment=self.pipeline[5], density_liquid=self.sub[2],
                                                molecular_weight=self.sub[3], boiling_temperature_liquid=self.sub[4],
                                                heat_evaporation_liquid=self.sub[5],
                                                adiabatic=self.sub[6], heat_capacity_liquid=self.sub[7]).calculation()
        mass_pf = round(mass_gas * KG_TO_T, 3)
        scnario_description = 'Разрыв трубопровода на сечение→ отсутствие мгновенного воспламенения→возможность образования взрывоопасного облака→отсуствие отсроченного воспламенения → токсическое поражение'
        general = [self.pipeline[0], self.pipeline[1], self.pipeline[10], scenario, scnario_value,
                   scnario_description,
                   mass_all, mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list(calc_toxi.Toxi().LD_PD(spill_square=mass_all * SPILL_COEF))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0  # т.к. не не большие
        injured_man = 0  # т.к. не не большие

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=0, diametr_pipe=self.pipeline[3],
                                           lenght_pipe=self.pipeline[2],
                                           degree_damage=0.5, m_out_spill=mass_gas * KG_TO_T, m_in_spill=0,
                                           S_spill=mass_all * SPILL_COEF).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_3 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 2. Частичная разгерметизация
        # 2.1. Пожар (частичная)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[3] * self._select_probability_pipe(self.pipeline[3], self.pipeline[2])[-1]
        mass_pf = mass_all * PART_NOFULL_DAMAGE
        scnario_description = 'Частичная разгерметизация трубопровода→ мгновенное воспламенение→ пожар пролива'
        general = [self.pipeline[0], self.pipeline[1], self.pipeline[10], scenario, scnario_value,
                   scnario_description,
                   mass_pf, mass_pf]
        spill_fire = list(
            calc_strait_fire.Strait_fire().termal_class_zone(S_spill=mass_pf * SPILL_COEF, m_sg=M_SG,
                                                             mol_mass=self.sub[3], t_boiling=self.sub[4],
                                                             wind_velocity=WIND))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0
        injured_man = 1

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=0, diametr_pipe=self.pipeline[3],
                                           lenght_pipe=self.pipeline[2] * PART_NOFULL_DAMAGE,
                                           degree_damage=PART_NOFULL_DAMAGE, m_out_spill=0, m_in_spill=mass_all* PART_NOFULL_DAMAGE,
                                           S_spill=mass_pf * SPILL_COEF).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_4 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 2.2. Вспышка  (частичная)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[4] * self._select_probability_pipe(self.pipeline[3], self.pipeline[2])[-1]
        mass_gas = calc_evaporation.Evaporation(volume_equipment=mass_all * PART_NOFULL_DAMAGE,
                                                degree_filling=1,
                                                spill_square=mass_all * SPILL_COEF* PART_NOFULL_DAMAGE,
                                                pressure_equipment=self.pipeline[4],
                                                temperature_equipment=self.pipeline[5], density_liquid=self.sub[2],
                                                molecular_weight=self.sub[3], boiling_temperature_liquid=self.sub[4],
                                                heat_evaporation_liquid=self.sub[5],
                                                adiabatic=self.sub[6], heat_capacity_liquid=self.sub[7]).calculation()

        mass_pf = round(mass_gas * KG_TO_T, 3)
        scnario_description = 'Частичная разгерметизация трубопровода→ отсутствие мгновенного воспламенения→возможность образования взрывоопасного облака→ отсроченное воспламенение → пожар-вспышка'
        general = [self.pipeline[0], self.pipeline[1], self.pipeline[10], scenario, scnario_value,
                   scnario_description,
                   mass_all * PART_NOFULL_DAMAGE, mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list(calc_lower_concentration.LCLP().lower_concentration_limit(mass=mass_pf * T_TO_KG,
                                                                                    molecular_weight=self.sub[
                                                                                                         3] * MOLE_TO_KMOLE,
                                                                                    t_boiling=self.sub[4],
                                                                                    lower_concentration=3))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0  # т.к. т.к. вспышка
        injured_man = 1  # т.к. вспышка

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=0, diametr_pipe=self.pipeline[3],
                                           lenght_pipe=self.pipeline[2] * PART_NOFULL_DAMAGE,
                                           degree_damage=0.2, m_out_spill=mass_pf * KG_TO_T, m_in_spill=0,
                                           S_spill=mass_all * SPILL_COEF* PART_NOFULL_DAMAGE).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_5 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 2.3. Токси (частичная)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[5] * self._select_probability_pipe(self.pipeline[3], self.pipeline[2])[-1]
        mass_gas = calc_evaporation.Evaporation(volume_equipment=mass_all * PART_NOFULL_DAMAGE,
                                                degree_filling=1,
                                                spill_square=mass_all * SPILL_COEF * PART_NOFULL_DAMAGE,
                                                pressure_equipment=self.pipeline[4],
                                                temperature_equipment=self.pipeline[5], density_liquid=self.sub[2],
                                                molecular_weight=self.sub[3], boiling_temperature_liquid=self.sub[4],
                                                heat_evaporation_liquid=self.sub[5],
                                                adiabatic=self.sub[6], heat_capacity_liquid=self.sub[7]).calculation()

        mass_pf = round(mass_gas * KG_TO_T, 3)
        scnario_description = 'Частичная разгерметизация трубопровода→ отсутствие мгновенного воспламенения→возможность образования взрывоопасного облака→отсуствие отсроченного воспламенения → токсическое поражение'
        general = [self.pipeline[0], self.pipeline[1], self.pipeline[10], scenario, scnario_value,
                   scnario_description, mass_all * PART_NOFULL_DAMAGE, mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list(calc_toxi.Toxi().LD_PD(spill_square=mass_all * SPILL_COEF* PART_NOFULL_DAMAGE))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0  # т.к. т.к. ликвидация
        injured_man = 0  # т.к. ликвидация

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=0, diametr_pipe=self.pipeline[3],
                                           lenght_pipe=self.pipeline[2] * PART_NOFULL_DAMAGE,
                                           degree_damage=0.1, m_out_spill=0, m_in_spill=0,
                                           S_spill=mass_all * PART_NOFULL_DAMAGE).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_6 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        return (data_1, data_2, data_3, data_4, data_5, data_6)
