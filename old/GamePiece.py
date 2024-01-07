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
        new_center = (self.polyomino.width - 1 - self.center[1], self.center[0])
        self.recenter(new_center)

    def counterclockwise(self):
        self.polyomino.counterclockwise()
        new_center = (self.center[1], self.polyomino.height - 1 - self.center[0])
        self.recenter(new_center)

    def recenter(self, new_center):
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
        # These numbers experimentally produce a good distribution
        index = 1
        for c in str(self.polyomino):
            index *= 3
            if c == ' ':
                index += 5
            elif c == '#':
                index += 3
            else:
                index += 6
        return self.COLORS[index % len(self.COLORS)]
        
class Square:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def hash_test(n):
    a = []
    for i in range(1, n + 1):
        a += Polyomino.generate(i)
    a = map(lambda p: GamePiece(p).color, a)
    dist = {}
    for c in a:
        if c in dist:
            dist[c] += 1
        else:
            dist[c] = 1
    print(dist)
