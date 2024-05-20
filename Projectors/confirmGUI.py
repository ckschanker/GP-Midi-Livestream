import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from pypjlink import Projector

projector_left = "192.168.110.34"
projector_center = "192.168.110.35"
projector_right = "192.168.110.36"

def commandAll(command):
    try:
        with Projector.from_address(projector_left) as projector:
            projector.authenticate()
            projector.set_power(command)

        with Projector.from_address(projector_center) as projector:
            projector.authenticate()
            projector.set_power(command)

        with Projector.from_address(projector_right) as projector:
            projector.authenticate()
            projector.set_power(command)
    except Exception as e:
        print(f"Errored with Exception: {e}")

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        button1 = QPushButton("Turn Projectors On", self)
        button2 = QPushButton("Turn Projectors Off", self)

        # Connect the buttons to their respective callback functions
        button1.clicked.connect(self.on_button1_click)
        button2.clicked.connect(self.on_button2_click)

        layout.addWidget(button1)
        layout.addWidget(button2)


        self.setLayout(layout)
        self.setWindowTitle("Two Buttons with Confirmation")
        self.show()

    def on_button1_click(self):
        result = QMessageBox.information(self, "Confirmation", "Are you sure you want to turn projectors on?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            commandAll('on')
            print("Turned Projectors On")

    def on_button2_click(self):
        result = QMessageBox.information(self, "Confirmation", "Are you sure you want to turn projectors off?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            commandAll('off')
            print("Turned Projectors Off")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())