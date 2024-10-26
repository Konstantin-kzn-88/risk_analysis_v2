import matplotlib.pyplot as plt
import numpy as np


class FN_FG_chart:
    '''
    Класс построения F/N  и  F/G диаграмм.
    '''

    def __init__(self, data_in_db):
        self.data_in_db = data_in_db

    def _return_data_for_chart(self):
        data_fn = []
        data_fg = []
        for i in self.data_in_db:
            data_fn.append([i[5], i[35]])
            data_fg.append([i[5], i[34]])
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

        del result[0]  # удалить суммарную вероятность где пострадало 0 человек
        return result

    def _sum_data_for_fg(self, data: list):
        '''
        Функция вычисления суммирования вероятностей F при которой ущерб не менее G млн.руб
        :param data: данные вида [[3.8e-08, 1.2],[5.8e-08, 0.2],[1.1e-08, 12.4]..]
        :return: данные вида: {0.2: 0.00018, 1: 0.012, 3: 6.9008e-06, 5: 3.8e-08, 6.25: 7.29e-05}
        '''
        uniq = np.arange(0, max([i[1] for i in data])+max([i[1] for i in data]) / 7, max([i[1] for i in data]) / 7)

        result = dict(zip(uniq, [0] * len(uniq)))

        for item_data in data:
            for item_uniq in uniq:
                if item_data[1] >= item_uniq:
                    result[item_uniq] = result[item_uniq] + item_data[0]

        del result[0]  # удалить суммарную вероятность где ущерб 0
        return result

    def fn_chart(self):
        """
        Построение FN диаграммы
        :return:
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

            # Отрисовка графика
            # fig = plt.figure()
            plt.semilogy(chart_line_x, chart_line_y, color='b', linestyle='-', marker='.')
            plt.semilogy(chart_dot_line_x, chart_dot_line_y, color='b', linestyle='--', marker='.')
            plt.xticks(ticks=people)
            plt.title('F/N - диаграмма')
            plt.xlabel('Количество погибших, чел')
            plt.ylabel('Вероятность, 1/год')
            plt.subplots_adjust(bottom=0.15, left=0.15)  # Добавляем пространство снизу и слева
            plt.grid(True)

            # plt.show(bbox_inches='tight')
            plt.savefig(f'fn.jpg')

    def fg_chart(self):
        """
        Построение FG диаграммы
        :return:
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
                    chart_line_x.extend([damage[damage.index(i)-1], damage[damage.index(i)-1], i, i])
                    chart_line_y.extend([probability[damage.index(i)], probability[damage.index(i)], probability[damage.index(i)], probability[damage.index(i)]])
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

            # Отрисовка графика
            fig = plt.figure()
            plt.semilogy(chart_line_x, chart_line_y, color='r', linestyle='-', marker='.')
            plt.semilogy(chart_dot_line_x, chart_dot_line_y, color='r', linestyle='--', marker='.')
            # plt.xticks(ticks=damage)
            plt.title('F/G - диаграмма')
            plt.xlabel('Ущерб, млн.руб')
            plt.ylabel('Вероятность, 1/год')
            plt.subplots_adjust(bottom=0.15, left=0.15)  # Добавляем пространство снизу и слева
            plt.grid(True)

            # plt.show()
            plt.savefig(f'fg.jpg')


# if __name__ == '__main__':
#
#     chart = FN_FG_chart(data=data)
#     # chart.fn_chart()
#     # chart.fg_chart()
