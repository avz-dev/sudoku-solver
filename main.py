import PySimpleGUI as sg
import numpy as np

grid_size = 9
layout = [[] for x in range(14)]
boxes = []
board = np.array([[0 for i in range(9)] for j in range(9)])


# Checks whether a given number can be placed in a certain index
# by testing for an equivalence in the same row, col, and box.
# If no issues arise, the number is assigned to the index.
# Input: 2d list of board values, number to be inserted, insertion row & column
# Output: boolean determining whether the number placement is valid
def valid_placement(grid, num, row, col):
    if num in grid[row, :] or num in grid[:, col]:
        return False
    block_row = (row // 3) * 3
    block_col = (col // 3) * 3
    if num in grid[block_row:block_row + 3, block_col: block_col + 3]:
        return False
    grid[row][col] = num
    return True


# Determines whether the starting board is valid
# Input: 2d list of sudoku board values
# Output: boolean indicating whether board is valid
def check_board(grid):
    for i in range(0, grid_size):
        for j in range(0, grid_size):
            if grid[i][j] != 0:
                num = grid[i][j]
                grid[i][j] = 0
                if not valid_placement(grid, num, i, j):
                    return False
    return True


# Runs through the board seeking values of zero and attempts to
# solve by checking the validity of values 1-9. If a value
# fits, the function calls itself, otherwise, the index values are
# reset and the next value is attempted. Rinse, repeat.
# Input: 2d list of sudoku board values
# Output: boolean indicating whether board is solvable
def solve_board(grid):
    if grid is None:
        return False
    if not check_board(grid):
        instructions.update('No solution, try again')
        return False
    for r in range(0, grid_size):
        for c in range(0, grid_size):
            if grid[r][c] == 0:
                for n in range(1, grid_size + 1):
                    if valid_placement(grid, n, r, c):
                        if solve_board(grid):
                            return True
                        grid[r][c] = 0
                return False
    return True


# updates input text elements in gui to display solution
# input: 2d list, solution to starting sudoku board
def display_board(grid):
    idx = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if not boxes[idx].get():
                boxes[idx].update(text_color='royal blue')
            boxes[idx].update(grid[i][j])
            idx += 1


# sets up the gui elements and returns a list of input elements
# input:  2d list of lists used to hold gui elements,
#         empty list to hold input text elements
# output: text element for displaying instructions
def initialize_GUI(grid_elements, bxs):
    grid_elements[0].append(sg.Text('', background_color='white'))
    for i in range(1, 12):
        if i not in (4, 8):
            grid_elements[i].append(sg.Push(background_color='white'))
            for j in range(3):
                for k in range(3):
                    box = sg.InputText(size=(2, 2), justification='center')
                    grid_elements[i].append(box)
                    bxs.append(box)
                if j != 2:
                    grid_elements[i].append(sg.VerticalSeparator(key='sep'))
            grid_elements[i].append(sg.Push(background_color='white'))
        else:
            grid_elements[i].append(sg.Text('', background_color='white'))
            for x in range(3):
                grid_elements[i].append(sg.HorizontalSeparator(key='sep'))
            grid_elements[i].append(sg.Text(' ', background_color='white'))
    text_box = sg.Text('Enter a starting sudoku board', size=(24, 2),
                       text_color='gray25', background_color='white',
                       justification='center')
    grid_elements.append([text_box])
    grid_elements.append([sg.Button('Clear', size=(18, 1), button_color='coral1'),
                          sg.Button('Solve', size=(18, 1), button_color='cornflower blue')])
    return text_box


# clears values, resets input text element colors, updates instruction text
# input: list of input text elements
def clear(vals):
    for element in vals:
        element.update('', background_color='gray96', text_color='black')
    instructions.update('Enter a starting sudoku board')


# colors user input text elements slightly darker
def color_board():
    for box in boxes:
        if sg.Input.get(box):
            box.update(background_color='gray88')


# reads input text values to fills a 2d list with, checks for valid input
def get_board():
    idx = 0
    color_board()
    is_valid = True
    for i in range(grid_size):
        for j in range(grid_size):
            if boxes[idx].get():
                if not boxes[idx].get().isdigit() \
                        or not int(boxes[idx].get()) in tuple(range(1, 10)):
                    instructions.update('Input must be numbers 1-9')
                    is_valid = False
                    boxes[idx].update(background_color='light salmon')
                else:
                    board[i][j] = int(boxes[idx].get())
            else:
                board[i][j] = 0
            idx += 1
    if is_valid:
        return board
    else:
        return None


instructions = initialize_GUI(layout, boxes)
sg.theme('Reddit')
window = sg.Window('Sudoku Solver', layout, size=(300, 335), element_justification='c')


while True:
    event, value = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Clear':
        clear(boxes)
    if event == 'Solve':
        if solve_board(get_board()):
            display_board(board)

window.close()
