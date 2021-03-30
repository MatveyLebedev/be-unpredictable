from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from tensorflow import Variable
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
import numpy as np
from kivy.config import Config

Config.set('graphics', 'width', '400')

difficulty = 0  # {0 - easy, 1 - hard}

def make_model(difficulty):
    model = Sequential()

    model.add(Dense(9, activation='relu', input_shape=[9]))
    if difficulty == 1:
        model.add(Dense(9, activation='relu'))

    model.add(Dense(9, activation='linear'))
    optimizer = Adam(lr=0.008)
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

def update_color(pushes, cmap_status):
    if cmap_status == True:
        m = max(pushes)
        brize = 0.5
        icalor = np.array(list(map(lambda x: float(x / m) * brize, pushes)))

        app.b1.background_color = [1, 1, 1, icalor[0]]
        app.b2.background_color = [1, 1, 1, icalor[1]]
        app.b3.background_color = [1, 1, 1, icalor[2]]
        app.b4.background_color = [1, 1, 1, icalor[3]]
        app.b5.background_color = [1, 1, 1, icalor[4]]
        app.b6.background_color = [1, 1, 1, icalor[5]]
        app.b7.background_color = [1, 1, 1, icalor[6]]
        app.b8.background_color = [1, 1, 1, icalor[7]]
        app.b9.background_color = [1, 1, 1, icalor[8]]
    else:
        app.b1.background_color = [1, 1, 1, 0.5]
        app.b2.background_color = [1, 1, 1, 0.5]
        app.b3.background_color = [1, 1, 1, 0.5]
        app.b4.background_color = [1, 1, 1, 0.5]
        app.b5.background_color = [1, 1, 1, 0.5]
        app.b6.background_color = [1, 1, 1, 0.5]
        app.b7.background_color = [1, 1, 1, 0.5]
        app.b8.background_color = [1, 1, 1, 0.5]
        app.b9.background_color = [1, 1, 1, 0.5]

def show(number):

    if type(number) == int:
        number = number + 1
        if number == 1:
            app.b1.background_color = [1, 0, 0, 1]
        if number == 2:
            app.b2.background_color = [1, 0, 0, 1]
        if number == 3:
            app.b3.background_color = [1, 0, 0, 1]
        if number == 4:
            app.b4.background_color = [1, 0, 0, 1]
        if number == 5:
            app.b5.background_color = [1, 0, 0, 1]
        if number == 6:
            app.b6.background_color = [1, 0, 0, 1]
        if number == 7:
            app.b7.background_color = [1, 0, 0, 1]
        if number == 8:
            app.b8.background_color = [1, 0, 0, 1]
        if number == 9:
            app.b9.background_color = [1, 0, 0, 1]
    else:
        number = np.array(number)
        number = number + 1
        for i in range(2):
            if number == 1:
                app.b1.background_color = [1, 0, 0, 1]
            if number == 2:
                app.b2.background_color = [1, 0, 0, 1]
            if number == 3:
                app.b3.background_color = [1, 0, 0, 1]
            if number == 4:
                app.b4.background_color = [1, 0, 0, 1]
            if number == 5:
                app.b5.background_color = [1, 0, 0, 1]
            if number == 6:
                app.b6.background_color = [1, 0, 0, 1]
            if number == 7:
                app.b7.background_color = [1, 0, 0, 1]
            if number == 8:
                app.b8.background_color = [1, 0, 0, 1]
            if number == 9:
                app.b9.background_color = [1, 0, 0, 1]


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
        self.cmap_status = True

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
            app.print_text(f'step = {self.iteration} (Total step = {self.steps})')

            update_color(self.pushes, self.cmap_status)
            show(max)

            self.iteration = self.iteration + 1
            self.steps = self.steps + 1

            self.score[-1] = self.iteration
            av_score = f'{"%.2f" % (sum(self.score) / len(self.score))}'
            app.print_score(av_score)

            if self.mode == 'easy':
                if inp - 1 == max:
                    self.iteration = 1
                    av_score = (sum(self.score) / len(self.score))
                    app.print_text(f'FAIL, score = {"%.2f" % av_score} (step = {self.iteration})')
                    self.score.append(self.iteration)

            if main.steps == 100:
                self.status = 0
                score = (sum(self.score) + self.iteration) / len(self.score)
                if score > 9:
                    app.print_text(f'YOU WIN, score = {"%.2f" % score} ({self.mode}) (r - restart)')
                else:
                    app.print_text(f'YOU LOSE, score = {"%.2f" % score} ({self.mode}) (r - restart)')

class app(App):

    def print_text(self, string):
        self.lbl2.text = string

    def print_score(self, score):
        self.lbl1.text = score

    def keypress(self, key):
        try:
            key = int(key.text)
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
                app.lbl2.text = 'Hard mode on, game restarted'
            elif key.char == 'e':
                main.__init__(0)
                app.lbl2.text = 'Easy mode on, game restarted'
            elif key.char == 'c':
                if main.cmap_status == True:
                    main.cmap_status = False
                    app.lbl2.text = 'Color map disabled'
                    update_color(main.pushes, main.cmap_status)
                else:
                    main.cmap_status = True
                    app.lbl2.text = 'Color map ON'
                    update_color(main.pushes, main.cmap_status)
            elif key.char == 'r':
                main.status = 1
                main.iteration = 1
                main.score = []
                main.steps = 1
            else:
                app.lbl2.text = 'Use numpad for play (i - info)'


    def build(self):

        l1 = BoxLayout(orientation='vertical')

        self.lbl1 = Label(text='0', font_size=30)
        self.lbl2 = Label(text='1')

        l1.add_widget(self.lbl1)
        l1.add_widget(self.lbl2)

        mb = GridLayout(cols=3, padding=25, size_hint=(1, 3))

        self.b7 = Button(text='7', background_normal='', background_color=[1, 1, 1, 0.5], on_press=self.keypress)
        self.b8 = Button(text='8', background_normal='', background_color=[1, 1, 1, 0.5], on_press=self.keypress)
        self.b9 = Button(text='9', background_normal='', background_color=[1, 1, 1, 0.5], on_press=self.keypress)

        self.b4 = Button(text='4', background_normal='', background_color=[1, 1, 1, 0.5], on_press=self.keypress)
        self.b5 = Button(text='5', background_normal='', background_color=[1, 1, 1, 0.5], on_press=self.keypress)
        self.b6 = Button(text='6', background_normal='', background_color=[1, 1, 1, 0.5], on_press=self.keypress)

        self.b1 = Button(text='1', background_normal='', background_color=[1, 1, 1, 0.5], on_press=self.keypress)
        self.b2 = Button(text='2', background_normal='', background_color=[1, 1, 1, 0.5], on_press=self.keypress)
        self.b3 = Button(text='3', background_normal='', background_color=[1, 1, 1, 0.5], on_press=self.keypress)

        mb.add_widget(self.b7)
        mb.add_widget(self.b8)
        mb.add_widget(self.b9)

        mb.add_widget(self.b4)
        mb.add_widget(self.b5)
        mb.add_widget(self.b6)

        mb.add_widget(self.b1)
        mb.add_widget(self.b2)
        mb.add_widget(self.b3)

        l1.add_widget(mb)

        return l1

if __name__ == '__main__':
    app = app()
    main = main(difficulty)
    app.run()