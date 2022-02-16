from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStyleFactory, QAbstractItemView
from PyQt5.QtWidgets import QTableWidgetItem
import design_main_page
from more_info import InfoPage
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
        self.update_tales_table()

    def initUi(self):
        self.find_tale.clicked.connect(self.search)
        self.find_character.clicked.connect(self.search)
        self.radioButton.toggled.connect(self.change_table)
        self.radioButton_2.toggled.connect(self.change_table)
        self.more_info.clicked.connect(self.ger_more_info)
        self.tableWidget.cellClicked.connect(self.select_row)
        self.reload_table.clicked.connect(self.change_table)

    def select_row(self):
        self.tableWidget.clearSelection()
        #self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        row = self.tableWidget.currentRow()
        self.tableWidget.selectRow(row)

    def change_table(self):
        if self.radioButton_2.isChecked():
            self.update_characters_table()
        else:
            self.update_tales_table()

    def update_characters_table(self):
        cur = self.con.cursor()
        result = cur.execute(f"SELECT characters.id, characters.name, tale.title"
                             f" FROM characters"
                             f" INNER JOIN tale ON tale.id = characters.tale").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.headers = ['id', 'Имя', 'Сказка', '1']
        for i, elem in enumerate(self.headers):
            header = QTableWidgetItem(elem)
            header.setBackground(QtGui.QColor(255, 231, 94))
            self.tableWidget.setHorizontalHeaderItem(i, header)

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def update_tales_table(self):
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

    def search(self):
        btn = self.sender()
        cur = self.con.cursor()
        try:
            request = self.lineEdit.text().lower().capitalize()
            if not request:
                raise VoidLineEdit
            if btn.objectName() == 'find_tale':
                self.update_tales_table()
                result = cur.execute(f"SELECT tale.id, tale.title, tale.author, tale.description"
                                      f" FROM tale WHERE tale.title = '{request}'").fetchall()
            else:
                self.update_characters_table()
                result = cur.execute(f"SELECT characters.id, characters.name, tale.title"
                                     f" FROM characters"
                                     f" INNER JOIN tale ON tale.id = characters.tale"
                                     f" WHERE characters.name = '{request}'").fetchall()
            if not result:
                raise NotFoundResult

            self.statusbar.showMessage(f'Найдено {len(result)} элементов')
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        except VoidLineEdit:
            if btn.objectName() == 'find_tale':
                self.statusbar.showMessage(
                    'Для выполнения этого действия нужно ввести название сказки в поисковую строку')
            else:
                self.statusbar.showMessage(
                    'Для выполнения этого действия нужно ввести имя персонажа в поисковую строку')
        except NotFoundResult:
            if btn.objectName() == 'find_tale':
                self.statusbar.showMessage('Сказки с таким названием не найдено')
            else:
                self.statusbar.showMessage('Персонажа с таким именем не найдено')

    def ger_more_info(self):
        try:
            if self.radioButton_2.isChecked():
                raise NotFoundResult
            select_tale = self.tableWidget.selectedItems()
            if select_tale:
                self.second_form = InfoPage(self, select_tale[0].text())
                self.second_form.show()
            else:
                raise VoidLineEdit
        except NotFoundResult:
            self.statusbar.showMessage('Подробная информация есть только у сказок')
        except VoidLineEdit:
            self.statusbar.showMessage('Выберете сказку из таблицы')



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