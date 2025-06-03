"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings_form.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QLCDNumber
from ui.d_eventfilter_settings_form import Ui_Form


class Window(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.settings = QtCore.QSettings("MyCompany", "MyApp")

        self.comboBox.addItems(["dec", "hex", "oct", "bin"])

        self.var_modes = {
            "dec": QLCDNumber.Mode.Dec,
            "hex": QLCDNumber.Mode.Hex,
            "oct": QLCDNumber.Mode.Oct,
            "bin": QLCDNumber.Mode.Bin,
        }

        self.positions()
        self.initSignals()

    def initSignals(self):
        self.dial.valueChanged.connect(self.horizontalSlider.setValue)
        self.horizontalSlider.valueChanged.connect(self.dial.setValue)

        self.dial.valueChanged.connect(self.lcdNumber.display)
        self.horizontalSlider.valueChanged.connect(self.lcdNumber.display)

        self.comboBox.currentTextChanged.connect(self.update_mode)

    def update_mode(self, text):
        mode = self.var_modes.get(text, QLCDNumber.Mode.Dec)
        self.lcdNumber.setMode(mode)

    def keyPressEvent(self, event, /):
        if event.key() == QtCore.Qt.Key.Key_Right:
            self.dial.setValue(self.dial.value() + 1)
        elif event.key() == QtCore.Qt.Key.Key_Left:
            self.dial.setValue(self.dial.value() - 1)

        return super().keyPressEvent(event)

    def closeEvent(self, event):
        self.settings.setValue("value", self.dial.value())
        self.settings.setValue("mode", self.comboBox.currentText())
        super().closeEvent(event)

    def positions(self):
        value = self.settings.value("value", 0, type=int)
        mode = self.settings.value("mode", "dec")

        self.dial.setValue(value)
        self.horizontalSlider.setValue(value)
        self.lcdNumber.display(value)

        check = self.comboBox.findText(mode)
        if check >= 0:
            self.comboBox.setCurrentIndex(check)

        self.update_mode(mode)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Window()
    window.show()
    app.exec()

