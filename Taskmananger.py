import sys
import psutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QHeaderView, QProgressBar
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(200, 150, 800, 560)
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #1e1e2e; color: #cdd6f4; }
            QTableWidget {
                background: #181825;
                color: #cdd6f4;
                gridline-color: #313244;
                border: none;
                font-size: 12px;
            }
            QTableWidget::item:selected { background: #0078d7; color: white; }
            QHeaderView::section {
                background: #313244;
                color: #cdd6f4;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QPushButton {
                background: #c0392b;
                color: white;
                border: none;
                padding: 7px 18px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover { background: #e74c3c; }
            QPushButton:disabled { background: #555; color: #999; }
            QLabel { font-size: 12px; color: #a6adc8; }
            QProgressBar {
                background: #313244;
                border: none;
                border-radius: 3px;
                height: 14px;
                text-align: center;
                color: white;
                font-size: 10px;
            }
            QProgressBar::chunk { background: #0078d7; border-radius: 3px; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # System stats bar
        stats_layout = QHBoxLayout()
        self.cpu_bar = self._make_stat("CPU", stats_layout)
        self.ram_bar = self._make_stat("RAM", stats_layout)
        layout.addLayout(stats_layout)

        # Process table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "RAM MB"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Bottom buttons
        btn_layout = QHBoxLayout()
        self.kill_btn = QPushButton("⛔ End Task")
        self.kill_btn.clicked.connect(self.kill_process)
        self.kill_btn.setEnabled(False)
        btn_layout.addStretch()
        btn_layout.addWidget(self.kill_btn)
        layout.addLayout(btn_layout)

        self.table.itemSelectionChanged.connect(
            lambda: self.kill_btn.setEnabled(bool(self.table.selectedItems()))
        )

        # Refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000)
        self.refresh()

    def _make_stat(self, label, parent_layout):
        col = QVBoxLayout()
        lbl = QLabel(label)
        lbl.setAlignment(Qt.AlignCenter)
        bar = QProgressBar()
        bar.setRange(0, 100)
        col.addWidget(lbl)
        col.addWidget(bar)
        parent_layout.addLayout(col)
        return bar

    def refresh(self):
        self.cpu_bar.setValue(int(psutil.cpu_percent()))
        self.cpu_bar.setFormat(f"CPU  {psutil.cpu_percent():.1f}%")
        ram = psutil.virtual_memory()
        self.ram_bar.setValue(int(ram.percent))
        self.ram_bar.setFormat(f"RAM  {ram.percent:.1f}%")

        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                procs.append(p.info)
            except Exception:
                pass
        procs.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(procs))
        for row, p in enumerate(procs):
            ram_mb = (p['memory_info'].rss / 1024 / 1024) if p['memory_info'] else 0
            vals = [str(p['pid']), p['name'] or '?',
                    f"{p['cpu_percent']:.1f}", f"{ram_mb:.1f}"]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 2 and float(val) > 20:
                    item.setForeground(QColor("#f38ba8"))
                self.table.setItem(row, col, item)
        self.table.setSortingEnabled(True)

    def kill_process(self):
        row = self.table.currentRow()
        if row < 0:
            return
        pid = int(self.table.item(row, 0).text())
        try:
            psutil.Process(pid).terminate()
        except Exception as e:
            print(f"Could not kill {pid}: {e}")
        self.refresh()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TaskManager()
    win.show()
    sys.exit(app.exec_())