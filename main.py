from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStyleFactory
from PyQt5.QtWidgets import QTabWidget, QPushButton, QLabel, QTableWidgetItem, QHeaderView
import design_main_page
import sys
import sqlite3


class MainPage(QMainWindow, design_main_page.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('data/tales_db.db')
        self.initUi()

    def initUi(self):
        cur = self.con.cursor()
        self.result = cur.execute(f"SELECT tale.id, tale.title, tale.author, tale.description"
                                  f" FROM tale").fetchall()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.headers = ['id', 'Название', 'Автор', 'Описание']
        for i, elem in enumerate(self.headers):
            header = QTableWidgetItem(elem)
            header.setBackground(QtGui.QColor(255, 231, 94))
            self.tableWidget.setHorizontalHeaderItem(i, header)

        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = MainPage()
    ex.show()
    sys.exit(app.exec_())