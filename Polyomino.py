class Polyomino:
    def __init__(self, *tiles):
        self.tiles = list(tiles)
        self.normalize()
        
        width, height = 0, 0
        for tile in self.tiles:
            if tile[0] > width:
                width = tile[0]
            if tile[1] > height:
                height = tile[1]
        self.width, self.height = width + 1, height + 1

        # Rotate to put center of mass as high as possible
        center_x = sum(map(lambda tile: tile[0], self.tiles)) / len(self.tiles)
        center_y = sum(map(lambda tile: tile[1], self.tiles)) / len(self.tiles)
        distances = [center_y, center_x, height - center_y, width - center_x]
        rotations = min(enumerate(distances), key=(lambda t: t[1]))[0]
        for i in range(rotations):
            self.clockwise()

    def normalize(self):
        self.to_first_quad()
        self.tiles.sort()

    def __eq__(self, other):
        if len(self.tiles) != len(other.tiles):
            return False
        for i in range(4):
            if self.is_translated(other):
                return True
            self.clockwise()
        return False

    def copy(self):
        return Polyomino(*self.tiles)

    def is_translated(self, other):
        if len(self.tiles) != len(other.tiles):
            return False
        diff = (self.tiles[0][0] - other.tiles[0][0], self.tiles[0][1] - other.tiles[0][1])
        for self_tile, other_tile in zip(self.tiles, other.tiles):
            if diff != (self_tile[0] - other_tile[0], self_tile[1] - other_tile[1]):
                return False
        return True

    def to_first_quad(self):
        min_x, min_y = self.tiles[0]
        for tile in self.tiles:
            if min_x > tile[0]:
                min_x = tile[0]
            if min_y > tile[1]:
                min_y = tile[1]
        self.translate(-min_x, -min_y)

    def translate(self, dx, dy):
        for i, tile in enumerate(self.tiles):
            self.tiles[i] = (tile[0] + dx, tile[1] + dy)
    
    def clockwise(self):
        for i, tile in enumerate(self.tiles):
            self.tiles[i] = (-tile[1], tile[0])
        self.width, self.height = self.height, self.width
        self.normalize()

    def counterclockwise(self):
        for i, tile in enumerate(self.tiles):
            self.tiles[i] = (tile[1], -tile[0])
        self.width, self.height = self.height, self.width
        self.normalize()

    def __str__(self):
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.tiles:
                    s += '#'
                else:
                    s += ' '
            s += '\n'
        return s
            

polyominos = [
    None,
    [ Polyomino((0, 0)) ],
]

def generate(size):
    if len(polyominos) > size:
        return polyominos[size]
    
    pieces = []
    smaller_pieces = generate(size - 1)
    for piece in smaller_pieces:
        for tile in reversed(piece.tiles):
            for new_tile in neighbours(tile):
                if new_tile not in piece.tiles:
                    new_piece = Polyomino(*piece.tiles, new_tile)
                    if new_piece not in pieces:
                        pieces.append(new_piece)
    polyominos.append(pieces)
    return pieces

def neighbours(tile):
    return (
        (tile[0] + 1, tile[1]),
        (tile[0], tile[1] + 1),
        (tile[0] - 1, tile[1]),
        (tile[0], tile[1] - 1),
    )
