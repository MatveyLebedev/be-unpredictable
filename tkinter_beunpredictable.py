# задача игрока быть непредсказуемым для нейросети
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow import Variable
import numpy as np
import tkinter as tk

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}

difficulty = 0  # {0 - easy, 1 - hard}

root = tk.Tk()
frame = tk.Frame(root)
root.title('beunpredicteble')

b1 = tk.Button(text="1", bg='grey', width=15, height=6)
b2 = tk.Button(text="2", bg='grey', width=15, height=6)
b3 = tk.Button(text="3", bg='grey', width=15, height=6)
b4 = tk.Button(text="4", bg='grey', width=15, height=6)
b5 = tk.Button(text="5", bg='grey', width=15, height=6)
b6 = tk.Button(text="6", bg='grey', width=15, height=6)
b7 = tk.Button(text="7", bg='grey', width=15, height=6)
b8 = tk.Button(text="8", bg='grey', width=15, height=6)
b9 = tk.Button(text="9", bg='grey', width=15, height=6)

caunter = tk.Label(bg='yellow', fg='black')
l = tk.Label(bg='white', fg='black', width=58, height=3)

caunter.grid(row=0, column=2,  columnspan=2)
l.grid(row=1, columnspan=4)


b7.grid(row=2, column=0, pady=15)
b8.grid(row=2, column=1, pady=10)
b9.grid(row=2, column=2, pady=10)
b4.grid(row=3, column=0, pady=10)
b5.grid(row=3, column=1, pady=10)
b6.grid(row=3, column=2, pady=10)
b1.grid(row=4, column=0, pady=10)
b2.grid(row=4, column=1, pady=10)
b3.grid(row=4, column=2, pady=10)


def info():
    root_info = tk.Toplevel(root)
    root_info.title('info')
    root_info.focus_set()
    inf = tk.Label(root_info, bg='white', fg='black', width=40, height=10)
    inf.pack()
    inf['text'] = 'You plaing vs AI, yor target is do \n not give AI pregict batton you will push\n' \
                  '\n You will win if yor resalt whill be better\n then random when you reach 100' \
                  ' step\n  \n r - reset counter,' \
                  'do not reset AI                  \n  e, h - chose the mode of game, and reset AI \n'
    root_info.mainloop()


def make_model(difficulty):
    model = Sequential()

    model.add(Dense(9, activation='linear', input_shape=[9]))
    if difficulty == 1:
        model.add(Dense(9, activation='relu'))
        model.add(Dense(9))


    optimizer = Adam(lr=0.005)
    model.compile(optimizer=optimizer, loss='mse')
    return model


def data_step(inp):
    data_line = []
    if type(inp) == int:
        for i in range(9):
            if inp - 1 == i:
                data_line.append(1)
            else:
                data_line.append(0)
    elif type(inp) == list:
        for i in range(9):
            if (inp[0] - 1) or (inp[1] - 1) == i:
                data_line.append(1)
            else:
                data_line.append(0)
    return data_line


def update_color(pushes, cmap, cmap_status):
    if cmap_status == True:
        cmap = np.array(cmap)
        m = max(pushes)
        icalor = np.array(list(map(lambda x: int((x / m) * 255), pushes)))
        calors = []

        def calor_hex(x):
            if len(hex(x)) == 3:
                calor = f'0x0{hex(x)[2]}'
            else:
                calor = hex(x)
            return calor

        for i in range(9):
            calor = list(map(int, icalor[i] * cmap / 255))
            calors.append(list(map(calor_hex, calor)))
            calor_names = []
        for i in range(9):
            calor_names.append(f'#{calors[i][0][2:4]}{calors[i][1][2:4]}{calors[i][2][2:4]}')

        b1['bg'] = calor_names[0]
        b2['bg'] = calor_names[1]
        b3['bg'] = calor_names[2]
        b4['bg'] = calor_names[3]
        b5['bg'] = calor_names[4]
        b6['bg'] = calor_names[5]
        b7['bg'] = calor_names[6]
        b8['bg'] = calor_names[7]
        b9['bg'] = calor_names[8]
    else:
        b1['bg'] = 'gray'
        b2['bg'] = 'gray'
        b3['bg'] = 'gray'
        b4['bg'] = 'gray'
        b5['bg'] = 'gray'
        b6['bg'] = 'gray'
        b7['bg'] = 'gray'
        b8['bg'] = 'gray'
        b9['bg'] = 'gray'


