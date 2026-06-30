# 🖥️ My Dev OS

A custom desktop environment built entirely in Python + PyQt5. Includes a desktop
with wallpaper and icons, a Windows-style taskbar with a Start menu and system tray,
a Notepad, a Task Manager, and a two-player Pong game.

---

## 📦 Requirements

- Python 3.8+
- PyQt5
- psutil

Install dependencies:

```bash
pip install PyQt5 psutil
```

---

## 🚀 Running

Launch the full desktop environment (desktop background + taskbar):

```bash
python3 main.py
```

This opens:
- The **desktop** — background + double-clickable app icons
- The **taskbar** — Start button, quick-launch icons, system tray, clock

### Run apps individually
You can also launch any app on its own without the full desktop:

```bash
python3 notepad.py       # Text editor
python3 taskmanager.py   # Process / CPU / RAM monitor
python3 pong.py          # Two-player Pong
```

---

## 🖼️ Setting a Wallpaper

Drop an image named exactly **`wallpaper.jpg`** into the project folder (same folder
as `main.py`). It will automatically scale to fill the screen.

If no `wallpaper.jpg` is found, the desktop falls back to a dark blue gradient.

---

## 🧩 Apps

### 📝 Notepad
A simple text editor.
- File menu: New, Open, Save, Save As, Exit
- Edit menu: Undo, Redo, Cut, Copy, Paste, Select All
- Standard keyboard shortcuts (Ctrl+S, Ctrl+O, etc.)

### 📊 Task Manager
Live system monitor.
- Real-time CPU % and RAM % bars
- Sortable process table (PID, Name, CPU %, RAM MB)
- Select a process and click **End Task** to terminate it
- Auto-refreshes every 2 seconds

### 🏓 Pong
Two-player Pong.

| Key | Action |
|-----|--------|
| W / S | Player 1 (left paddle) |
| ↑ / ↓ | Player 2 (right paddle) |
| SPACE | Pause / Resume |
| SPACE (after a win) | Start a new game |

First to **7 points** wins.

---

## 🖱️ Desktop & Taskbar

**Desktop icons** — double-click to launch Notepad, Task Manager, or Pong.

**Taskbar (bottom of screen):**
- **⊞ Start** — opens a Start menu with all apps + Shut Down
- **Quick-launch buttons** — one click to open Notepad, Task Manager, or Pong
- **System tray** — 🔊 sound (click to mute/unmute), 📶 network status, 🔋 battery %
- **Clock** — live time + date, updates every second

---

## 📁 Project Structure

```
devos/
├── main.py          ← Launches the full desktop environment (start here)
├── desktop.py        ← Desktop background + app icons
├── taskbar.py         ← Taskbar, Start menu, system tray, clock
├── notepad.py         ← Text editor
├── taskmanager.py      ← Process / CPU / RAM monitor
├── pong.py              ← Two-player Pong game
├── wallpaper.jpg         ← (optional) your custom background image
└── README.md
```

---

## 💡 Ideas for What's Next

- A calculator app
- A file explorer
- A settings panel (change wallpaper, accent color, etc.)
- Auto-start on boot (Linux: add to `.xinitrc` or a systemd user service)
- More games (Snake, Minesweeper, etc.)

Just ask and we'll build it!
