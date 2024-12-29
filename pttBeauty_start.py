# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 05:48:12 2022

@author: Alvin
"""

from PyQt5 import QtWidgets

from pttBeauty_controller import MainWindow

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())