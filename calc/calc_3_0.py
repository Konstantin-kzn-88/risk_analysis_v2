from .methods import calc_strait_fire
from .methods import calc_damage
from .methods import calc_evaporation
from .methods import calc_tvs_explosion
from .methods import calc_outflow
from .methods import calc_jet_fire
from .methods import calc_lower_concentration
from .methods import calc_fireball

# from
M_SG = 0.06  # удельная массовая скорость выгорания
WIND = 1  # скорость ветра
KG_TO_T = 0.001
KMOLE_TO_MOLE = 0.001
MOLE_TO_KMOLE = 1000
PART_TO_EXPLOSION = 0.1
T_TO_KG = 1000
PART_FULL_DAMAGE = 0.5
PART_NOFULL_DAMAGE = 0.15
PART_ECOLOG = 0.125
TIME_JET = 300


class Result:
    def __init__(self, scenario_num, equipment, sub, tree):
        self.equipment = equipment
        self.scenario_num = scenario_num
        self.sub = sub
        self.tree = tree

    def calculation(self):
        # 1. Полное разрушение
        mass_all = self.equipment[2] * self.equipment[3] * self.sub[
            2] * KG_TO_T  # объем*ст.заполнения*плотность вещества
        # 1.1. Расчет пожара пролива (полное)
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[0] * self.tree[-2]
        mass_pf = mass_all
        scnario_description = 'Полное разрушение→ мгновенное воспламенение→ пожар пролива'
        general = [self.equipment[0], self.equipment[1], self.equipment[7], scenario, scnario_value,
                   scnario_description,
                   mass_all, mass_pf]
        spill_fire = list(calc_strait_fire.Strait_fire().termal_class_zone(S_spill=self.equipment[4], m_sg=M_SG,
                                                                           mol_mass=self.sub[3], t_boiling=self.sub[4],
                                                                           wind_velocity=WIND))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = (self.equipment[8] - 1) if (self.equipment[8] - 1) > 0 else 0
        injured_man = (self.equipment[9] - 1) if (self.equipment[9] - 1) > 0 else 0

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=self.equipment[2], diametr_pipe=0, lenght_pipe=0,
                                           degree_damage=0.5, m_out_spill=0, m_in_spill=mass_all,
                                           S_spill=self.equipment[4]).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_1 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 1.2. Расчет взрыва (полное)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[1] * self.tree[-2]
        mass_gas = calc_evaporation.Evaporation(volume_equipment=self.equipment[2], degree_filling=self.equipment[3],
                                                spill_square=self.equipment[4],
                                                pressure_equipment=self.equipment[5],
                                                temperature_equipment=self.equipment[6], density_liquid=self.sub[2],
                                                molecular_weight=self.sub[3], boiling_temperature_liquid=self.sub[4],
                                                heat_evaporation_liquid=self.sub[5],
                                                adiabatic=self.sub[6], heat_capacity_liquid=self.sub[7]).calculation()

        mass_pf = round(PART_TO_EXPLOSION * mass_gas * KG_TO_T, 3)
        scnario_description = 'Полное разрушение→ отсутствие мгновенного воспламенения→возможность образования взрывоопасного облака→ отсроченное воспламенение → взрыв облака ТВС'
        general = [self.equipment[0], self.equipment[1], self.equipment[7], scenario, scnario_value,
                   scnario_description,
                   mass_all, mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list(
            calc_tvs_explosion.Explosion().explosion_class_zone(self.sub[8], 3, mass_pf * T_TO_KG, self.sub[9],
                                                                self.sub[10], self.sub[11]))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = self.equipment[8]
        injured_man = self.equipment[9]

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=self.equipment[2], diametr_pipe=0, lenght_pipe=0,
                                           degree_damage=0.5, m_out_spill=0, m_in_spill=mass_all,
                                           S_spill=self.equipment[4]).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_2 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 1.3. Ликвидация (полное)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[2] * self.tree[-2]
        mass_pf = 0  # т.к. нет поражающего фактора
        mass_gas = calc_evaporation.Evaporation(volume_equipment=self.equipment[2], degree_filling=self.equipment[3],
                                                spill_square=self.equipment[4],
                                                pressure_equipment=self.equipment[5],
                                                temperature_equipment=self.equipment[6], density_liquid=self.sub[2],
                                                molecular_weight=self.sub[3], boiling_temperature_liquid=self.sub[4],
                                                heat_evaporation_liquid=self.sub[5],
                                                adiabatic=self.sub[6], heat_capacity_liquid=self.sub[7]).calculation()
        scnario_description = 'Полное разрушение→ отсутствие мгновенного воспламенения→возможность образования взрывоопасного облака→ отсутствие отсроченного воспламенения → ликвидация аварии'
        general = [self.equipment[0], self.equipment[1], self.equipment[7], scenario, scnario_value,
                   scnario_description,
                   mass_all, mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0  # т.к. нет поражающего фактора
        injured_man = 0  # т.к. нет поражающего фактора

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=self.equipment[2] * PART_FULL_DAMAGE, diametr_pipe=0,
                                           lenght_pipe=0,
                                           degree_damage=0.5, m_out_spill=mass_gas * KG_TO_T, m_in_spill=0,
                                           S_spill=self.equipment[4]).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_3 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 2. Частичная разгерметизация
        # 2.1. Факел жидкостной (частичная)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[3] * self.tree[-1]
        consumption = calc_outflow.Outflow(pressure_equipment=self.equipment[5]).outflow_liquid(
            density_liquid=self.sub[2])

        mass_pf = round(consumption * TIME_JET * KG_TO_T, 3)

        scnario_description = 'Частичная разгерметизация→ разрушение ниже уровня жидкости→возможность мгновенного воспламенения→горение жидкостного факела'
        general = [self.equipment[0], self.equipment[1], self.equipment[7], scenario, scnario_value,
                   scnario_description,
                   mass_pf, mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list(calc_jet_fire.Torch().jetfire_size(consumption=consumption, type=2))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0  # т.к. т.к. частичное
        injured_man = 1  # т.к. частичное

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=self.equipment[2], diametr_pipe=0, lenght_pipe=0,
                                           degree_damage=0.3, m_out_spill=0, m_in_spill=mass_pf * KG_TO_T,
                                           S_spill=self.equipment[4] * PART_NOFULL_DAMAGE).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_4 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 2.2. Ликвидация жидкость (частичная)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[4] * self.tree[-1]
        consumption = calc_outflow.Outflow(pressure_equipment=self.equipment[5]).outflow_liquid(
            density_liquid=self.sub[2])

        mass_pf = 0
        scnario_description = 'Частичная разгерметизация→ разрушение ниже уровня жидкости→отсутствие мгновенного воспламенения→ликвидация аварии'
        general = [self.equipment[0], self.equipment[1], self.equipment[7], scenario, scnario_value,
                   scnario_description,
                   round(consumption * TIME_JET * KG_TO_T, 3), mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0  # т.к. т.к. ликвидация
        injured_man = 0  # т.к. ликвидация

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=self.equipment[2], diametr_pipe=0, lenght_pipe=0,
                                           degree_damage=0.1, m_out_spill=0, m_in_spill=0,
                                           S_spill=self.equipment[4] * PART_NOFULL_DAMAGE).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_5 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 2.3. Факел газовый (частичная)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[5] * self.tree[-1]
        consumption = calc_outflow.Outflow(pressure_equipment=self.equipment[5]).outflow_gas()

        mass_pf = round(consumption * TIME_JET * KG_TO_T, 3)

        scnario_description = 'Частичная разгерметизация→ разрушение выше уровня жидкости→возможность мгновенного воспламенения→горение газового факела'
        general = [self.equipment[0], self.equipment[1], self.equipment[7], scenario, scnario_value,
                   scnario_description,
                   mass_pf, mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list(calc_jet_fire.Torch().jetfire_size(consumption=consumption, type=0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0  # т.к. т.к. частичное
        injured_man = 1  # т.к. частичное

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=self.equipment[2], diametr_pipe=0, lenght_pipe=0,
                                           degree_damage=0.2, m_out_spill=mass_pf * KG_TO_T, m_in_spill=0,
                                           S_spill=PART_ECOLOG * self.equipment[4] * PART_NOFULL_DAMAGE).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_6 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 2.4. Вспышка газ (частичная)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[6] * self.tree[-1]
        consumption = calc_outflow.Outflow(pressure_equipment=self.equipment[5]).outflow_gas()

        mass_pf = round(consumption * TIME_JET * KG_TO_T, 3)
        scnario_description = 'Частичная разгерметизация→ разрушение выше уровня жидкости→отсуствие мгновенного воспламенения→ возможность отсроченного воспламенения→пожар-вспышка'
        general = [self.equipment[0], self.equipment[1], self.equipment[7], scenario, scnario_value,
                   scnario_description,
                   mass_pf, mass_pf]
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
                                           volume_equipment=self.equipment[2], diametr_pipe=0, lenght_pipe=0,
                                           degree_damage=0.2, m_out_spill=mass_pf * KG_TO_T, m_in_spill=0,
                                           S_spill=PART_ECOLOG * self.equipment[4] * PART_NOFULL_DAMAGE).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_7 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 2.5. Ликвидация газ (частичная)
        self.scenario_num += 1
        scenario = 'C' + str(self.scenario_num)
        scnario_value = self.tree[7] * self.tree[-1]
        consumption = calc_outflow.Outflow(pressure_equipment=self.equipment[5]).outflow_gas()

        mass_pf = 0
        scnario_description = 'Частичная разгерметизация→ разрушение ниже уровня жидкости→отсутствие мгновенного воспламенения→ликвидация аварии'
        general = [self.equipment[0], self.equipment[1], self.equipment[7], scenario, scnario_value,
                   scnario_description,
                   round(consumption * TIME_JET * KG_TO_T, 3), mass_pf]
        spill_fire = list((0, 0, 0, 0))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list((0, 0, 0, 0))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0  # т.к. т.к. ликвидация
        injured_man = 0  # т.к. ликвидация

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=self.equipment[2], diametr_pipe=0, lenght_pipe=0,
                                           degree_damage=0.1, m_out_spill=mass_pf * KG_TO_T, m_in_spill=0,
                                           S_spill=PART_ECOLOG * self.equipment[4] * PART_NOFULL_DAMAGE).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_8 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        # 3. Полное разрушение - Огненный шар
        self.scenario_num += 1
        mass_all = self.equipment[2] * self.equipment[3] * self.sub[
            2] * KG_TO_T  # объем*ст.заполнения*плотность вещества
        # 1.1. Расчет пожара пролива (полное)
        scenario = 'C' + str(self.scenario_num)
        scnario_value = 2.5e-5
        mass_pf = mass_all
        scnario_description = 'Полное разрушение при воздействии внешнего источника горения→ образование огненного шара+горение пролива'
        general = [self.equipment[0], self.equipment[1], self.equipment[7], scenario, scnario_value,
                   scnario_description,
                   mass_all, mass_pf]
        spill_fire = list(calc_strait_fire.Strait_fire().termal_class_zone(S_spill=self.equipment[4], m_sg=M_SG,
                                                                           mol_mass=self.sub[3], t_boiling=self.sub[4],
                                                                           wind_velocity=WIND))  # результат расчета пожара
        explosion = list((0, 0, 0, 0, 0))  # результат расчета взрыва
        jet_fire = list((0, 0))  # результат расчета факела
        flash_fire = list((0, 0))  # результат расчета вспышки
        toxi = list((0, 0))  # результат расчета токси
        ball_fire = list(calc_fireball.Fireball().termal_class_zone(mass_all *T_TO_KG*0.01, 350))  # результат расчета шара
        spill_toxi = list((0,))  # результат расчета токс.пролива

        dead_man = 0
        injured_man = 1

        result_damage = calc_damage.Damage(dead_man=dead_man, injured_man=injured_man,
                                           volume_equipment=self.equipment[2], diametr_pipe=0, lenght_pipe=0,
                                           degree_damage=0.7, m_out_spill=0, m_in_spill=mass_all,
                                           S_spill=self.equipment[4]).sum_damage()
        damage = list(result_damage)  # результат расчета ущерба
        man = list((dead_man, injured_man))  # результат расчета погибших/пострадавших
        coll_risk = list(
            (scnario_value * dead_man, scnario_value * injured_man))  # результат расчета погибших/пострадавших
        math_risk = list((scnario_value * result_damage[-1],))  # результат мат.риска
        data_9 = general + spill_fire + explosion + jet_fire + flash_fire + toxi + ball_fire + spill_toxi + damage + man + coll_risk + math_risk

        return (data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8, data_9)
