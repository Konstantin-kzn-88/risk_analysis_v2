import matplotlib.pyplot as plt
import numpy as np


class FN_FG_chart:
    def __init__(self, data_in_db):
        self.data_in_db = data_in_db

    def _return_data_for_chart(self):
        data_fn = []
        data_fg = []
        for i in self.data_in_db:
            data_fn.append([i[0], i[1]])  # Вероятность и число пострадавших
            data_fg.append([i[0], i[2]])  # Вероятность и материальный ущерб
        return (data_fn, data_fg)

    def _sum_data_for_fn(self, data: list):
        '''
        Функция вычисления суммирования вероятностей F при которой пострадало не менее N человек
        :param data: данные вида [[3.8e-08, 1],[5.8e-08, 2],[1.1e-08, 1]..]
        :return: данные вида: {1: 0.00018, 2: 0.012, 3: 6.9008e-06, 4: 3.8e-08, 2: 7.29e-05}
        '''
        uniq = set(sorted([i[1] for i in data]))
        result = dict(zip(uniq, [0] * len(uniq)))

        for item_data in data:
            for item_uniq in uniq:
                if item_data[1] >= item_uniq:
                    result[item_uniq] = result[item_uniq] + item_data[0]

        if 0 in result:
            del result[0]  # удалить суммарную вероятность где пострадало 0 человек
        return result

    def _sum_data_for_fg(self, data: list):
        '''
        Функция вычисления суммирования вероятностей F при которой ущерб не менее G млн.руб
        :param data: данные вида [[3.8e-08, 1.2],[5.8e-08, 0.2],[1.1e-08, 12.4]..]
        :return: данные вида: {0.2: 0.00018, 1: 0.012, 3: 6.9008e-06, 5: 3.8e-08, 6.25: 7.29e-05}
        '''
        uniq = np.arange(0, max([i[1] for i in data]) + max([i[1] for i in data]) / 7, max([i[1] for i in data]) / 7)
        result = dict(zip(uniq, [0] * len(uniq)))

        for item_data in data:
            for item_uniq in uniq:
                if item_data[1] >= item_uniq:
                    result[item_uniq] = result[item_uniq] + item_data[0]

        if 0 in result:
            del result[0]  # удалить суммарную вероятность где ущерб 0
        return result

    def _add_fn_criteria(self, ax, n_max):
        """Добавление критериев приемлемости для FN диаграммы с цветовыми зонами"""
        n_values = np.logspace(0, np.log10(n_max), 100)

        # Верхняя и нижняя границы
        f_upper = 1e-3 * n_values ** (-1)
        f_lower = 1e-5 * n_values ** (-1)

        # Создание цветовых зон
        # Недопустимая зона (красная)
        ax.fill_between(n_values, f_upper, 1,
                        color='red', alpha=0.1,
                        label='Недопустимый риск')

        # Переходная зона ALARP (желтая)
        ax.fill_between(n_values, f_lower, f_upper,
                        color='yellow', alpha=0.1,
                        label='Переходная зона (ALARP)')

        # Приемлемая зона (зеленая)
        ax.fill_between(n_values, 1e-7, f_lower,
                        color='green', alpha=0.1,
                        label='Приемлемый риск')

        # Границы
        ax.loglog(n_values, f_upper, 'r--', label='Граница недопустимого риска')
        ax.loglog(n_values, f_lower, 'g--', label='Граница приемлемого риска')

    def _add_fg_criteria(self, ax, g_max):
        """Добавление критериев приемлемости для FG диаграммы с цветовыми зонами"""
        g_values = np.logspace(0, np.log10(g_max), 100)

        # Верхняя и нижняя границы
        f_upper = 1e-3 * g_values ** (-1)
        f_lower = 1e-5 * g_values ** (-1)

        # Создание цветовых зон
        # Недопустимая зона (красная)
        ax.fill_between(g_values, f_upper, 1,
                        color='red', alpha=0.1,
                        label='Недопустимый риск')

        # Переходная зона ALARP (желтая)
        ax.fill_between(g_values, f_lower, f_upper,
                        color='yellow', alpha=0.1,
                        label='Переходная зона (ALARP)')

        # Приемлемая зона (зеленая)
        ax.fill_between(g_values, 1e-7, f_lower,
                        color='green', alpha=0.1,
                        label='Приемлемый риск')

        # Границы
        ax.loglog(g_values, f_upper, 'r--', label='Граница недопустимого риска')
        ax.loglog(g_values, f_lower, 'g--', label='Граница приемлемого риска')

    def fn_chart(self):
        """
        Построение FN диаграммы с критериями приемлемости
        """
        # получим данные с листа для построения диаграммы
        data = self._return_data_for_chart()[0]
        if len(data) < 3:
            return print('Значений для диаграммы должно быть больше')
        else:
            sum_data = self._sum_data_for_fn(data)
            people, probability = list(sum_data.keys()), list(sum_data.values())

            # для сплошных линий
            chart_line_x = []
            chart_line_y = []
            for i in people:
                chart_line_x.extend([i - 1, i, i, i])
                chart_line_y.extend([probability[people.index(i)], probability[people.index(i)], None, None])

            # для пунктирных линий
            chart_dot_line_x = []
            chart_dot_line_y = []
            for i in people:
                if i == people[-1]:
                    chart_dot_line_x.extend([i, i])
                    chart_dot_line_y.extend([probability[people.index(i)], 0])
                    break
                chart_dot_line_x.extend([i, i])
                chart_dot_line_y.extend([probability[people.index(i)], probability[people.index(i) + 1]])

            # Создание графика
            fig, ax = plt.subplots(figsize=(10, 8))

            # Построение основной диаграммы
            ax.semilogy(chart_line_x, chart_line_y, color='b', linestyle='-', marker='.')
            ax.semilogy(chart_dot_line_x, chart_dot_line_y, color='b', linestyle='--', marker='.')
            ax.set_xticks(people)

            # Добавление критериев приемлемости
            n_max = max(people) * 1.5  # Расширяем диапазон для лучшей видимости
            self._add_fn_criteria(ax, n_max)

            # Настройка графика
            ax.grid(True)
            ax.set_xlabel('Количество погибших, чел')
            ax.set_ylabel('Вероятность, 1/год')
            ax.set_title('F/N - диаграмма с критериями приемлемости риска')
            ax.legend()

            plt.subplots_adjust(bottom=0.15, left=0.15)
            plt.savefig('fn_with_criteria.jpg')
            plt.close()

    def fg_chart(self):
        """
        Построение FG диаграммы с критериями приемлемости
        """
        # получим данные с листа для построения диаграммы
        data = self._return_data_for_chart()[1]
        if len(data) < 3:
            return print('Значений для диаграммы должно быть больше')
        else:
            sum_data = self._sum_data_for_fg(data)
            damage, probability = list(sum_data.keys()), list(sum_data.values())

            # для сплошных линий
            chart_line_x = []
            chart_line_y = []
            for i in damage:
                if damage[0] == i:
                    chart_line_x.extend([0, i, i, i])
                    chart_line_y.extend([probability[damage.index(i)], probability[damage.index(i)], None, None])
                elif damage[-1] == i:
                    chart_line_x.extend([damage[damage.index(i) - 1], damage[damage.index(i) - 1], i, i])
                    chart_line_y.extend(
                        [probability[damage.index(i)], probability[damage.index(i)], probability[damage.index(i)],
                         probability[damage.index(i)]])
                    break
                else:
                    chart_line_x.extend([damage[damage.index(i) - 1], i, i, i])
                    chart_line_y.extend([probability[damage.index(i)], probability[damage.index(i)], None, None])

            # для пунктирных линий
            chart_dot_line_x = []
            chart_dot_line_y = []
            for i in damage:
                if i == damage[-1]:
                    chart_dot_line_x.extend([i, i])
                    chart_dot_line_y.extend([probability[damage.index(i)], probability[damage.index(i)]])
                    chart_dot_line_x.extend([i, i])
                    chart_dot_line_y.extend([probability[damage.index(i)], 0])
                    break
                chart_dot_line_x.extend([i, i])
                chart_dot_line_y.extend([probability[damage.index(i)], probability[damage.index(i) + 1]])

            # Создание графика
            fig, ax = plt.subplots(figsize=(10, 8))

            # Построение основной диаграммы
            ax.semilogy(chart_line_x, chart_line_y, color='r', linestyle='-', marker='.')
            ax.semilogy(chart_dot_line_x, chart_dot_line_y, color='r', linestyle='--', marker='.')

            # Добавление критериев приемлемости
            g_max = max(damage) * 1.5  # Расширяем диапазон для лучшей видимости
            self._add_fg_criteria(ax, g_max)

            # Настройка графика
            ax.grid(True)
            ax.set_xlabel('Ущерб, млн.руб')
            ax.set_ylabel('Вероятность, 1/год')
            ax.set_title('F/G - диаграмма с критериями приемлемости риска')
            ax.legend()

            plt.subplots_adjust(bottom=0.15, left=0.15)
            plt.savefig('fg_with_criteria.jpg')
            plt.close()


if __name__ == '__main__':
    # Примерные данные для тестирования
    # Формат: [вероятность, число_пострадавших, материальный_ущерб]
    test_data = [
        [1e-3, 1, 0.5],  # Высокая вероятность, малые последствия
        [5e-4, 2, 1.0],
        [1e-4, 3, 2.0],
        [5e-5, 4, 5.0],
        [1e-5, 6, 10.0],
        [5e-6, 8, 15.0],
        [1e-6, 10, 20.0],  # Низкая вероятность, серьезные последствия
        [5e-7, 15, 30.0],
        [1e-7, 20, 50.0],
    ]

    # Создание экземпляра класса и построение диаграмм
    chart = FN_FG_chart(test_data)

    # Построение FN диаграммы
    print("Построение FN диаграммы...")
    chart.fn_chart()
    print("FN диаграмма сохранена в файл 'fn_with_criteria.jpg'")

    # Построение FG диаграммы
    print("Построение FG диаграммы...")
    chart.fg_chart()
    print("FG диаграмма сохранена в файл 'fg_with_criteria.jpg'")