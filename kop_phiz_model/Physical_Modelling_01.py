import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import correlate2d
from Cell2D import Cell2D, draw_array


class Diffusion(Cell2D):# Клеточный автомат. Смешивание(диффузия). Ядро автомата.

    kernel = np.array([[0, 1, 0],
                       [1,-4, 1],
                       [0, 1, 0]])

    def __init__(self, n, r=0.1):
        # Объявление атрибутов. n: число строк r: постоянная- диффузионная константа (интенсивность диффузии)
        super().__init__(n)
        self.r = r
        self.array = np.zeros((n, n), float)

    def step(self):
        """Выполнить один шаг во времени (временной шаг).
        Применить ядро к каждой ячейке в 2D-массиве жидкости"""
        c = correlate2d(self.array, self.kernel, mode='same')
        self.array += self.r * c

    def add_cells(self, row, col, *strings):
        """Добавить ячейки в данное место Adds cells at the given location.
        row: индекс верхней строки
        col: индекс левого столбца
        strings: список строк 0s и 1s"""
        for i, s in enumerate(strings):
            self.array[row + i, col:col + len(s)] = np.array([int(b) for b in s])

    def draw(self):#выполнить инфографию (изобразить ячейки)
        draw_array(self.array, cmap='Reds')


#тело основной программы_____________________________________________
i=0
step = ""
while not step.isdigit():
    step = input("Введите количество состояний(временных шагов)\n(0 < step < 20), чтобы не нагружать вычислительные мощности)\n:")
    i+=1
    if i == 3:
        print('Наденьте очки. Необходимо вводить целые положительные числа.\nПрограмма остановлена.')
        exit()                           
step = int(step)
print("Количество состояний (шагов: ", step)
if step == 0 or step > 19:
    print('Пожалуйста, введите значения аргументов в диапазоне\n0 < кол-во состояний < 20\nПрограмма остановлена.')
    exit()

diff = Diffusion(n=9, r=0.1)
diff.add_cells(3, 3, '111', '111', '111')
for i in range(step):
    # очистка графика
    plt.clf()
    diff.draw()
    plt.annotate("Состояние_"+str(i+1), xy=(0, 0), xytext=(-0.8, -0.8), color='k')
    plt.axis('equal')
    # задержка на 1 сек
    plt.pause(1)
    diff.step()
plt.show()