def show(number):

    if type(number) == int:
        number = number + 1
        if number == 1:
            b1['bg'] = 'red'
        if number == 2:
            b2['bg'] = 'red'
        if number == 3:
            b3['bg'] = 'red'
        if number == 4:
            b4['bg'] = 'red'
        if number == 5:
            b5['bg'] = 'red'
        if number == 6:
            b6['bg'] = 'red'
        if number == 7:
            b7['bg'] = 'red'
        if number == 8:
            b8['bg'] = 'red'
        if number == 9:
            b9['bg'] = 'red'
    else:
        number = np.array(number)
        number = number + 1
        for i in range(2):
            if number[i] == 1:
                b1['bg'] = 'red'
            if number[i] == 2:
                b2['bg'] = 'red'
            if number[i] == 3:
                b3['bg'] = 'red'
            if number[i] == 4:
                b4['bg'] = 'red'
            if number[i] == 5:
                b5['bg'] = 'red'
            if number[i] == 6:
                b6['bg'] = 'red'
            if number[i] == 7:
                b7['bg'] = 'red'
            if number[i] == 8:
                b8['bg'] = 'red'
            if number[i] == 9:
                b9['bg'] = 'red'


class main():
    def __init__(self, difficulty):
        x_data = np.array([data_step(1)])
        y_data = np.array([data_step(1)])
        x_data = np.vstack((x_data, data_step(1)))
        self.x_data = x_data
        self.y_data = y_data
        self.model = make_model(difficulty)
        self.iteration = 1
        self.status = 1
        self.score = [1]
        self.steps = 1
        self.pushes = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.cmap = [128, 128, 128]
        self.cmap_status = False
        update_color(self.pushes, self.cmap, self.cmap_status)

        if difficulty == 0:
            self.mode = 'easy'
        elif difficulty == 1:
            self.mode = 'hard'
            self.buffer = []

    def main(self, number):

        if self.status == 1:
            inp = number

            if self.mode == 'easy':
                self.pushes[inp - 1] = self.pushes[inp - 1] + 1
            elif self.mode == 'hard':
                self.pushes[inp[0] - 1] = self.pushes[inp[0] - 1] + 1
                self.pushes[inp[1] - 1] = self.pushes[inp[1] - 1] + 1

            inp_step = data_step(inp)
            output = self.model(Variable([self.y_data[len(self.y_data) - 1]]))
            if self.mode == 'easy':
                max = int(output.numpy().argmax())
            elif self.mode == 'hard':
                output = output.numpy()[0]
                max = [output.argmax()]
                output[max] = 0
                max.append(output.argmax())

            self.y_data = np.vstack((self.y_data, inp_step))

            self.model.fit(self.x_data, self.y_data, epochs=10)
            self.x_data = np.vstack((self.x_data, inp_step))
            l['text'] = f'step = {self.iteration} (Total step = {self.steps})'

            update_color(self.pushes, self.cmap, self.cmap_status)
            show(max)

            self.iteration = self.iteration + 1
            self.steps = self.steps + 1

            av_score = sum(self.score) / len(self.score)
            caunter['text'] = av_score

            if self.mode == 'easy':
                if inp - 1 == max:
                    self.score.append(self.iteration)
                    self.iteration = 1
                    av_score = sum(self.score) / len(self.score)
                    l['text'] = f'FAIL, score = {"%.2f" % av_score} (iteration = {self.iteration})'

            if main.steps == 100:
                self.status = 0
                score = (sum(self.score) + self.iteration) / len(self.score)
                if score > 9:
                    l['text'] = f'YOU WIN, score = {"%.2f" % score} ({self.mode}) (r - restart)'
                else:
                    l['text'] = f'YOU LOSE, score = {"%.2f" % score} ({self.mode}) (r - restart)'

