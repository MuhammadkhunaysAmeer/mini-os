"""a working notepad which can runnnnnnnnn note your thingd heck yea"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit,
    QAction, QFileDialog, QMessageBox, QMenuBar
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.setWindowTitle("Notepad")
        self.setGeometry(200, 200, 700, 500)
        self.setStyleSheet("""
            QMainWindow { background: #f0f0f0; }
            QTextEdit {
                background: white;
                color: #1a1a1a;
                font-family: Consolas, monospace;
                font-size: 13px;
                border: none;
                padding: 8px;
            }
            QMenuBar {
                background: #e8e8e8;
                color: #1a1a1a;
                border-bottom: 1px solid #ccc;
            }
            QMenuBar::item:selected { background: #0078d7; color: white; }
            QMenu { background: white; border: 1px solid #ccc; }
            QMenu::item:selected { background: #0078d7; color: white; }
        """)

        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 13))
        self.setCentralWidget(self.editor)

        self._build_menu()

    def _build_menu(self):
        mb = self.menuBar()

        # File menu
        file_menu = mb.addMenu("File")
        for label, shortcut, func in [
            ("New",       "Ctrl+N", self.new_file),
            ("Open...",   "Ctrl+O", self.open_file),
            ("Save",      "Ctrl+S", self.save_file),
            ("Save As..","Ctrl+Shift+S", self.save_as),
            ("Exit",      "Alt+F4", self.close),
        ]:
            act = QAction(label, self)
            act.setShortcut(shortcut)
            act.triggered.connect(func)
            file_menu.addAction(act)

        # Edit menu
        edit_menu = mb.addMenu("Edit")
        for label, shortcut, func in [
            ("Undo",  "Ctrl+Z", self.editor.undo),
            ("Redo",  "Ctrl+Y", self.editor.redo),
            ("Cut",   "Ctrl+X", self.editor.cut),
            ("Copy",  "Ctrl+C", self.editor.copy),
            ("Paste", "Ctrl+V", self.editor.paste),
            ("Select All", "Ctrl+A", self.editor.selectAll),
        ]:
            act = QAction(label, self)
            act.setShortcut(shortcut)
            act.triggered.connect(func)
            edit_menu.addAction(act)

    def new_file(self):
        if self._confirm_discard():
            self.editor.clear()
            self.current_file = None
            self.setWindowTitle("Notepad")

    def open_file(self):
        if not self._confirm_discard():
            return
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if path:
            with open(path, "r") as f:
                self.editor.setPlainText(f.read())
            self.current_file = path
            self.setWindowTitle(f"Notepad — {path}")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as f:
                f.write(self.editor.toPlainText())
        else:
            self.save_as()

    def save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt);;All Files (*)")
        if path:
            self.current_file = path
            self.save_file()
            self.setWindowTitle(f"Notepad — {path}")

    def _confirm_discard(self):
        if self.editor.document().isModified():
            r = QMessageBox.question(self, "Unsaved Changes",
                "You have unsaved changes. Discard them?",
                QMessageBox.Yes | QMessageBox.No)
            return r == QMessageBox.Yes
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Notepad()
    win.show()
    sys.exit(app.exec_())
    """this is the end for this py file"""