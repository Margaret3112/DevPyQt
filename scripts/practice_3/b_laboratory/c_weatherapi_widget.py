"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QApplication
from ui.cc_weather import Ui_Form
from a_threads import WeatherHandler


class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.thread = None
        self.running = False

        self.initSignals()

    def initSignals(self) -> None:
        self.ui.pushButton.clicked.connect(self.onPushButtonVariance)

    def onPushButtonVariance(self) -> None:
        if not self.running:
            self.startThread()
        else:
            self.stopThread()

    def startThread(self) -> None:
        lat = float(self.ui.lineEdit_5.text())
        lon = float(self.ui.lineEdit.text())
        delay = int(self.ui.lineEdit_2.text())

        self.thread = WeatherHandler(lat, lon)
        self.thread.setDelay(delay)
        self.thread.getStatus(True)

        self.thread.started.connect(lambda: self.onThreadStarted())
        self.thread.weather.connect(lambda data: self.info_weather(data))
        self.thread.finished.connect(lambda: self.onThreadFinished())

        self.thread.start()
        self.ui.pushButton.setEnabled(False)

    def stopThread(self) -> None:
        if self.thread:
            self.thread.getStatus(False)
            self.thread.quit()
            self.thread.wait()

        self.running = False
        self.ui.pushButton.setText("Запуск")
        self.setInputsEnabled(True)

    def onThreadStarted(self) -> None:
        self.setInputsEnabled(False)
        self.ui.pushButton.setText("Остановить")
        self.ui.pushButton.setEnabled(True)
        self.running = True

    def info_weather(self, data: dict) -> None:
        weather = data.get("current_weather", {})
        temp = weather.get("temperature")
        self.ui.lineEdit_3.setText(f"Температура: {temp} °C")

    def onThreadFinished(self) -> None:
        self.running = False
        self.ui.pushButton.setText("Запуск")
        self.setInputsEnabled(True)

    def setInputsEnabled(self, enabled: bool) -> None:
        self.ui.lineEdit_5.setEnabled(enabled)
        self.ui.lineEdit.setEnabled(enabled)
        self.ui.lineEdit_2.setEnabled(enabled)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = WeatherWidget()
    window.show()
    sys.exit(app.exec())