main = main(difficulty)
l['text'] = 'i - rules, c - color gradient, s - settings, \n r - restart, h - hard mode, e - easy mode '


def keypress(key):
    try:
        key = int(key.char)
        if main.mode == 'easy':
            main.main(key)
        elif main.mode == 'hard':
            if main.buffer == []:
                main.buffer.append(key)
            else:
                main.buffer.append(key)
                main.main(main.buffer)
                main.buffer = []
    except ValueError:
        if key.char == 'h':
            main.__init__(1)
            l['text'] = 'Hard mode on, game restarted'
        elif key.char == 'e':
            main.__init__(0)
            l['text'] = 'Easy mode on, game restarted'
        elif key.char == 'c':
            if main.cmap_status == True:
                main.cmap_status = False
                l['text'] = 'Color map disabled'
                update_color(main.pushes, main.cmap, main.cmap_status)
            else:
                main.cmap_status = True
                l['text'] = 'Color map ON'
                update_color(main.pushes, main.cmap, main.cmap_status)
        elif key.char == 'r':
            main.status = 1
            main.iteration = 1
            main.score = []
            main.steps = 1
        elif key.char == 'i':
            info()
        else:
            l['text'] = 'Use numpad for play (i - info)'


def c1(a):
    a = 1
    if main.mode == 'easy':
        main.main(a)
    elif main.mode == 'hard':
        if main.buffer == []:
            main.buffer.append(a)
        else:
            main.buffer.append(a)
            main.main(main.buffer)
            main.buffer = []

def c2(a):
    a = 2
    if main.mode == 'easy':
        main.main(a)
    elif main.mode == 'hard':
        if main.buffer == []:
            main.buffer.append(a)
        else:
            main.buffer.append(a)
            main.main(main.buffer)
            main.buffer = []
def c3(a):
    a = 3
    if main.mode == 'easy':
        main.main(a)
    elif main.mode == 'hard':
        if main.buffer == []:
            main.buffer.append(a)
        else:
            main.buffer.append(a)
            main.main(main.buffer)
            main.buffer = []
def c4(a):
    a = 4
    if main.mode == 'easy':
        main.main(a)
    elif main.mode == 'hard':
        if main.buffer == []:
            main.buffer.append(a)
        else:
            main.buffer.append(a)
            main.main(main.buffer)
            main.buffer = []
def c5(a):
    a = 5
    if main.mode == 'easy':
        main.main(a)
    elif main.mode == 'hard':
        if main.buffer == []:
            main.buffer.append(a)
        else:
            main.buffer.append(a)
            main.main(main.buffer)
            main.buffer = []
def c6(a):
    a = 6
    if main.mode == 'easy':
        main.main(a)
    elif main.mode == 'hard':
        if main.buffer == []:
            main.buffer.append(a)
        else:
            main.buffer.append(a)
            main.main(main.buffer)
            main.buffer = []
def c7(a):
    a = 7
    if main.mode == 'easy':
        main.main(a)
    elif main.mode == 'hard':
        if main.buffer == []:
            main.buffer.append(a)
        else:
            main.buffer.append(a)
            main.main(main.buffer)
            main.buffer = []
def c8(a):
    a = 8
    if main.mode == 'easy':
        main.main(a)
    elif main.mode == 'hard':
        if main.buffer == []:
            main.buffer.append(a)
        else:
            main.buffer.append(a)
            main.main(main.buffer)
            main.buffer = []
def c9(a):
    a = 9
    if main.mode == 'easy':
        main.main(a)
    elif main.mode == 'hard':
        if main.buffer == []:
            main.buffer.append(a)
        else:
            main.buffer.append(a)
            main.main(main.buffer)
            main.buffer = []

frame.bind("<KeyPress>", keypress)

b1.bind('<Button-1>', c1)
b2.bind('<Button-1>', c2)
b3.bind('<Button-1>', c3)
b4.bind('<Button-1>', c4)
b5.bind('<Button-1>', c5)
b6.bind('<Button-1>', c6)
b7.bind('<Button-1>', c7)
b8.bind('<Button-1>', c8)
b9.bind('<Button-1>', c9)

frame.grid()
frame.focus_set()

root.mainloop()
