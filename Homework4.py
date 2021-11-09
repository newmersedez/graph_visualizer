import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import random


app = QtGui.QApplication([])


# класс окна игры змейка
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.score = 0          # Общий счет
        self.operation = ''         # Переменная для отслеживания нажатой клавиши
        self.deleted_tail = [0, 0]      # Последний элемент змейки(хвост)
        self.speed = 300            # Скорость перемещения

        # Главное окно игры
        self.main_window = QtGui.QMainWindow()
        self.main_window.setWindowTitle('Python Game: Snake')
        self.main_window.resize(1100, 800)

        # Задание главного менеджера размещения
        # Верт. и горизонт. менеджера размещения кнопок и полотна
        self.main_widget = QtWidgets.QWidget()
        self.hbox = QtWidgets.QHBoxLayout()                 # Главный менеджер размещения
        self.vbox = QtWidgets.QVBoxLayout()                 # Для кнопок управления и статистики
        self.canvas = pg.PlotWidget()                       # Отрисовка графика
        self.hbox.addWidget(self.canvas)
        self.hbox.addLayout(self.vbox)

        # Создание функциональных кнопок и информационной панели
        # С общим счетом, скоростью и сообщениями
        self.vbox_info = QtWidgets.QVBoxLayout()        # Информация или сообщения
        self.vbox_hud = QtWidgets.QVBoxLayout()         # Менеджер размещения для статистика
        self.vbox_control_panel = QtWidgets.QVBoxLayout()    # Менеджер размещения для кнопок
        self.vbox.addLayout(self.vbox_hud)
        self.vbox.addLayout(self.vbox_info)
        self.vbox.addLayout(self.vbox_control_panel)

        # Счет, скорость, описание игры, информация о паузе/возобновлении
        self.health_power = QtWidgets.QLabel('<center>Счет: {}</center>'.format(self.score))
        self.vbox_hud.addWidget(self.health_power)
        self.speed_info = QtWidgets.QLabel('<center>Скорость: 1</center>')
        self.vbox_hud.addWidget(self.speed_info)
        self.pause_resume_info = QtWidgets.QLabel('<center>Нажмите любую кнопку управления, чтобы начать</center>')
        self.vbox_hud.addWidget(self.pause_resume_info)
        self.description = QtWidgets.QLabel('<center>-----------------------------------------------------</center>\n'      
                                            '<center>Игра Змейка</center>'                                                                                     
                                            '<center>Инструкция</center>\n'
                                            '<center>W/Стрелка вверх - движение вверх</center>\n'
                                            '<center>S/Стрелка вниз - движение вниз</center>\n'
                                            '<center>A/Стрелка влево - движение влево</center>\n'
                                            '<center>D/Стрелка вправо - движение вправо</center>\n'
                                            '<center>------------------------------------------------------</center>\n')
        self.vbox_info.addWidget(self.description)

        # Функциональные кнопки
        self.btn_pause = QtWidgets.QPushButton('&Пауза')
        self.btn_pause.clicked.connect(self.pause_button)
        self.btn_resume = QtWidgets.QPushButton('&Вернуться в игру')
        self.btn_resume.clicked.connect(self.resume_button)
        self.btn_new_game = QtWidgets.QPushButton('&Новая игра')
        self.btn_new_game.clicked.connect(self.new_game_button)
        self.btn_exit = QtWidgets.QPushButton('&Выход')
        self.btn_exit.clicked.connect(QtWidgets.qApp.exit)
        self.vbox_control_panel.addWidget(self.btn_pause)
        self.vbox_control_panel.addWidget(self.btn_resume)
        self.vbox_control_panel.addWidget(self.btn_new_game)
        self.vbox_control_panel.addWidget(self.btn_exit)

        # Размещение
        self.main_widget.setLayout(self.hbox)
        self.main_window.setCentralWidget(self.main_widget)

        # Вызов метод построения игрового поля
        self.__init_field()

        # Вызов метода построения змейки
        self.__init_snake()

        # Вызов метода спавна "еды"
        self.__init_food()

        # Таймер анимации
        self.__timer_id = self.startTimer(self.speed)
        if self.__timer_id == -1:
            print("Не смог создать таймер - анимации больше не будет")

        # Блокировка фокуса на полотне
        self.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.canvas.setFocus()

        # Вывод окна
        self.main_window.show()

    # Метод построения игрового поля
    def __init_field(self):
        self.play_field = QtWidgets.QGraphicsRectItem(QtCore.QRectF(-98, -98, 196, 196))
        self.play_field.setPen(pg.mkPen(150, 0, 0))
        self.canvas.addItem(self.play_field)

    # Метод построение графа, который и будет змейкой
    def __init_snake(self):
        self.item = pg.PlotDataItem([0], pen=(0, 0, 200), symbolBrush=(1, 50, 32), symbolPen='w', symbol='s',
                                    symbolSize=20)
        self.plot = self.canvas.getPlotItem()
        self.plot.addItem(self.item)

        self.plot.setMouseEnabled(x=False, y=False)             # Отключение скроллинга
        self.plot.enableAutoRange(x=False, y=False)
        self.plot.setLimits(xMin=-100, xMax=100, yMin=-100, yMax=100)
        self.pos_data = [[0, 0], [5, 0], [10, 0], [15, 0]]
        self.plot.setXRange(min=-100, max=100)
        self.plot.setYRange(min=-100, max=100)
        self.canvas.showAxis('bottom', False)
        self.canvas.showAxis('left', False)

        self.graph = self.item

    # Метод добавления на игровое поле одной единицы еды
    def __init_food(self):
        self.coord_x = random.randrange(-90, 90, 5)
        self.coord_y = random.randrange(-90, 90, 5)
        self.food = pg.PlotDataItem([0], pen=(0, 0, 200), symbolBrush=(150, 0, 0),
                                    symbolPen='w', symbol='o', symbolSize=40)
        self.plot_food = self.canvas.getPlotItem()
        self.plot_food.addItem(self.food)
        self.food.setData(np.array([[self.coord_x, self.coord_y]]))

    # Метод проверки того, попала змея на еду или нет
    def __snake_on_food(self):
        # self.coord_x - 15, self.coord_x + 15 - диапазон "еды" по х
        # self.coord_y - 15, self.coord_y + 15 - диапазон "еды" по у

        # Основная идея заключается в том, чтобы сравнивать координаты еды и координаты головы змейки
        # Соответственно, если координаты головы змейки находятся в соответствующем диапазоне, то змейка съела еду
        # В ином случае не съела

        if self.check_x >= self.coord_x - 5 and self.check_x <= self.coord_x + 5\
                and self.check_y >= self.coord_y - 5 and self.check_y <= self.coord_y + 5:
            # print('попал в еду')
            self.__snake_growth()
            self.__delete_food()
            self.__init_food()

    # Метод удаления "еды" с игрового поля
    def __delete_food(self):
        self.coord_x = 1000
        self.coord_y = 1000
        self.food.setData(np.array([[self.coord_x, self.coord_y]]))

    # Методы прибавления к змее новых ячеек
    # Для демонстрации работы изменения скорости можно изменить параметр на любой
    # Можно поставить -100, тогда змейка будет перемещаться очень быстро
    # self.speed уменьшается на 1(лучше ставить в диапазоне 1-5), потому что это самый оптимальный параметр для игры
    def __snake_growth(self):
        self.pos_data.append(self.deleted_tail)      # Добавляем удаленный хвост в конец
        self.item.setData(np.array(self.pos_data))
        self.score += 10
        if self.score > 0 or self.speed < 20:
            self.speed -= 5            # Постепенно изменяем скорость, усложняя игру (1-5 - идеально)
            self.killTimer(self.__timer_id)                 # Обновление таймера с новым значением скорости
            self.__timer_id = self.startTimer(self.speed)   #
        self.speed_info.setText('<center>Скорость: {}</center>'.format(300 - self.speed))
        self.health_power.setText('<center>Score: {}</center>'.format(self.score))

    # Проверка на выход за пределы поля, в случае выполнения условия завершение игры
    # Используются check_x и check_y - координаты головы змеи
    def __exit_field(self):
        if (self.check_x < -95) or (self.check_y < -95) or (self.check_x > 95) or (self.check_y > 95):
            self.killTimer(self.__timer_id)
            self.pause_resume_info.setText('<center>Игра окончена, вы вышли за пределы игрового поля</center>')
            # print('Выход за пределы игрового поля!')

    # Метод, реализующий нажатие кнопки паузы
    def pause_button(self):
        self.killTimer(self.__timer_id)
        self.pause_resume_info.setText('<center>Пауза</center>')
        # print('clicked')

    # Метод, реализующий нажатие на кнопку возобновления игры
    def resume_button(self):
        self.killTimer(self.__timer_id)
        self.__timer_id = self.startTimer(self.speed)
        self.pause_resume_info.setText('<center>Игра возобновлена</center>')
        # print(self.speed)
        # print('resume button clicked')

    # Метод, реализующий начало новой игры
    def new_game_button(self):
        self.score = 0
        self.speed = 300
        self.killTimer(self.__timer_id)
        self.__timer_id = self.startTimer(self.speed)

        self.speed_info.setText('<center>Скорость: 1</center>')
        self.health_power.setText('<center>Счет: {}</center>'.format(self.score))
        self.pause_resume_info.setText('<center>Нажмите любую кнопку управления, чтобы начать</center>')
        self.pos_data.clear()
        self.pos_data = [[0, 0], [5, 0], [10, 0], [15, 0]]
        self.plot.clear()

        self.__init_field()
        self.__init_snake()
        self.__init_food()
        # print('new game button clicked')

    def keyPressEvent(self, event):
        self.operation = ''
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_W or event.key() == QtCore.Qt.Key_Up:
                # print('Up/W')
                self.operation = 'Up'
                event.accept()
            elif event.key() == QtCore.Qt.Key_S or event.key() == QtCore.Qt.Key_Down:
                # print('Down/S')
                self.operation = 'Down'
                event.accept()
            elif event.key() == QtCore.Qt.Key_A or event.key() == QtCore.Qt.Key_Left:
                # print('Left/A')
                self.operation = 'Left'
                event.accept()
            elif event.key() == QtCore.Qt.Key_D or event.key() == QtCore.Qt.Key_Right:
                # print('Right/D')
                self.operation = 'Right'
                event.accept()
        event.ignore()

    def timerEvent(self, event):
        self.deleted_tail = self.pos_data[-1]        # Запоминаем последний удаленный элемент
        # print(self.deleted_tail)

        self.check_x = self.pos_data[0][0]       # Координаты головы змейки
        self.check_y = self.pos_data[0][1]       # необходимы для увеличения длины змейки и тд.
        # print(self.check_x, ':', self.check_y)

        self.long = len(self.pos_data)
        self.item.setData(np.array(self.pos_data))

        if self.operation == 'Up':
            self.pos_data.insert(0, [self.check_x, self.check_y + 5])
            self.pos_data = self.pos_data[0:self.long]
            # print(self.pos_data)

        elif self.operation == 'Down':
            self.pos_data.insert(0, [self.check_x, self.check_y - 5])
            self.pos_data = self.pos_data[0:self.long]
            # print(self.pos_data)

        elif self.operation == 'Right':
            self.pos_data.insert(0, [self.check_x + 5, self.check_y])
            self.pos_data = self.pos_data[0:self.long]
            # print(self.pos_data)

        elif self.operation == 'Left':
            self.pos_data.insert(0, [self.check_x - 5, self.check_y])
            self.pos_data = self.pos_data[0:self.long]
            # print(self.pos_data)

        # Запускается проверка, попала ли змея на еду
        self.__snake_on_food()

        # Проверка на выход за пределы игрового поля
        self.__exit_field()


window = MyWindow()
window.grabKeyboard()
sys.exit(app.exec_())  # Запускаем цикл обработки событий
