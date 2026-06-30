import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QTimer, QRect


class PongWidget(QWidget):
    W, H = 800, 500
    PAD_W, PAD_H = 12, 80
    BALL = 12
    SPEED = 5

    def __init__(self):
        super().__init__()
        self.setFixedSize(self.W, self.H)
        self.setFocusPolicy(Qt.StrongFocus)
        self._reset()
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)  # ~60fps

    def _reset(self):
        self.ball_x = self.W // 2
        self.ball_y = self.H // 2
        angle = random.choice([-1, 1])
        self.ball_dx = self.SPEED * angle
        self.ball_dy = self.SPEED * random.choice([-1, 1])
        self.p1_y = self.H // 2 - self.PAD_H // 2
        self.p2_y = self.H // 2 - self.PAD_H // 2
        self.score1 = 0
        self.score2 = 0
        self.paused = False
        self.winner = None
        self.keys = set()

    def _tick(self):
        if self.paused or self.winner:
            return

        # Move paddles
        if Qt.Key_W in self.keys:
            self.p1_y = max(0, self.p1_y - 6)
        if Qt.Key_S in self.keys:
            self.p1_y = min(self.H - self.PAD_H, self.p1_y + 6)
        if Qt.Key_Up in self.keys:
            self.p2_y = max(0, self.p2_y - 6)
        if Qt.Key_Down in self.keys:
            self.p2_y = min(self.H - self.PAD_H, self.p2_y + 6)

        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Wall bounce (top/bottom)
        if self.ball_y <= 0 or self.ball_y >= self.H - self.BALL:
            self.ball_dy *= -1

        # Paddle 1 collision (left)
        if (self.ball_x <= 30 + self.PAD_W and
                self.p1_y <= self.ball_y <= self.p1_y + self.PAD_H):
            self.ball_dx = abs(self.ball_dx)
            offset = (self.ball_y - (self.p1_y + self.PAD_H / 2)) / (self.PAD_H / 2)
            self.ball_dy = offset * self.SPEED * 1.2

        # Paddle 2 collision (right)
        if (self.ball_x >= self.W - 30 - self.PAD_W - self.BALL and
                self.p2_y <= self.ball_y <= self.p2_y + self.PAD_H):
            self.ball_dx = -abs(self.ball_dx)
            offset = (self.ball_y - (self.p2_y + self.PAD_H / 2)) / (self.PAD_H / 2)
            self.ball_dy = offset * self.SPEED * 1.2

        # Scoring
        if self.ball_x < 0:
            self.score2 += 1
            self._serve()
        elif self.ball_x > self.W:
            self.score1 += 1
            self._serve()

        if self.score1 >= 7:
            self.winner = "Player 1"
        elif self.score2 >= 7:
            self.winner = "Player 2"

        self.update()

    def _serve(self):
        self.ball_x = self.W // 2
        self.ball_y = self.H // 2
        self.ball_dx = self.SPEED * random.choice([-1, 1])
        self.ball_dy = self.SPEED * random.choice([-1, 1])

    def keyPressEvent(self, e):
        self.keys.add(e.key())
        if e.key() == Qt.Key_Space:
            if self.winner:
                self._reset()
            else:
                self.paused = not self.paused

    def keyReleaseEvent(self, e):
        self.keys.discard(e.key())

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Background
        p.fillRect(0, 0, self.W, self.H, QColor("#0d0d1a"))

        # Centre dashed line
        pen = QPen(QColor("#333355"), 2, Qt.DashLine)
        p.setPen(pen)
        p.drawLine(self.W // 2, 0, self.W // 2, self.H)

        # Paddles
        p.setBrush(QColor("#0078d7"))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(30, self.p1_y, self.PAD_W, self.PAD_H, 4, 4)
        p.drawRoundedRect(self.W - 30 - self.PAD_W, self.p2_y, self.PAD_W, self.PAD_H, 4, 4)

        # Ball
        p.setBrush(QColor("white"))
        p.drawEllipse(int(self.ball_x), int(self.ball_y), self.BALL, self.BALL)

        # Score
        p.setPen(QColor("white"))
        p.setFont(QFont("Arial", 36, QFont.Bold))
        p.drawText(QRect(0, 20, self.W // 2, 60), Qt.AlignCenter, str(self.score1))
        p.drawText(QRect(self.W // 2, 20, self.W // 2, 60), Qt.AlignCenter, str(self.score2))

        # Labels
        p.setFont(QFont("Arial", 10))
        p.setPen(QColor("#888"))
        p.drawText(20, self.H - 10, "W/S — Player 1")
        p.drawText(self.W - 120, self.H - 10, "↑/↓ — Player 2")
        p.drawText(self.W // 2 - 60, self.H - 10, "SPACE — Pause")

        # Pause overlay
        if self.paused:
            p.fillRect(0, 0, self.W, self.H, QColor(0, 0, 0, 140))
            p.setPen(QColor("white"))
            p.setFont(QFont("Arial", 40, QFont.Bold))
            p.drawText(QRect(0, 0, self.W, self.H), Qt.AlignCenter, "PAUSED")

        # Winner overlay
        if self.winner:
            p.fillRect(0, 0, self.W, self.H, QColor(0, 0, 0, 160))
            p.setPen(QColor("#FFD700"))
            p.setFont(QFont("Arial", 44, QFont.Bold))
            p.drawText(QRect(0, 0, self.W, self.H - 60), Qt.AlignCenter, f"🏆 {self.winner} Wins!")
            p.setPen(QColor("white"))
            p.setFont(QFont("Arial", 16))
            p.drawText(QRect(0, 0, self.W, self.H + 80), Qt.AlignCenter, "Press SPACE to play again")


class PongWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pong")
        self.setCentralWidget(PongWidget())
        self.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PongWindow()
    win.show()
    sys.exit(app.exec_())
#the end of this pong game and it functions great lalalalalal huehuehueheue yeeeeeeeeeeee