import sys
from PySide6 import QtWidgets, QtCore
class Example(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.combo = QtWidgets.QComboBox(self)
        self.combo.setEditable(True)
        self.combo.editTextChanged.connect(self.findText)
        self.combo.addItems([u"Петров", u"Сидоров", u"Иванов", u"Ивановa"])
    def findText(self, s):
        index=self.combo.findText(s)
        if index > -1:
            self.combo.setCurrentIndex(index)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())