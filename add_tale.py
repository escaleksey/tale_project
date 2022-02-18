from design_add_tale_page import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
import sqlite3
import sys
from PIL import Image


class VoidNameEdit(Exception):
    pass


class VoidCharacterEdit(Exception):
    pass


class VoidDescriptionEdit(Exception):
    pass


class AddTalePage(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('data/tales_db.db')
        self.initUi()

    def initUi(self):
        cur = self.con.cursor()
        self.select_picture.clicked.connect(self.select_image)
        self.cancel.clicked.connect(self.cancel_func)
        self.ok_btn.clicked.connect(self.ok_pressed)
        self.image_path = ''
        self.ids = cur.execute("""SELECT id FROM tale""").fetchall()
        self.ids = list(map(lambda x: x[0], self.ids))

    def cancel_func(self):
        self.hide()

    def select_image(self):
        self.image_path = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.jpg);;Картинка (*.png)')[0]
        pil_image = Image.open(self.image_path)
        pil_image = pil_image.resize((260, 180))
        pil_image.save('data/image/exit_picture.png')
        self.pixmap = QPixmap('data/image/exit_picture.png')
        self.image.setPixmap(self.pixmap)

    def ok_pressed(self):
        cur = self.con.cursor()
        name = self.name.text()
        description = self.description.toPlainText()
        characters = self.characters_text_edit.toPlainText()
        author = self.author.text()
        try:
            if not name:
                raise VoidNameEdit
            if not description:
                raise VoidDescriptionEdit
            if not characters:
                raise VoidCharacterEdit
            if not author:
                author = '-'
            characters = [elem.strip() for elem in characters.split(',')]
            cur.execute(f"INSERT INTO tale(id, title, author, picture, description)"
                        f" VALUES({self.ids[-1] + 1}, '{str(name)}', '{str(author)}',"
                        f" '{str(self.image_path)}', '{str(description)}')")
            self.con.commit()
            id_tale = cur.execute(f"""SELECT id FROM tale WHERE title='{name}'""").fetchone()
            print(id_tale)
            for elem in characters:
                cur.execute(f"INSERT INTO characters(name, tale)"
                            f" VALUES('{str(elem)}', {id_tale[0]})")
                print(elem)
            self.con.commit()
            self.con.close()
            self.hide()
        except VoidNameEdit:
            self.statusbar.showMessage('Введите название сказки')
        except VoidDescriptionEdit:
            self.statusbar.showMessage('Введите описание сказки')
        except VoidCharacterEdit:
            self.statusbar.showMessage('Введите главных героев сказки')


sys.__excepthook__ = sys.__excepthook__


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AddTalePage()
    ex.show()
    sys.exit(app.exec_())
