from Cell import *
from random import *

class Maze:
    def __init__(self, list_of_cells):
        #list dimension 2 of cells
        self.__list_of_cells = list_of_cells
        self.__width = len(list_of_cells[0])
        self.__height = len(list_of_cells)

    def get_width(self):
        return self.__width
    
    def get_list_of_cells(self):
        return  self.__list_of_cells
    
    def get_height(self):
        return self.__height

    def __str__(self):
        res = ""
        for i in range(self.__height):
            if i == 0:
                res += "+-" * self.__width + "+\n"
            for cells in self.__list_of_cells[i]:
                res += str(cells)
            res += "\n"
            for cells in self.__list_of_cells[i]:
                res += cells.get_line_bottom()
            if i == self.__height - 1:
                res += "+"
            else:
                res += "+\n"
        return res

    def get_print_solution(self, path):
        res = ""
        for i in range(self.__height):
            if i == 0:
                res += "+-" * self.__width + "+\n"
            for j in range(self.__width):
                if path[i][j] == False:
                    res += str(self.__list_of_cells[i][j])
                else:
                    res += self.__list_of_cells[i][j].print_full()
            res += "\n"
            for cells in self.__list_of_cells[i]:
                res += cells.get_line_bottom()
            if i == self.__height - 1:
                res += "+"
            else:
                res += "+\n"
        return res

    def print_solution(self):
        path = self.launch_solving()
        if path == False:
            print("There is no solution to this maze !")
            print(self)
        else:
            print("There is at least one solution to this maze !")
            print(self.get_print_solution(path))
    
    def save(self, file_name):
        with open(file_name, "w") as file:
            file.write(str(self.__width) + "\n")
            file.write(str(self.__height) + "\n")
            file.write(str(self) + "\n")

    def open(self, file_name):
        with open(file_name, "r") as file:
            width = int(file.readline())
            height = int(file.readline())
            file.readline()
            file.read(1)
            res = file.read()
        l = []
        p = -1
        for i in range(height):
            k = []
            for j in range(width):
                p += 2 # 2 characters
                has_border_right = res[p] == "|" 
                has_border_bottom = res[p + 2 * width + 1] == "-" #there is \n and 2 width equals the entire width of characters
                cell = Cell(j, i, has_border_right, has_border_bottom)
                k += [cell]
            p += width * 2 + 4 #there is 2 \n and | and + 
            l += [k]
        return Maze(l)

    def create_perfect_maze(self, width, height):
        l = []
        for i in range(0, height):
            k = []
            for j in range(0, width):
                k += [Cell(j, i, True, True)]
            l += [k]
        dic = {}
        for i in range(0, height):
            for j in range(0, width):
                dic[i * width + j + 1] = [l[i][j]]
        
        n = width * height
        while len(dic) > 1:
            i = choice(transform_keys_to_list(dic))
            k = choice(dic[i])
            choice_neighbours = []
            coord = (k.get_x(), k.get_y())
            
            if coord[0] < width - 1 and get_index_of(dic, Cell(coord[0] + 1, coord[1], True, True)) != i:
                choice_neighbours += [(coord[0] + 1, coord[1])]
            if coord[1] < height - 1 and get_index_of(dic, Cell(coord[0], coord[1] + 1, True, True)) != i:
                choice_neighbours += [(coord[0], coord[1] + 1)]
            if coord[0] > 0 and get_index_of(dic, Cell(coord[0] - 1, coord[1], True, True)) != i:
                choice_neighbours += [(coord[0] - 1, coord[1])]
            if coord[1] > 0 and get_index_of(dic, Cell(coord[0], coord[1] - 1, True, True)) != i:
                choice_neighbours += [(coord[0], coord[1] - 1)]

            if len(choice_neighbours) > 0:
                choice_final = choice(choice_neighbours)
                index = get_index_of(dic, Cell(choice_final[0], choice_final[1], True, True))
                
                if coord[0] < choice_final[0]:
                    l[coord[1]][coord[0]].set_border_right(False)
                elif coord[0] > choice_final[0]:
                    l[choice_final[1]][choice_final[0]].set_border_right(False)
                elif coord[1] < choice_final[1]:
                    l[coord[1]][coord[0]].set_border_bottom(False)
                else:
                    l[choice_final[1]][choice_final[0]].set_border_bottom(False)
                      
                dic[i] += dic[index]
                dic = copy_without(dic, index)

        return Maze(l)

    def launch_solving(self):
        l = []
        path = []
        for i in range(self.__height):
            k = []
            path_k = []
            for j in range(self.__width):
                k += [False]
                path_k += [False]
            l += [k]
            path += [path_k]
        found_path = self.__solve_maze(0, 0, l, path)
        if found_path:
            return path
        return False

    def __solve_maze(self, x, y, l, path):
        if x == self.__width - 1 and y == self.__height - 1:
            path[y][x] = True
            return True
        if (self.__list_of_cells[y][x].has_border_right() and self.__list_of_cells[y][x].has_border_bottom() and
            ((x > 0 and self.__list_of_cells[y][x - 1].has_border_right()) or (y > 0 and self.__list_of_cells[y - 1][x].has_border_bottom()))) or l[y][x] == True:
            return False
        l[y][x] = True
        if not self.__list_of_cells[y][x].has_border_right() and self.__solve_maze(x + 1, y, l, path):
            path[y][x] = True
            return True
        if x > 0 and not self.__list_of_cells[y][x - 1].has_border_right() and self.__solve_maze(x - 1, y, l, path):
            path[y][x] = True
            return True
        if y > 0 and not self.__list_of_cells[y - 1][x].has_border_bottom() and self.__solve_maze(x, y - 1, l, path):
            path[y][x] = True
            return True
        if not self.__list_of_cells[y][x].has_border_bottom() and self.__solve_maze(x, y + 1, l, path):
            path[y][x] = True
            return True
        return False

def get_index_of(dic, cell):
    for key in dic.keys():
        l = dic[key]
        if cell in l:
            return key

def copy_without(dic, key):
    dic2 = {}
    for key_loop in dic.keys():
        if key_loop != key:
            dic2[key_loop] = dic[key_loop]

    return dic2

def transform_keys_to_list(dic):
    l = []
    for key in dic.keys():
        l += [key]
    return l

MAZE1 = Maze([[Cell(0, 0, True, False), Cell(1, 0, True, True)],
              [Cell(0, 1, False, True), Cell(1, 1, True, True)]])

MAZE2 = Maze([[Cell(0, 0, False, False), Cell(1, 0, False, False), Cell(2, 0, True, True)],
              [Cell(0, 1, False, True), Cell(1, 1, True, True), Cell(2, 1, True, True)]])
