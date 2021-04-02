#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog
from Maze import *

CAN_WIDTH = 800
CAN_HEIGHT = 600
BG_COLOR = 'black'
GRID_COLOR = 'green'

WIN = Tk()

def draw_resolution(canvas, maze):
    width = maze.get_width()
    height = maze.get_height()
    l = maze.get_list_of_cells()
    
    var = 5
    
    DX = CAN_WIDTH // width
    DY = CAN_HEIGHT // height
    
    solv = maze.launch_solving()
    y = 0
    for line in solv:
        x = 0
        for boolean in line:
            if boolean:
                canvas.create_oval(x * DX + var, y * DY + var, (x + 1) * DX - var, (y + 1) * DY - var, fill = 'white')
            x += 1
        y += 1

def draw_grid(canvas, maze):
    canvas.create_rectangle(0, 0, CAN_WIDTH, CAN_HEIGHT, fill='black')
    width = maze.get_width()
    height = maze.get_height()
    l = maze.get_list_of_cells()

    label = WIN.children["!label"]
    button = label.children["!button4"]

    button.grid(row = 0, column=3)
    button.config(command=lambda:draw_resolution(canvas, maze))
    button.config(text="Solve Maze")
    button.config(bg="red")

    button2 = label.children["!button3"]
    
    button2.grid(row=0,column=2)
    button2.config(command=lambda:save_maze(maze))
    button2.config(text="Save Maze")
    
    DX = CAN_WIDTH // width
    DY = CAN_HEIGHT // height
    y = 0
    for line in l:
        x = 0
        for cell in line:
            if x < width - 1 and cell.has_border_right():
                canvas.create_line((x + 1)* DX, y * DY,  (x + 1) * DX, (y + 1) * DY, fill=GRID_COLOR, width = 1)
        
            if y < height - 1 and cell.has_border_bottom():
                canvas.create_line(x * DX, (y + 1) * DY, (x + 1) * DX, (y + 1) * DY, fill=GRID_COLOR, width = 1)
            
            x += 1
        y += 1

def launch_grid():
    can = Canvas(WIN, bg=BG_COLOR, width=CAN_WIDTH, height=CAN_HEIGHT)
    can.grid(row = 1, column = 0)
    label = Label(WIN)
    Button(label, text="Create Perfect Maze", command=lambda:create_perfect_grid(can)).grid(row=0,column = 0)
    Button(label, text='Load Maze', command=lambda:load_perfect_grid(can)).grid(row=0,column=1)
    Button(label)
    Button(label)
    label.grid(row = 0, column = 0, sticky=W)

def load_perfect_grid(canvas):
    filename = filedialog.askopenfilename(initialdir = ".")
    m = Maze.open(Maze, filename)
    draw_grid(canvas, m)

def save_maze(maze):
    filename = filedialog.asksaveasfilename(initialdir = ".")
    maze.save(filename)

def create_perfect_grid(canvas):
    new_window = Tk()
    new_window.title("Perfect Maze")
    Label(new_window, text="Width").grid(row=0)
    Label(new_window, text="Height").grid(row=1)

    e1 = Entry(new_window)
    e1.insert(0, 20)
    e2 = Entry(new_window)
    e2.insert(0, 20)

    e1.grid(row = 0, column = 1)
    e2.grid(row = 1, column = 1)

    Button(new_window, text='Exit', command=new_window.destroy).grid(row=3, column=0, pady = 5)
    Button(new_window, text='Launch', command=lambda:create_maze_for_resolution(canvas, new_window, e1, e2)).grid(row=3, column=1, sticky = W, padx = 10, pady = 5)

def create_maze_for_resolution(canvas, window, e1, e2):
    maze = Maze.create_perfect_maze(Maze, int(e1.get()), int(e2.get()))
    draw_grid(canvas, maze)
    window.destroy()

def main():
    WIN.title('Maze')
    launch_grid()
    WIN.mainloop()
    
if __name__ == '__main__':
    main()
    
    
