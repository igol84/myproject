from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtWidgets import QCompleter


class CustomQCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.local_completion_prefix = ""
        self.source_model = None

    def setModel(self, model):
        self.source_model = model
        super().setModel(self.source_model)

    def updateModel(self):
        local_completion_prefix = self.local_completion_prefix

        class InnerProxyModel(QSortFilterProxyModel):
            def filterAcceptsRow(self, sourceRow, sourceParent):
                index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
                return local_completion_prefix.lower() in self.sourceModel().data(index0).lower()

        proxy_model = InnerProxyModel()
        proxy_model.setSourceModel(self.source_model)
        super(CustomQCompleter, self).setModel(proxy_model)

    def splitPath(self, path):
        self.local_completion_prefix = path
        self.updateModel()
        return []


if __name__ == '__main__':
    import sys

    from PySide6 import QtWidgets
    from PySide6.QtWidgets import QComboBox

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setWindowTitle("QSlider")
    window.resize(300, 200)

    combobox = QtWidgets.QComboBox()
    combobox.addItems(["", "Lola", "Lila", "Cola 70", 'Coca 70'])
    combobox.setEditable(True)
    combobox.setInsertPolicy(QComboBox.NoInsert)

    completer = CustomQCompleter(combobox)
    completer.setCompletionMode(QCompleter.PopupCompletion)
    completer.setModel(combobox.model())

    combobox.setCompleter(completer)

    h_box = QtWidgets.QHBoxLayout()
    h_box.addWidget(combobox)
    window.setLayout(h_box)

    window.show()
    sys.exit(app.exec())
