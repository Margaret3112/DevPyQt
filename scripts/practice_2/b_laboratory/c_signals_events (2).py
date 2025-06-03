"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6 import QtWidgets, QtCore
from ui.c_signals_events_form import Ui_Form
from datetime import datetime



class Window(QtWidgets.QWidget, Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        screen = QtWidgets.QApplication.primaryScreen()
        self.w_screen, self.h_screen = screen.size().toTuple()

        self.spinBoxX.setMaximum(self.w_screen - self.size().width())
        self.spinBoxY.setMaximum(self.h_screen - self.size().height())
        self.spinBoxX.setValue(500)
        self.spinBoxY.setValue(500)

        self.old_pos = self.pos()
        self.initSignals()

    def initSignals(self):
        self.pushButtonGetData.clicked.connect(self.get_state_data)
        self.pushButtonMoveCoords.clicked.connect(
            lambda: self.move(self.spinBoxX.value(), self.spinBoxY.value())
        )

    def get_time(self) -> str:
        now = datetime.now()
        return f"[{now.day:02d}.{now.month:02d}.{now.year} {now.hour:02d}:{now.minute:02d}:{now.second:02d}]"

    def window_status(self) -> str:
        states = []

        if self.isMinimized():
            states.append("Свернуто")
        elif self.isMaximized():
            states.append("Развёрнуто")

        if self.isActiveWindow():
            states.append("Активно")
        if self.isVisible():
            states.append("Отображается")

        return " / ".join(states)



    def get_state_data(self):
        screen = QtWidgets.QApplication.primaryScreen()
        all_screens = QtWidgets.QApplication.screens()
        screen_index = all_screens.index(screen)
        data = f"""
        Кол-во экранов: {len(QtWidgets.QApplication.screens())}
        Основное окно: {QtWidgets.QApplication.primaryScreen().name()}
        Разрешение экрана: Ширина = {self.w_screen}, Высота = {self.h_screen}
        Размеры окна: {self.size().width()} x {self.size().height()}
        Минимальный размер: {self.minimumSize().toTuple()}
        Максимальный размер: {self.maximumSize().toTuple()}
        Координаты окна: {self.x()}, {self.y()}
        Координаты окна: {self.pos().toTuple()}
        Центр: {self.rect().center().toTuple()}
        Состояние: {self.window_status()}
        """
        self.plainTextEdit.appendPlainText(data)



    def resizeEvent(self, event, /):
        size = self.size()
        print(f"{self.get_time()} {size.width()} x {size.height()}")
        return super().resizeEvent(event)

    def moveEvent(self, event):
        new_pos = self.pos()
        self.old_pos = new_pos
        return super().moveEvent(event)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            print(f"{self.get_time()} {self.window_status()}")
        return super().changeEvent(event)



if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
