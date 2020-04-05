import Polyomino

class GamePiece:
    COLORS = ['white', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
    
    def __init__(self, polyomino):
        self.polyomino = polyomino.copy()
        self.x = 0
        self.y = 0
        self.center = self.get_center()
        self.color = self.get_color()

    def reset(self):
        self.x = 0
        self.y = 0

    def set_position(self):
        self.x = 5 - self.polyomino.width // 2
        self.y = 0 - self.polyomino.height

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def clockwise(self):
        self.polyomino.clockwise()
        self.recenter()

    def counterclockwise(self):
        self.polyomino.counterclockwise()
        self.recenter()

    def recenter(self):
        new_center = self.get_center()
        self.x += self.center[0] - new_center[0]
        self.y += self.center[1] - new_center[1]
        self.center = new_center

    def get_center(self):
        size = max(self.polyomino.width, self.polyomino.height)
        if size % 2 == 0:
            center_x = (self.polyomino.width - 1) // 2 + 0.5
            center_y = (self.polyomino.height - 1) // 2 + 0.5
        else:
            center_x = (self.polyomino.width - 1) // 2
            center_y = (self.polyomino.height - 1) // 2
        return center_x, center_y

    def squares(self):
        return list(map(
            lambda tile: Square(
                tile[0] + self.x,
                tile[1] + self.y,
                self.color,
            ),
            self.polyomino.tiles
        ))

    def get_color(self):
        index = 1
        for c in str(self.polyomino):
            if c == ' ':
                index *= 11
            elif c == '#':
                index *= 13
            else:
                index *= 17
            index += 1
        return self.COLORS[index % len(self.COLORS)]
        
class Square:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

