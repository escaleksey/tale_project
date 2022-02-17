from design_more_info_page import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from io import BytesIO
from PyQt5.QtGui import QPixmap
import sys
import sqlite3
from PIL import Image


class InfoPage(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('data/tales_db.db')
        self.initUi(args[-1])


    def initUi(self, tale_id):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT tale.title, tale.author, tale.picture, tale.description
                                 FROM tale WHERE id='{tale_id}'""").fetchone()
        characters = cur.execute(f"""SELECT characters.name
                                 FROM characters WHERE tale='{tale_id}'""").fetchall()
        self.tale_id = tale_id
        print(tale_id)
        self.title.setText(str(result[0]))
        self.author.setText(str(result[1]))
        self.text_description.setText(str(result[3]))
        characters = ', '.join(elem[0] for elem in characters)
        self.characters.setText(characters)
        image =  Image.open(result[2])
        image = image.resize((300, 300))
        image.save('data/image/exit_picture.png')
        self.pixmap = QPixmap('data/image/exit_picture.png')
        self.image.setPixmap(self.pixmap)
        self.delete_btn.clicked.connect(self.delete)

    def delete(self):
        valid = QMessageBox.question(self, '', f"Вы действительно хотите удалить это растение из базы данных?",
                                     QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM tale WHERE id = {self.tale_id}")
            self.con.commit()
            cur.execute(f"DELETE FROM characters WHERE tale = {self.tale_id}")
            self.con.commit()
            self.con.close()
            self.hide()


sys.__excepthook__ = sys.__excepthook__


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = InfoPage(1)
    ex.show()
    sys.exit(app.exec_())
