from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pypjlink import Projector

import sys, os

projector_left = "192.168.110.34"
projector_right = "192.168.110.36"

basedir = os.path.dirname(__file__)

def commandAll(command):
    try:
        pass
        with Projector.from_address(projector_left) as projector:
            projector.authenticate()
            projector.set_power(command)

        with Projector.from_address(projector_right) as projector:
            projector.authenticate()
            projector.set_power(command)
    except Exception as e:
        print(f"Errored with Exception: {e}")

def projTurnOn():
    commandAll('on')

def projTurnOff():
    result = QMessageBox.information(None, "Confirmation", "Are you sure you want to turn projectors off?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if result == QMessageBox.Yes:
        commandAll('off')

if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Create the icon
    
    icon = QIcon(os.path.join(basedir, "icons", "menuIcon.png"))

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Create the menu
    menu = QMenu()
    projOn = QAction("Projectors On")
    projOn.triggered.connect(projTurnOn)
    menu.addAction(projOn)

    projOff = QAction("Projectors Off")
    projOff.triggered.connect(projTurnOff)
    menu.addAction(projOff)

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)

    app.exec_()