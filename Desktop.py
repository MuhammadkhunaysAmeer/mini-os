import os
import sys
import subprocess
import PyQt5.QtWidgets as QtWidgets

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QGridLayout, QDesktopWidget, QPushButton
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QSize
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WALLPAPER_PATH = os.path.join(SCRIPT_DIR, "wallpaper.jpg")  # drop your image here
 
 
def launch(script):
    subprocess.Popen([sys.executable, os.path.join(SCRIPT_DIR, script)])
 
 
class DesktopIcon(QWidget):
    def __init__(self, label, emoji, script):
        super().__init__()
        self.script = script
        self.setFixedSize(90, 90)
        self.setStyleSheet("""
            QWidget { background: transparent; }
            QWidget:hover { background: rgba(255,255,255,0.15); border-radius: 8px; }
        """)
 
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 6, 4, 4)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignCenter)
 
        icon_lbl = QLabel(emoji)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setFont(QFont("Arial", 28))
        icon_lbl.setStyleSheet("background: transparent;")
 
        text_lbl = QLabel(label)
        text_lbl.setAlignment(Qt.AlignCenter)
        text_lbl.setFont(QFont("Arial", 9))
        text_lbl.setStyleSheet("""
            color: white;
            background: transparent;
        """)
        text_lbl.setWordWrap(True)
 
        layout.addWidget(icon_lbl)
        layout.addWidget(text_lbl)
 
    def mouseDoubleClickEvent(self, event):
        launch(self.script)
 
 
class Desktop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
 
        screen = QDesktopWidget().screenGeometry()
        # Leave room for the taskbar (64px) at the bottom
        self.setGeometry(0, 0, screen.width(), screen.height() - 64)
 
        self._set_background()
 
        grid = QGridLayout(self)
        grid.setContentsMargins(20, 20, 20, 20)
        grid.setSpacing(10)
        grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
 
        icons = [
            ("Notepad",       "📝", "notepad.py"),
            ("Task Manager",  "📊", "taskmanager.py"),
            ("Pong",          "🏓", "pong.py"),
        ]
        for row, (label, emoji, script) in enumerate(icons):
            grid.addWidget(DesktopIcon(label, emoji, script), row, 0)
 
    def _set_background(self):
        if os.path.exists(WALLPAPER_PATH):
            pixmap = QPixmap(WALLPAPER_PATH)
            screen = QDesktopWidget().screenGeometry()
            scaled = pixmap.scaled(
                screen.width(), screen.height(),
                Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        else:
            # Fallback gradient if no wallpaper.jpg is found
            self.setStyleSheet("""
                Desktop {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 #0d0d2e, stop:1 #1a1a3e
                    );
                }
            """)
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = Desktop()
    desktop.show()
    sys.exit(app.exec_())