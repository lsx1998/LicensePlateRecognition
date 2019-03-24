# -*- coding: utf-8 -*-
from Window import MyWindow
import sys
from PyQt5.QtWidgets import QApplication




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
