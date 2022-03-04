def clearLayout(cur_lay):
    if cur_lay is not None:
        while cur_lay.count():
            item = cur_lay.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clearLayout(item.layout())
