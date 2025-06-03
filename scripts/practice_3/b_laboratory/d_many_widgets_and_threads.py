"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
from PySide6 import QtWidgets
from c_weatherapi_widget import WeatherWidget
from b_systeminfo_widget import Window as SystemInfoWidget

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.weather_widget = WeatherWidget()
        self.systeminfo_widget = SystemInfoWidget()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.weather_widget)
        layout.addWidget(self.systeminfo_widget)

        self.setLayout(layout)
        self.setWindowTitle("Объединённый интерфейс")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
