import random
import time
import tkinter as tk
from enum import Enum


class Player(Enum):
    PLAYER1 = 1
    PLAYER2 = 2
    NO_PLAYER = 0


class Frame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.board = Board(self)
        # self.board.pack()


class Board(tk.Canvas):
    cell_size = 60
    margin = 7
    # cell_info = [
    #     [Player.NO_PLAYER, Player.PLAYER1, Player.NO_PLAYER, Player.NO_PLAYER, Player.NO_PLAYER, Player.NO_PLAYER],
    #     [Player.NO_PLAYER, Player.PLAYER1, Player.PLAYER1, Player.NO_PLAYER, Player.NO_PLAYER, Player.NO_PLAYER],
    #     [Player.NO_PLAYER, Player.NO_PLAYER, Player.PLAYER1, Player.PLAYER2, Player.PLAYER2, Player.PLAYER2],
    #     [Player.NO_PLAYER, Player.NO_PLAYER, Player.PLAYER2, Player.PLAYER2, Player.NO_PLAYER, Player.NO_PLAYER],
    #     [Player.NO_PLAYER, Player.NO_PLAYER, Player.NO_PLAYER, Player.PLAYER2, Player.NO_PLAYER, Player.NO_PLAYER],
    #     [Player.NO_PLAYER, Player.NO_PLAYER, Player.NO_PLAYER, Player.NO_PLAYER, Player.NO_PLAYER, Player.NO_PLAYER],
    # ]
    cell_info = [[Player.NO_PLAYER] * 6 for i in range(6)]
    player = Player.PLAYER1

    def __init__(self, master):
        width = len(self.cell_info) * self.cell_size + 1
        tk.Canvas.__init__(self, master, relief=tk.RAISED, bd=4, bg='green', width=width, height=width)
        self.cell_info[2][2] = Player.PLAYER1
        self.cell_info[3][3] = Player.PLAYER1
        self.cell_info[2][3] = Player.PLAYER2
        self.cell_info[3][2] = Player.PLAYER2

        self.grid(column=0, row=0)

        self.info_frame = tk.Frame(master, width=500)
        self.info_frame.grid(column=1, row=0, sticky=tk.W+tk.E)

        self.player_label = tk.Label(self.info_frame, text="Player1")
        self.player_label.grid(column=0, row=0)
        self.info_label = tk.Label(self.info_frame, text="info")
        self.info_label.grid(column=0, row=1)

        self.bind("<Button-1>", self.user_input)
        self.bind("<Button-2>", self.com_input)
        self.refresh()

    def user_input(self, event):
        # self.print_board()
        if self.player != Player.PLAYER1:
            return
        x = event.x - self.margin
        y = event.y - self.margin
        px = x // self.cell_size
        py = y // self.cell_size
        l = self.can_put_list(self.player)
        if not (px, py) in l:
            self.info_label["text"] = "can not put there"
            return
        self.cell_info[px][py] = Player.PLAYER1
        self.put((px, py), self.player)
        self.player = Player.PLAYER2
        self.player_label["text"] = "Player2"
        self.refresh()
        self.com_input()

    def com_input(self):
        time.sleep(0.5)
        if self.player != Player.PLAYER2:
            return
        l = self.can_put_list(Player.PLAYER2)
        if len(l) == 0:
            self.info_label["text"] = "Player2 can not put"
            self.player = Player.PLAYER1
            self.player_label["text"] = "Player1"
            return
        p = random.choice(l)
        self.cell_info[p[0]][p[1]] = Player.PLAYER2
        self.put(p, self.player)
        self.player = Player.PLAYER1
        self.player_label["text"] = "Player1"
        self.refresh()

    def can_put_list(self, player):
        out = []
        for i in range(6):
            for j in range(6):
                if self.can_put((i, j), player):
                    out.append((i, j))
        # print(out)
        return out

    def can_put(self, point, player):
        if self.cell_info[point[0]][point[1]] != Player.NO_PLAYER:
            return False
        vec = [
            (1, 1),
            (1, 0),
            (1, -1),
            (0, 1),
            (0, -1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
        ]
        for v in vec:
            try:
                if point[0]+v[0] < 0 or point[1]+v[1] < 0:
                    raise IndexError
                if self.cell_info[point[0]+v[0]][point[1]+v[1]] == Player.NO_PLAYER:
                    continue
                if self.cell_info[point[0]+v[0]][point[1]+v[1]] == player:
                    continue
            except IndexError:
                continue
            for i in range(2, 6):
                try:
                    if point[0] + v[0]*i < 0 or point[1] + v[1]*i < 0:
                        raise IndexError
                    if self.cell_info[point[0] + v[0]*i][point[1] + v[1]*i] == player and self.cell_info[point[0] + v[0]*i][point[1] + v[1]*i] != Player.NO_PLAYER:
                        return True
                    if self.cell_info[point[0] + v[0]*i][point[1] + v[1]*i] == Player.NO_PLAYER:
                        break
                except IndexError:
                    break
        return False

    def put(self, point, player):
        vec = [
            (1, 1),
            (1, 0),
            (1, -1),
            (0, 1),
            (0, -1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
        ]
        change_points = []
        for v in vec:
            buf = []
            try:
                if point[0]+v[0] < 0 or point[1]+v[1] < 0:
                    raise IndexError
                if self.cell_info[point[0]+v[0]][point[1]+v[1]] == Player.NO_PLAYER:
                    continue
                if self.cell_info[point[0]+v[0]][point[1]+v[1]] == player:
                    continue
            except IndexError:
                continue
            buf.append((point[0]+v[0], point[1]+v[1]))
            for i in range(2, 6):
                try:
                    if point[0] + v[0]*i < 0 or point[1] + v[1]*i < 0:
                        raise IndexError
                    if self.cell_info[point[0] + v[0]*i][point[1] + v[1]*i] == player and self.cell_info[point[0] + v[0]*i][point[1] + v[1]*i] != Player.NO_PLAYER:
                        change_points += buf
                        break
                    if self.cell_info[point[0] + v[0]*i][point[1] + v[1]*i] == Player.NO_PLAYER:
                        break
                except IndexError:
                    break
                buf.append((point[0] + v[0]*i, point[1] + v[1]*i))

        # print(change_points)
        for p in change_points:
            self.cell_info[p[0]][p[1]] = player

    def refresh(self):
        for i in range(6):
            for j in range(6):
                x0 = i * self.cell_size + self.margin
                y0 = j * self.cell_size + self.margin
                self.create_rectangle(x0, y0, x0 + self.cell_size, y0 + self.cell_size, fill="green")
                if self.cell_info[i][j] == Player.PLAYER1:
                    self.create_oval(x0 + 2, y0 + 2, x0 + self.cell_size - 2, y0 + self.cell_size - 2, fill="white")
                elif self.cell_info[i][j] == Player.PLAYER2:
                    self.create_oval(x0 + 2, y0 + 2, x0 + self.cell_size - 2, y0 + self.cell_size - 2, fill="black")

        l = self.can_put_list(self.player)
        for i in l:
            x0 = i[0] * self.cell_size + self.margin
            y0 = i[1] * self.cell_size + self.margin
            x = x0 + self.cell_size
            y = y0 + self.cell_size
            if self.player == Player.PLAYER1:
                self.create_rectangle(x0, y0, x, y, fill="red")
            else:
                self.create_rectangle(x0, y0, x, y, fill="blue")
        player1 = self.can_put_list(Player.PLAYER1)
        player2 = self.can_put_list(Player.PLAYER2)
        if len(player1) == 0 and len(player2) == 0:
            self.end()

    def end(self):
        p1 = 0
        p2 = 0
        for row in self.cell_info:
            for e in row:
                if e == Player.PLAYER1:
                    p1 += 1
                elif e == Player.PLAYER2:
                    p2 += 1

        if p1 > p2:
            win = "Player1"
        elif p2 > p1:
            win = "Player2"
        else:
            win = "Draw"
        self.info_label["text"] = f"Player1: {p1}\nPlayer2: {p2}\n{win}"

    def print_board(self):
        for i in range(6):
            for j in range(6):
                print(self.cell_info[j][i].value, end=" ")
            print()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("othello")
    root.geometry("500x500")
    frame = Frame(master=root)
    frame.mainloop()
