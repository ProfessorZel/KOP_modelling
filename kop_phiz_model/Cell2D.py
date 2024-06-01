import numpy as np
import matplotlib.pyplot as plt 
from IPython.display import clear_output

from time import sleep

from utils import underride


class Cell2D:
    """Родительский класс для 2D-клеточного автомата."""

    def __init__(self, n, m=None):
        """Объявление атрибутов.
        n: number of rows
        m: number of columns
        """
        m = n if m is None else m
        self.array = np.zeros((n, m), np.uint8)
        #Нули, но типа "целочисленные без знака", совместимые с типом в C "unsigned long".
        #того - 8-разрядные целые числа без знака.
        #self.array - название массива модель-системы для объекта self
        
    """def add_cells(self, row, col, *strings):
        #Добавление ячеек в заданные места.row: индекс верхней сроки
        #col: индекс левого столбца. strings: список строк  (0s и 1s)
        #for i, s in enumerate(strings):
         #   self.array[row+i, col:col+len(s)] = np.array([int(b) for b in s])
         """
            
    def loop(self, iters=1):
        """Отрабатывает заданное количество шагов."""
        for i in range(iters):
            self.step()

    def draw(self, **options):
        """Отображает массив ячеек."""
        draw_array(self.array, **options)

    """def animate(self, frames, interval=None, step=None):
        #Анимирует моделирование        
        #frames: число фреймов(кадров) для отрисовки
        #interval: время (в сек.)между фреймов
        #iters: число шагов между фреймами
        
        if step is None:
            step = self.step
            
        plt.figure()
        try:
            for i in range(frames-1):
                self.draw()
                plt.show()
                if interval:
                    sleep(interval)
                step()
                clear_output(wait=True) # https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.clear_output
            self.draw()
            plt.show()
        except KeyboardInterrupt:
            pass """
        

def draw_array(array, **options):
    """Отображает ячейки клеточного автомата"""
    n, m = array.shape
    options = underride(options,
                        cmap='Greens',
                        alpha=0.7,
                        vmin=0, vmax=1, 
                        interpolation='none', 
                        origin='upper',
                        extent=[0, m, 0, n])

    plt.axis([0, m, 0, n])
    plt.xticks([])
    plt.yticks([])

    return plt.imshow(array, **options)#отображает данные как 2D-растровую картинку
