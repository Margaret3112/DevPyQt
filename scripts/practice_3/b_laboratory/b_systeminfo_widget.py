"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""
from PySide6 import QtWidgets
from a_threads import SystemInfo
from ui.b_system import Ui_Form


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.thread_check = SystemInfo()
        self.thread_check.systemInfoReceived.connect(self.cpuram_info)
        self.thread_check.delay = 1
        self.thread_check.start()
        self.ui.lineEdit.textChanged.connect(self.new_delay)

    def cpuram_info (self, data):
        cpu, ram = data
        self.ui.lineEdit_2.setText(f"{cpu}%")
        self.ui.lineEdit_3.setText(f"{ram}%")

    def new_delay(self, value: str):
            delay = float(value)
            if delay > 0:
                self.thread_check.set_delay = delay



if __name__ == '__main__':
            app = QtWidgets.QApplication()
            window = Window()
            window.show()
            app.exec()