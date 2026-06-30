# My Dev OS

This is a little desktop environment I built using Python and PyQt5. It's not a real
operating system (no kernel, no bootloader) — it's a desktop shell that runs on top of
whatever OS you already have. It has a desktop with icons, a taskbar with a start menu,
a notepad, a task manager, and a Pong game.

## What you need

- Python 3.8 or newer
- PyQt5
- psutil

Install both with:

```bash
pip install PyQt5 psutil
```

## Running it

To start the whole thing (desktop + taskbar):

```bash
python3 main.py
```

If you just want one app without the rest, you can run any of them on their own:

```bash
python3 notepad.py
python3 taskmanager.py
python3 pong.py
```

## Setting a wallpaper

Put an image in the project folder and name it `wallpaper.jpg`. It'll stretch to fill
the screen automatically. If there's no `wallpaper.jpg` there, it just uses a dark blue
gradient instead.

## The apps

**Notepad** — basic text editor. Open, save, save as, the usual shortcuts (Ctrl+S,
Ctrl+O, etc.) all work.

**Task Manager** — shows CPU and RAM usage, plus a list of running processes. You can
select one and hit "End Task" to kill it. Refreshes every couple seconds.

**Pong** — two player, same keyboard. Player 1 uses W/S, player 2 uses the arrow keys.
Space pauses the game, and also restarts it once someone wins. First to 7 points takes it.

## Desktop and taskbar

Double-click the icons on the desktop to open an app. The taskbar at the bottom has a
Start button (click it for a small menu with all the apps plus a shut down option),
quick-launch buttons for each app, and on the right side there's sound/network/battery
icons plus a clock.

## Files

```
devos/
├── main.py          - run this to start everything
├── desktop.py        - background + icons
├── taskbar.py         - taskbar, start menu, tray icons, clock
├── notepad.py         - text editor
├── taskmanager.py      - process monitor
├── pong.py              - the game

this was my mini dev os



