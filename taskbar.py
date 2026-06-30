import sys
import subprocess
import os
import psutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QMenu, QAction, QFrame,
    QDesktopWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QTime, QDate, QPoint
from PyQt5.QtGui import QFont, QCursor

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def launch(script):
    subprocess.Popen([sys.executable, os.path.join(SCRIPT_DIR, script)])


class SystemTray(QWidget):
    """Battery / Network / Sound icons shown on the right side of the taskbar."""
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.setStyleSheet("""
            QLabel#tray {
                color: #cdd6f4;
                font-size: 19px;
                padding: 6px 10px;
                border-radius: 6px;
            }
            QLabel#tray:hover { background: rgba(255,255,255,0.1); }
        """)

        self.sound_lbl = QLabel("🔊")
        self.sound_lbl.setObjectName("tray")
        self.sound_lbl.setToolTip("Sound")
        self.sound_lbl.mousePressEvent = self._toggle_mute

        self.net_lbl = QLabel("📶")
        self.net_lbl.setObjectName("tray")
        self.net_lbl.setToolTip("Network")

        self.batt_lbl = QLabel("🔋")
        self.batt_lbl.setObjectName("tray")
        self.batt_lbl.setToolTip("Battery")

        layout.addWidget(self.sound_lbl)
        layout.addWidget(self.net_lbl)
        layout.addWidget(self.batt_lbl)

        self.muted = False

        timer = QTimer(self)
        timer.timeout.connect(self.refresh)
        timer.start(5000)
        self.refresh()

    def _toggle_mute(self, event):
        self.muted = not self.muted
        self.sound_lbl.setText("🔇" if self.muted else "🔊")

    def refresh(self):
        # Network status
        try:
            stats = psutil.net_if_stats()
            up = any(s.isup for name, s in stats.items() if name != "lo")
            self.net_lbl.setText("📶" if up else "📡")
            self.net_lbl.setToolTip("Connected" if up else "No connection")
        except Exception:
            self.net_lbl.setText("📶")

        # Battery status
        try:
            batt = psutil.sensors_battery()
            if batt is None:
                self.batt_lbl.setText("🔌")
                self.batt_lbl.setToolTip("Desktop (no battery)")
            else:
                pct = int(batt.percent)
                if batt.power_plugged:
                    icon = "🔌"
                elif pct >= 80:
                    icon = "🔋"
                elif pct >= 40:
                    icon = "🔋"
                elif pct >= 15:
                    icon = "🪫"
                else:
                    icon = "🪫"
                self.batt_lbl.setText(icon)
                self.batt_lbl.setToolTip(f"Battery: {pct}%" + (" (charging)" if batt.power_plugged else ""))
                self.batt_lbl.setText(f"{icon} {pct}%")
        except Exception:
            self.batt_lbl.setText("🔌")


class StartMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QWidget {
                background: #1e1e2e;
                border: 1px solid #444;
                border-radius: 8px;
            }
            QPushButton {
                background: transparent;
                color: #cdd6f4;
                text-align: left;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background: #0078d7; color: white; }
            QLabel {
                color: #888;
                font-size: 11px;
                padding: 8px 20px 4px 20px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 10, 6, 10)
        layout.setSpacing(2)

        title = QLabel("MY DEV OS")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet("color: #89b4fa; padding: 4px 14px 10px 14px;")
        layout.addWidget(title)

        apps = [
            ("📝  Notepad",       "notepad.py"),
            ("📊  Task Manager",  "taskmanager.py"),
            ("🏓  Pong",          "pong.py"),
        ]
        for label, script in apps:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, s=script: (launch(s), self.hide()))
            layout.addWidget(btn)

        layout.addSpacing(8)
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("border: none; border-top: 1px solid #333;")
        layout.addWidget(sep)
        layout.addSpacing(4)

        shutdown = QPushButton("⏻  Shut Down")
        shutdown.setStyleSheet("QPushButton { color: #f38ba8; } QPushButton:hover { background: #c0392b; color: white; }")
        shutdown.clicked.connect(QApplication.quit)
        layout.addWidget(shutdown)

        self.setFixedWidth(220)


class Taskbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, screen.height() - 64, screen.width(), 64)

        self.setStyleSheet("""
            QWidget#taskbar {
                background: rgba(20, 20, 35, 230);
                border-top: 1px solid #333;
            }
            QPushButton {
                background: transparent;
                color: #cdd6f4;
                border: none;
                padding: 10px 18px;
                font-size: 15px;
                border-radius: 6px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.1); }
            QPushButton#start {
                background: #0078d7;
                color: white;
                font-weight: bold;
                padding: 10px 22px;
                border-radius: 6px;
            }
            QPushButton#start:hover { background: #005fa3; }
            QLabel#clock {
                color: #cdd6f4;
                font-size: 15px;
                padding: 0 16px;
            }
        """)

        inner = QWidget(self)
        inner.setObjectName("taskbar")
        inner.setGeometry(0, 0, screen.width(), 64)

        layout = QHBoxLayout(inner)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        # Start button
        self.start_btn = QPushButton("⊞  Start")
        self.start_btn.setObjectName("start")
        self.start_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.start_btn.clicked.connect(self.toggle_start_menu)
        layout.addWidget(self.start_btn)

        layout.addSpacing(10)

        # Quick launch buttons
        for label, script in [
            ("📝 Notepad", "notepad.py"),
            ("📊 Tasks",   "taskmanager.py"),
            ("🏓 Pong",    "pong.py"),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, s=script: launch(s))
            layout.addWidget(btn)

        layout.addStretch()

        # System tray (sound / network / battery)
        self.tray = SystemTray()
        layout.addWidget(self.tray)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.VLine)
        sep2.setStyleSheet("border: none; border-left: 1px solid #444; margin: 0 6px;")
        layout.addWidget(sep2)

        # Date + Clock
        clock_box = QVBoxLayout()
        clock_box.setSpacing(0)
        clock_box.setContentsMargins(0, 0, 0, 0)

        self.clock = QLabel()
        self.clock.setObjectName("clock")
        self.clock.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.clock.setFont(QFont("Arial", 14))

        self.date_lbl = QLabel()
        self.date_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.date_lbl.setStyleSheet("color: #a6adc8; font-size: 11px; padding: 0 16px;")

        clock_box.addWidget(self.clock)
        clock_box.addWidget(self.date_lbl)
        layout.addLayout(clock_box)

        self.start_menu = StartMenu()

        timer = QTimer(self)
        timer.timeout.connect(self._update_clock)
        timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        self.clock.setText(QTime.currentTime().toString("hh:mm:ss"))
        self.date_lbl.setText(QDate.currentDate().toString("ddd, MMM d yyyy"))

    def toggle_start_menu(self):
        if self.start_menu.isVisible():
            self.start_menu.hide()
        else:
            btn_pos = self.start_btn.mapToGlobal(QPoint(0, 0))
            self.start_menu.adjustSize()
            self.start_menu.move(btn_pos.x(), btn_pos.y() - self.start_menu.height() - 4)
            self.start_menu.show()
            self.start_menu.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    taskbar = Taskbar()
    taskbar.show()
    sys.exit(app.exec_())