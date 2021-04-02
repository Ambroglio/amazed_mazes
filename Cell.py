class Cell:
    def __init__(self, x, y, has_border_right, has_border_bottom):
        self.__x = x
        self.__y = y
        self.__has_border_right = has_border_right
        self.__has_border_bottom = has_border_bottom

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def has_border_right(self):
        return self.__has_border_right

    def set_border_right(self, has_border_right):
        self.__has_border_right = has_border_right

    def set_border_bottom(self, has_border_bottom):
        self.__has_border_bottom = has_border_bottom

    def has_border_bottom(self):
        return self.__has_border_bottom

    def __str__(self):
        if (self.__x == 0):
            if self.__has_border_right:
                return "| |"
            else:
                return "|  "
        else:
            if self.__has_border_right:
                return " |"
            else:
                return "  "

    def print_full(self):
        if (self.__x == 0):
            if self.__has_border_right:
                return "|o|"
            else:
                return "|o "
        else:
            if self.__has_border_right:
                return "o|"
            else:
                return "o "

    def get_line_bottom(self):
        if self.__has_border_bottom:
            return "+-"
        else:
            return "+ "

    def __eq__(self, other):
        return self.__x == other.get_x() and self.__y == other.get_y()
