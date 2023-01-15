import tkinter as tk
import customtkinter as ctk
import random
import time

PATH = __file__[:-7]


class Frame:
    def __init__(self):
        self.frame = tk.Tk()
        self.frame.geometry('840x525')
        self.frame.title('Battleships')
        self.frame.resizable(False, False)

        self.images = {
            'empty': tk.PhotoImage(file=f'{PATH}graphics\\cell_empty.png'),
            'ship': tk.PhotoImage(file=f'{PATH}graphics\\cell_ship.png'),
            'sunk': tk.PhotoImage(file=f'{PATH}graphics\\cell_sunk.png'),
            '2_ship_horizontal': tk.PhotoImage(file=f'{PATH}graphics\\2_ship_horizontal.png')
        }

        # text below the grids
        tk.Label(self.frame, text='Your Grid', font='Arial 20').place(x=212, y=500, anchor='center')
        tk.Label(self.frame, text='Opponent Grid', font='Arial 20').place(x=628, y=500, anchor='center')

        # text at the top in the middle. Tells the user the status of the game
        self.status_text_var = tk.StringVar()
        self.status_text_var.set('Hola')
        tk.Label(self.frame, textvariable=self.status_text_var, font='Arial 20').place(x=420, y=25, anchor='center')

        self.status_text2_var = tk.StringVar()
        self.status_text2_var.set('bingo')
        tk.Label(self.frame, textvariable=self.status_text2_var, font='Arial 12').place(x=420, y=55, anchor='center')

    def mainloop(self):
        self.frame.mainloop()


class Game:
    def __init__(self):
        self.cellImages = ['empty', 'ship', 'sunk']
        ''' states:
        'player_setup': The player is placing their ships.
        'game_running': The game is running. It is always the players move, as the computer makes its move instantly'''
        self.state = 'player_setup'
        self.update_status_text()
        self.temporary_ship = None  # used for hovering while placing ships

    def update_status_text(self):
        if self.state == 'player_setup':
            frame.status_text_var.set('Place your ships!')
            frame.status_text2_var.set('Use the up- and down-arrows to cycle through ship sizes, and use the the '
                                       'left- and right arrows to change ship direction.')

    def mouse_motion(self, x, y):
        #print('första')
        #grid1.print_grid()
        mouse_grid_pos = get_linear_coords([x/40, y/40])
        if self.state == 'player_setup':
            '''
            if grid_pos != self.temporary_ship_anchor:
                if grid1.add_ship(True, 2, grid_pos, limit=false):
                    grid1.delete_ship(self.temporary_ship_anchor)
                    grid1.update_grid()
                    self.temporary_ship_anchor = grid_pos
            '''
            if grid1.check_clear_space_for_ship(True, 3, mouse_grid_pos):
                self.temporary_ship = Ship(True, 3, mouse_grid_pos)
            grid1.update_grid()


class Grid:
    def __init__(self, view, pos_offset=(0, 0), selection=False):
        # 100 values, a 10x10 grid.
        # Cell state 0 means no empty, state 1 means part of ship, state 2 means sunken part of ship
        self.grid = [0 for n in range(100)]
        self.ships = []

        self.view = view  # True means you see everything, False means opponent view
        self.selection = selection
        self.pos_offset = pos_offset
        self.canvas = tk.Canvas(frame.frame, width=401, height=401)
        self.canvas.place(x=pos_offset[0], y=pos_offset[1])
        self.canvas_grid = []

        for i in range(100):
            x, y = get_2d_coords(i)
            self.canvas_grid.append(self.canvas.create_image(40*x+2, 40*y+2, image=frame.images['empty'], anchor='nw'))
        self.update_grid()

        self.canvas.bind('<Motion>', self.mouse_motion)

    def mouse_motion(self, event):
        game.mouse_motion(event.x, event.y)

    def generate_ships(self, amount, max_len):
        for i in range(amount):
            done = False
            while not done:
                direction = bool(random.randint(0, 1))
                length = 3
                pos = random.randint(0, 99)
                done = self.add_ship(direction, length, pos)
            self.update_grid()

    def check_clear_space_for_ship(self, direction, length, pos):
        #print('andra')
        #self.print_grid()
        success = False
        x, y = get_2d_coords(pos)
        if direction:  # horizontal
            if x + length < 11 and all([self.grid[pos + j] == 0 for j in range(length)]):
                success = True
        else:  # vertical
            if y + length < 9 and all([self.grid[pos + 10 * j] == 0 for j in range(length)]):
                success = True
        print(success, x + length < 11, x, length)
        return success

    def add_ship(self, direction, length, pos):
        success = self.check_clear_space_for_ship(direction, length, pos)
        if success:
            self.ships.append(Ship(direction, length, pos))
        return success

    def delete_ship(self, pos):
        ship_id = None
        for i, ship in enumerate(self.ships):
            if ship.anchor == pos:
                ship_id = i
                break
        if ship_id is not None:
            self.ships.pop(ship_id)
        return ship_id is not None

    def update_grid(self):
        ''' Updates the grid data based on the ships and updates the tk_grid. '''

        # clear the grid
        for i in range(len(self.grid)):
            self.grid[i] = 0

        grid_data = [2, 1]
        for ship in self.ships:
            for i, cell in enumerate(ship.cells):
                if ship.direction:  # direction is horizontal
                    self.grid[ship.anchor+i] = grid_data[cell]
                else:  # direction is vertical
                    self.grid[ship.anchor+10*i] = grid_data[cell]
        '''
        if game.temporary_ship is not None:  # if there is a temporary ship
            for i in range(len(game.temporary_ship.cells)):
                if game.temporary_ship.direction:  # direction is horizontal
                    self.grid[game.temporary_ship.anchor+i] = 1
                else:  # direction is vertical
                    self.grid[game.temporary_ship.anchor+10*i] = 1
        '''

        # update the tk_grid
        if self.view:
            for i, cell in enumerate(self.grid):
                self.canvas.itemconfig(self.canvas_grid[i], image=frame.images[game.cellImages[cell]])
        if game.temporary_ship is not None:

            for i in range(len(game.temporary_ship.cells)):
                if game.temporary_ship.direction:  # direction is horizontal
                    self.canvas.itemconfig(self.canvas_grid[game.temporary_ship.anchor+i], image=frame.images[game.cellImages[1]])
                else:  # direction is vertical
                    self.canvas.itemconfig(self.canvas_grid[game.temporary_ship.anchor+10*i], image=frame.images[game.cellImages[1]])
        else:
            pass

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


def get_2d_coords(pos):
    ''' Returns x,y coords from linear coords input. '''
    y = 0
    while pos > 9:
        pos -= 10
        y += 1
    x = pos
    return x, y


def get_linear_coords(pos):
    ''' Returns linear coords from given 2d coords '''
    return 10 * int(pos[1]) + int(pos[0])


frame = Frame()
game = Game()

grid1 = Grid(True, (10, 75))
grid2 = Grid(True, (424, 75))
grid2.generate_ships(5, 4)
grid1.update_grid()

frame.mainloop()