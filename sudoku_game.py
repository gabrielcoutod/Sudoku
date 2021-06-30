import pygame
import sudoku_grid as sg
from enum import Enum


class SudokuGame:
    """
    Implementation of sudoku with pygame
    """
    SCREEN_COLOR = (240, 240, 240)  # color of the screen
    TEXT_COLOR = (0, 0, 0)  # color of text
    PLAY_BACKGROUND = (220, 220, 220)  # background color of the play button
    WIN_BACKGROUND = (220, 220, 220)  # background color of the win message
    LINE_COLOR = (128, 0, 128)  # color of the line when a cell is selected
    ERROR_TEXT_COLOR = (255, 0, 0)  # color of the grid numbers when there's conflict
    GRID_POS = (151, 51)  # position of the grid
    RES = (800, 600)  # resolution of the screen
    PLAY_CENTER = (400, 400)  # center of the play button
    LINE_DESLOC = (15, 10)  # to adjust line position in relation to the square
    WIN_SIZE = 50  # win message size
    PLAY_SIZE = 32  # play button size
    TITLE_SIZE = 50  # size of the game title
    NUMBERS_SIZE = 32  # size of the numbers on the grid
    ERROR = -1  # indicates the pressed button wasn't a number
    NO_CLICK = -1  # indicates that no click was made
    SQUARE_SIZE = 51  # size of the region that can be clicked

    # position of the cells
    CELLS_POS = [(47 * i + i // 3 + 151 + 20 + 4 * i, 47 * j + j // 3 + 51 + 20 + 4 * j)
                 for j in range(9) for i in range(9)]

    class State(Enum):
        """
        Possible states of the game
        """
        menu = 1
        game = 2
        win = 3

    def __init__(self):
        """
        Initializes the game
        """
        # initializes pygame
        pygame.init()
        # initializes the screen
        self.screen = pygame.display.set_mode(SudokuGame.RES)
        self.grid_img = pygame.image.load("grid.png")
        pygame.display.set_caption("Sudoku")
        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)
        # initializes the grid
        self.sg = sg.SudokuGrid()
        self.grid = []
        # initializes game variables
        self.current_click = SudokuGame.NO_CLICK
        self.state = SudokuGame.State.menu
        self.running = True

    def event(self):
        """
        updates the game based on the pressed keys
        """
        mouse = pygame.mouse.get_pos()  # gets tuple with pos

        for event in pygame.event.get():

            if event.type == pygame.QUIT \
                    or (self.state == SudokuGame.State.menu
                        and event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                """
                if closed the game
                """
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP and self.state == SudokuGame.State.game:
                """
                if clicked during the game checks if clicked on a cell
                """
                self.clicked(mouse)

            elif self.state == SudokuGame.State.game and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                """
                if during the game pressed ESC goes back to the menu
                """
                self.state = SudokuGame.State.menu
                self.current_click = SudokuGame.NO_CLICK
            elif event.type == pygame.KEYDOWN and self.current_click != SudokuGame.NO_CLICK \
                    and self.state == SudokuGame.State.game:
                """
                if during the game pressed a key after having clicked on a cell checks if pressed a number 
                to put on the cell
                """
                number = self.number_pressed(event)
                if number != SudokuGame.ERROR and self.sg.grid[self.current_click] == sg.SudokuGrid.INVALID_VALUE:
                    self.grid[self.current_click] = number
                elif self.sg.grid[self.current_click] == sg.SudokuGrid.INVALID_VALUE:
                    self.grid[self.current_click] = sg.SudokuGrid.INVALID_VALUE
                self.current_click = SudokuGame.NO_CLICK
            elif self.state == SudokuGame.State.menu and event.type == pygame.MOUSEBUTTONUP:
                """
                if in the menu pressed the mouse button checks if pressed on the play button
                """
                if self.mouse_over_button(mouse, (360, 385), 80, 30):
                    self.state = SudokuGame.State.game
                    self.grid_reset()
                    self.current_click = SudokuGame.NO_CLICK
            elif self.state == SudokuGame.State.menu \
                    and event.type == pygame.KEYDOWN \
                    and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                """
                if in the menu pressed Enter starts the game
                """
                self.state = SudokuGame.State.game
                self.grid_reset()
                self.current_click = SudokuGame.NO_CLICK
            elif self.state == SudokuGame.State.win \
                    and (event.type == pygame.MOUSEBUTTONUP
                         or (event.type == pygame.KEYDOWN
                             and (event.key == pygame.K_ESCAPE
                                  or event.key == pygame.K_KP_ENTER
                                  or event.key == pygame.K_RETURN))):
                """
                if won the game and clicked on the screen or pressed ESC or Enter goes back to the menu
                """
                self.state = SudokuGame.State.menu
                self.current_click = SudokuGame.NO_CLICK

    def selected(self):
        """
         If a cell is selected draws a line on it
        """
        if self.current_click != SudokuGame.NO_CLICK \
                and self.sg.grid[self.current_click] == sg.SudokuGrid.INVALID_VALUE:
            pygame.draw.line(self.screen, SudokuGame.LINE_COLOR, (
                SudokuGame.CELLS_POS[self.current_click][0] + SudokuGame.LINE_DESLOC[0],
                SudokuGame.CELLS_POS[self.current_click][1] + SudokuGame.SQUARE_SIZE - SudokuGame.LINE_DESLOC[1]), (
                                 SudokuGame.CELLS_POS[self.current_click][0] + SudokuGame.SQUARE_SIZE -
                                 SudokuGame.LINE_DESLOC[0],
                                 SudokuGame.CELLS_POS[self.current_click][1] + SudokuGame.SQUARE_SIZE -
                                 SudokuGame.LINE_DESLOC[1]))

    def numbers(self):
        """
        Draws the numbers on the grid. If there is a collision draws the number with ERROR_TEXT_COLOR
        """
        font = pygame.font.Font('freesansbold.ttf', SudokuGame.NUMBERS_SIZE)
        collisions = [self.get_collisions(i) for i in range(sg.SudokuGrid.GRID_SIZE)]

        for i in range(sg.SudokuGrid.GRID_SIZE):
            if self.grid[i] != sg.SudokuGrid.INVALID_VALUE and not collisions[i]:
                text = font.render(f"{self.grid[i]}", True, SudokuGame.TEXT_COLOR, SudokuGame.SCREEN_COLOR)
                rect = text.get_rect()
                rect.center = (SudokuGame.CELLS_POS[i][0] + SudokuGame.SQUARE_SIZE / 2,
                               SudokuGame.CELLS_POS[i][1] + SudokuGame.SQUARE_SIZE / 2)
                self.screen.blit(text, rect)
            elif self.grid[i] != sg.SudokuGrid.INVALID_VALUE and collisions[i]:
                text = font.render(f"{self.grid[i]}", True, SudokuGame.ERROR_TEXT_COLOR, SudokuGame.SCREEN_COLOR)
                rect = text.get_rect()
                rect.center = (SudokuGame.CELLS_POS[i][0] + SudokuGame.SQUARE_SIZE / 2,
                               SudokuGame.CELLS_POS[i][1] + SudokuGame.SQUARE_SIZE / 2)
                self.screen.blit(text, rect)

    def clicked(self, mouse: tuple):
        """
        Checks if the mouse is on some cell
        """
        self.current_click = SudokuGame.NO_CLICK
        i = 0  # to iterate through cells
        while i < sg.SudokuGrid.GRID_SIZE:
            # if mouse is over a cell
            if self.mouse_over_button(mouse, SudokuGame.CELLS_POS[i], SudokuGame.SQUARE_SIZE, SudokuGame.SQUARE_SIZE):
                self.current_click = i
            i += 1

    def grid_reset(self):
        """
        Resets the grid to play again
        """
        self.sg.reset()
        self.sg.create()
        self.sg.remove_cells()
        self.grid = self.sg.grid[:]

    def start(self):
        """
        Starts the game
        """
        while self.running:  # runs game
            self.screen.fill(SudokuGame.SCREEN_COLOR)  # fills background

            if self.grid == self.sg.sol and self.state == SudokuGame.State.game:  # checks if won the game
                self.state = SudokuGame.State.win

            self.event()  # checks the events
            self.draw_state()  # draws according to the state
            pygame.display.update()  # updates the display

    def draw_state(self):
        """
        Draws on the screen according o the current state
        """
        if self.state == SudokuGame.State.menu:
            self.menu()
            self.play_button()
        elif self.state == SudokuGame.State.game:
            self.numbers()
            self.draw_grid()
            self.selected()
        elif self.state == SudokuGame.State.win:
            self.numbers()
            self.draw_grid()
            self.win()

    def get_collisions(self, pos: int) -> list:
        """
        Returns a list with the indexes of the elements that collide with the element in pos
        """
        cols = []

        value = self.grid[pos]  # backup of the previous value
        self.grid[pos] = sg.SudokuGrid.INVALID_VALUE  # so it doesn't interfere with the test

        sub_grid = sg.SudokuGrid.sub_grids[pos]  # gets a list with the elements of the sub_grid
        line = pos // sg.SudokuGrid.MAX_NUMBER * sg.SudokuGrid.MAX_NUMBER  # index of the first element of the line
        col = pos % sg.SudokuGrid.MAX_NUMBER  # index of the first element of the column

        for i in range(sg.SudokuGrid.MAX_NUMBER):
            if self.grid[line + i] == value:
                cols.append(line + i)  # checks line
            if self.grid[col + sg.SudokuGrid.MAX_NUMBER * i] == value:  # checks column
                cols.append(col + sg.SudokuGrid.MAX_NUMBER * i)
            if self.grid[sub_grid[i]] == value:  # checks subgrid
                cols.append(sub_grid[i])

        self.grid[pos] = value
        return cols

    def number_pressed(self, event: pygame.event.Event) -> int:
        """
        Checks the number pressed. Returns SudokuGame.ERROR if a number wasn't pressed
        """
        if event.key == pygame.K_1 or event.key == pygame.K_KP1:
            return 1
        if event.key == pygame.K_2 or event.key == pygame.K_KP2:
            return 2
        if event.key == pygame.K_3 or event.key == pygame.K_KP3:
            return 3
        if event.key == pygame.K_4 or event.key == pygame.K_KP4:
            return 4
        if event.key == pygame.K_5 or event.key == pygame.K_KP5:
            return 5
        if event.key == pygame.K_6 or event.key == pygame.K_KP6:
            return 6
        if event.key == pygame.K_7 or event.key == pygame.K_KP7:
            return 7
        if event.key == pygame.K_8 or event.key == pygame.K_KP8:
            return 8
        if event.key == pygame.K_9 or event.key == pygame.K_KP9:
            return 9

        return SudokuGame.ERROR

    def mouse_over_button(self, mouse_pos: tuple, button_pos: tuple, width: int, height: int) -> bool:
        """
        Checks if the mouse is over the button
        """
        if button_pos[0] <= mouse_pos[0] < button_pos[0] + width \
                and button_pos[1] <= mouse_pos[1] < button_pos[1] + height:
            return True

        return False

    def draw_grid(self):
        """
        Draws the game grid
        """
        self.screen.blit(self.grid_img, SudokuGame.GRID_POS)

    def play_button(self):
        """
        Draws the play button on the screen
        """
        self.button(SudokuGame.PLAY_SIZE, "PLAY", SudokuGame.TEXT_COLOR, SudokuGame.PLAY_BACKGROUND,
                    SudokuGame.PLAY_CENTER)

    def menu(self):
        """
        Draws the game title on the screen
        """
        self.button(SudokuGame.TITLE_SIZE, "SUDOKU", SudokuGame.TEXT_COLOR, SudokuGame.SCREEN_COLOR,
                    (SudokuGame.RES[0] / 2, SudokuGame.RES[1] / 2))

    def win(self):
        """
        Draws the win message on the screen
        """
        self.button(SudokuGame.WIN_SIZE, "YOU WIN", SudokuGame.TEXT_COLOR, SudokuGame.WIN_BACKGROUND,
                    (SudokuGame.RES[0] / 2, SudokuGame.RES[1] / 2))

    def button(self, font_size: int, text: str, text_color: tuple, back_color: tuple, center: tuple):
        """
        Draws a button on the screen with back_color being the background color, center being the center of the
        rectangle, text being the text that will be written on the button, text_color the color of the text and
        font_size the size of the text
        """
        font = pygame.font.Font('freesansbold.ttf', font_size)
        rect_text = font.render(text, True, text_color, back_color)
        rect = rect_text.get_rect()
        rect.center = center
        self.screen.blit(rect_text, rect)


if __name__ == '__main__':
    SudokuGame().start()  # starts the game
