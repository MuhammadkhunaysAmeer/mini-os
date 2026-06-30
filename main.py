import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from taskbar import Taskbar
from Desktop import Desktop 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("My Dev OS")
    taskbar = Taskbar()
    desktop = Desktop()
    desktop.show()
    taskbar.show()
    sys.exit(app.exec_())

