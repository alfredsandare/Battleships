import tkinter as tk
import customtkinter as ctk
import random

PATH = __file__[:-7]


class Frame:
    def __init__(self):
        self.frame = tk.Tk()
        self.frame.geometry('955x600')
        self.frame.title('Battleships')
        self.frame.resizable(False, False)
        self.cellImages = ['empty', 'ship', 'sunk']

        self.images = {
            'empty': tk.PhotoImage(file=f'{PATH}graphics\\cell_empty.png'),
            'ship': tk.PhotoImage(file=f'{PATH}graphics\\cell_ship.png'),
            'sunk': tk.PhotoImage(file=f'{PATH}graphics\\cell_sunk.png')
        }

        tk.Label(self.frame, text='Your Grid', font='Arial 20').place(x=225, y=25, anchor='center')
        tk.Label(self.frame, text='Opponent Grid', font='Arial 20').place(x=725, y=25, anchor='center')

        status_text_var = tk.StringVar()
        status_text_var.set('Hola')
        status_text = tk.Label(self.frame, textvariable=status_text_var, font='Arial 20')
        status_text.place(x=477, y=520, anchor='center')

        status_text2_var = tk.StringVar()
        status_text2_var.set('bingo')
        status_text2 = tk.Label(self.frame, textvariable=status_text2_var, font='Arial 15')
        status_text2.place(x=477, y=550, anchor='center')


    def mainloop(self):
        self.frame.mainloop()

#### BING XILLING
class Grid:
    def __init__(self, view, pos_offset=(0, 0), selection=False):
        # 100 values, a 10x10 grid.
        # Cell state 0 means no empty, state 1 means part of ship, state 2 means sunken part of ship
        self.grid = [0 for n in range(100)]
        self.ships = []

        self.view = view  # True means you see everything, False means opponent view
        self.selection = selection
        self.pos_offset = pos_offset
        self.canvas = tk.Canvas(frame.frame, width=450, height=450)
        self.canvas.place(x=pos_offset[0], y=pos_offset[1])
        self.canvas_grid = []

        for i in range(100):
            x, y = self.get_2d_coords(i)
            self.canvas_grid.append(self.canvas.create_image(45*x, 45*y, image=frame.images['empty'], anchor='nw'))
        self.update_grid()

    def get_2d_coords(self, pos):
        ''' Returns x,y coords from linear coords input. '''
        y = 0
        while pos > 9:
            pos -= 10
            y += 1
        x = pos
        return x, y

    def generate_ships(self, amount, max_len):
        for i in range(amount):
            direction = bool(random.randint(0, 1))
            length = 3

            done = False
            pos = random.randint(0, 99)
            while not done:
                pos = random.randint(0, 99)
                x, y = self.get_2d_coords(pos)
                if direction:  # horizontal
                    if x + length < 9 and all([self.grid[pos+j] == 0 for j in range(length)]):
                        done = True
                else:  # vertical
                    if y + length < 9 and all([self.grid[pos+10*j] == 0 for j in range(length)]):
                        done = True
            self.ships.append(Ship(direction, length, pos))
            self.update_grid()

    def update_grid(self):
        ''' Updates the grid data based on the ships and updates the tk_grid. '''
        grid_data = [2, 1]
        for ship in self.ships:
            for i, cell in enumerate(ship.cells):
                if ship.direction:  # direction is horizontal
                    self.grid[ship.anchor+i] = grid_data[cell]
                else:  # direction is vertical
                    self.grid[ship.anchor+10*i] = grid_data[cell]

        # update the tk_grid
        if self.view:
            for i, cell in enumerate(self.grid):
                self.canvas.itemconfig(self.canvas_grid[i], image=frame.images[frame.cellImages[cell]])

    def print_grid(self):
        ''' Prints the grid to the console. '''
        for i in range(10):
            print(''.join(f'{self.grid[10*i+j]} ' for j in range(10))[:-1])


class Ship:
    def __init__(self, direction, length, anchor):
        # direction True is horizontal, direction False is vertical
        self.direction = direction
        self.cells = [True for i in range(length)]
        self.anchor = anchor

    def get_occupied_cells(self):
        if self.direction:
            return [self.anchor+i for i in range(len(self.cells))]
        return [self.anchor+10*i for i in range(len(self.cells))]


frame = Frame()

grid1 = Grid(True, (5, 50))
grid2 = Grid(False, (500, 50))
grid2.generate_ships(5, 4)
grid1.update_grid()

frame.mainloop()
