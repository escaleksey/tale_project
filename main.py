from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStyleFactory
from PyQt5.QtWidgets import QTableWidgetItem
import design_main_page
import sys
import sqlite3


class NotFoundResult(Exception):
    pass


class VoidLineEdit(Exception):
    pass


class MainPage(QMainWindow, design_main_page.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('data/tales_db.db')

        self.initUi()
        self.update_table()

    def initUi(self):
        self.find_tale.clicked.connect(self.search_tale)


    def update_table(self):
        cur = self.con.cursor()
        result = cur.execute(f"SELECT tale.id, tale.title, tale.author, tale.description"
                                  f" FROM tale").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.headers = ['id', 'Название', 'Автор', 'Описание']
        for i, elem in enumerate(self.headers):
            header = QTableWidgetItem(elem)
            header.setBackground(QtGui.QColor(255, 231, 94))
            self.tableWidget.setHorizontalHeaderItem(i, header)

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def search_tale(self):
        cur = self.con.cursor()
        try:
            request = self.lineEdit.text().lower().capitalize()
            if not request:
                raise VoidLineEdit
            result = cur.execute(f"SELECT tale.id, tale.title, tale.author, tale.description"
                                  f" FROM tale WHERE tale.title = '{request}'").fetchall()
            if not result:
                raise NotFoundResult

            self.statusbar.showMessage(f'Найдено {len(result)} элементов')
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        except VoidLineEdit:
            self.statusbar.showMessage('Для выполнения этого действия нужно ввести название сказки в поисковую строку')
        except NotFoundResult:
            self.statusbar.showMessage('Сказки с таким названием не найдено')




sys.__excepthook__ = sys.__excepthook__


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = MainPage()
    ex.show()
    sys.exit(app.exec_())