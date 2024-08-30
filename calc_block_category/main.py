import math

volume_equipment = 27.2  # объем, м3
degree_filling = 0.151  # степень заполения, доли единицы
spill_square = 300  # м2
pressure_equipment = 0.1  # давление, МПа
temperature_equipment = 135  # температура, градусов Цельсия
sub_name = 'Нефть'
density_liquid = 850  # плотность, кг/м3
molecular_weight = 0.06  # кг/моль
boiling_temperature_liquid = 300  # температура кипения, градусов Цельсия (чем больше температура кипения, тем меньше мгновенно испаряется)
heat_evaporation_liquid = 179000  # теплота испарения, Дж/кг (чем больше теплота, тем меньше мгновенно испаряется)
adiabatic = 1.01  # показатель адиабаты
heat_capacity_liquid = 1200  # теплоемкость жидкости, Дж/кг/град (чем меньше теплоемкость, тем меньше мгновенно испаряется)
surface = 'Бетон'
density_surface = 2200  # плотность бетона, кг/м3
thermal_conductivity_surface = 1.42  # теплопроводность бетона, Вт/(м·град)
heat_capacity_surface = 770  # теплоёмкость бетона, Дж/(кг·K)
temperature_surface = 220  # температура, градусов Цельсия (чем больше температура поверности, тем больше кипит)
R = 8.314  # газовая постоянная


def mass_boiling(boiling_temperature_liquid: int, spill_square: int, time_boiling: int):
    '''
    Ф-ция определения количества испарившейся жидкости при кипении и последующем испарении при захолаживании жидкости

    :param boiling_temperature_liquid: температура кипения, градусов Цельсия
    :param spill_square: площадь пролива, м2
    :param time_boiling: время кипения, с
    :return:
    '''
    sum_g_50 = 0.0001 * pow(boiling_temperature_liquid, 3) + 0.0067 * pow(boiling_temperature_liquid, 2) - \
               3.4616 * boiling_temperature_liquid + 163.37  # интерполяция табл.2 прил.2 ОПВБ
    return sum_g_50 * (spill_square / 50) * (time_boiling / 180)  # ф-ла табл.2 прил.2 ОПВБ


print('1. Объем парогазовой фазы в блоке, м3:')
volume_gas = volume_equipment * (1 - degree_filling)
print(volume_gas)

print('2. Масса жидкости в блоке, кг:')
mass_liguid = volume_equipment * degree_filling * density_liquid
print(mass_liguid)

print('3. Масса ПГФ, имеющаяся непосредственно в блоке, кг:')
mass_gas = molecular_weight * volume_gas * pressure_equipment * pow(10, 6) / (R * (temperature_equipment + 273))
print(mass_gas)

print(
    '4.Масса вещества, переходящая в парогазовую фазу при мгновенном вскипании перегретой жидкости блока (аппарата), кг:')
fraction = 1 - math.exp(-heat_capacity_liquid * (((temperature_equipment + 273) - (
        boiling_temperature_liquid + 273) + math.fabs(
    (temperature_equipment + 273) - (boiling_temperature_liquid + 273))) / heat_evaporation_liquid))
mass_instantly_boiling = fraction * mass_liguid
print(mass_instantly_boiling)

print('5. Масса вещества в проливе после мгновенного вскипания жидкости, кг:')
mass_liguid_after_instantly_boiling = mass_liguid - mass_instantly_boiling
print(mass_liguid_after_instantly_boiling)

print('6. Давление насыщенного пара при расчетной температуре, Па:')
steam_pressure = 101325 * math.exp((heat_evaporation_liquid * molecular_weight / R) * (
        (1 / (boiling_temperature_liquid + 273)) - (1 / (temperature_equipment + 273))))
print(steam_pressure)

print('7. Масса испарившегося в-ва от теплопритока поверхности, кг и время кипения, с:')

if temperature_surface > boiling_temperature_liquid:
    time_boiling = ((temperature_surface - boiling_temperature_liquid + math.fabs(
        temperature_surface - boiling_temperature_liquid)) / (2 * heat_evaporation_liquid / 1000)) * pow(
        thermal_conductivity_surface * heat_capacity_surface * density_surface / math.pi, 1 / 2) * 1 / (
                           pow(molecular_weight, 1 / 2) * pow(10, -6) * 9.93 * steam_pressure)
    print(time_boiling)
    mass_surface_heat_intake = min(mass_boiling(boiling_temperature_liquid, spill_square, time_boiling),mass_liguid_after_instantly_boiling)
    print(mass_surface_heat_intake)
else:
    mass_surface_heat_intake = min(
        pow(10, -6) * (steam_pressure / 1000) * math.sqrt(molecular_weight * 1000) * 3600 * spill_square,
        mass_liguid_after_instantly_boiling)
    print(0)
    print(mass_surface_heat_intake)

print('8. Масса вещества оставшегося в проливе после испарения от теплопритока поверхности, кг:')
mass_end = mass_liguid_after_instantly_boiling - mass_surface_heat_intake
print(mass_end)

print('9. Масса вещества перешедшее в газообразное состояние, кг:')
mass_gas_end = mass_gas+mass_instantly_boiling+mass_surface_heat_intake
print(mass_gas_end)

if __name__ == '__main__':
    print('')
