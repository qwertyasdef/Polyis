import Polyomino
import GamePiece
import random

class GameManager:

    def __init__(self, FPS):
        self.time = 0
        self.speed = 1
        self.FPS = FPS
        self.is_down = False
        self.game_over = False
        self.level = 0
        self.score = 0
        self.current = None
        self.held = None
        self.upcoming = [] # 0 is next, 1-3 are preview
        self.placed = [] # list of squares, not polyominos

        while len(self.upcoming) < 4:
            self.update_pieces()

    def update_pieces(self):
        if self.game_over:
            return

        if len(self.upcoming) < 5:
            self.upcoming += self.get_pieces()
        self.current = self.current or self.upcoming.pop(0)
        self.current.set_position()

    def clockwise(self):
        if self.game_over:
            return

        self.current.clockwise()
        if not self.rotation_kick():
            self.current.counterclockwise()

    def counterclockwise(self):
        if self.game_over:
            return

        self.current.counterclockwise()
        if not self.rotation_kick():
            self.current.clockwise()

    def rotation_kick(self):
        original_x = self.current.x
        original_y = self.current.y

        # BFS to see if the piece fits somewhere below
        queue = [(0, 0)]
        visited = []
        while len(queue) > 0:
            pos = queue.pop(0)
            if pos in visited:
                continue
            visited.append(pos)

            self.current.x = original_x + pos[0]
            self.current.y = original_y + pos[1]
            if not self.collide():
                return True

            if abs(pos[1] + 1) <= self.current.polyomino.height / 2:
                queue.append((pos[0], pos[1] + 1))
            if abs(pos[0] - 1) <= self.current.polyomino.width / 2:
                queue.append((pos[0] - 1, pos[1]))
            if abs(pos[0] + 1) <= self.current.polyomino.width / 2:
                queue.append((pos[0] + 1, pos[1]))
        self.current.x = original_x
        self.current.y = original_y

        # BFS to see if the piece fits somewhere above
        queue = [(0, -1)]
        visited = []
        while len(queue) > 0:
            pos = queue.pop(0)
            if pos in visited:
                continue
            visited.append(pos)

            self.current.x = original_x + pos[0]
            self.current.y = original_y + pos[1]
            if not self.collide():
                return True

            if abs(pos[1] - 1) <= self.current.polyomino.height / 2:
                queue.append((pos[0], pos[1] - 1))
            if abs(pos[0] - 1) <= self.current.polyomino.width / 2:
                queue.append((pos[0] - 1, pos[1]))
            if abs(pos[0] + 1) <= self.current.polyomino.width / 2:
                queue.append((pos[0] + 1, pos[1]))
        self.current.x = original_x
        self.current.y = original_y

        # Couldn't perform any kicks to make the piece not collide
        return False

    def left(self):
        if self.game_over:
            return

        self.current.left()
        if self.collide():
            self.current.right()

    def right(self):
        if self.game_over:
            return

        self.current.right()
        if self.collide():
            self.current.left()

    def down_pressed(self):
        if self.game_over:
            return

        self.is_down = True

    def down_released(self):
        if self.game_over:
            return

        self.is_down = False

    def down(self):
        self.current.down()
        if self.collide():
            self.current.up()
            self.place()

    def drop(self):
        if self.game_over:
            return

        while not self.collide():
            self.current.down()
        self.current.up()
        self.place()

    def place(self):
        self.placed += self.current.squares()
        self.clear_lines()
        self.check_game_over()
        self.current = None
        self.update_pieces()
        self.speed += 0.01

    def hold(self):
        if self.game_over:
            return

        time = 0
        if self.held is None:
            self.held = self.current
            self.current = None
            self.update_pieces()
        else:
            self.held, self.current = self.current, self.held
            self.current.set_position()
        self.held.reset()

    def collide(self):
        for square in self.current.squares():
            if square in self.placed:
                return True
            if square.x < 0 or square.x >= 10:
                return True
            if square.y >= 20:
                return True
        return False

    def clear_lines(self):
        points = 0
        lines = 0
        y = 20
        while y > 0:
            y -= 1
            if y not in map(lambda square: square.y, self.current.squares()):
                continue
            clear = True
            for x in range(10):
                if GamePiece.Square(x, y, '') not in self.placed:
                    clear = False
            if clear:
                for x in range(10):
                    self.placed.remove(GamePiece.Square(x, y, ''))
                for square in self.placed:
                    if square.y < y:
                        square.y += 1
                y += 1
                lines += 1
                if points == 0:
                    points = 50
                else:
                    points *= lines
        self.score += points


    def check_game_over(self):
        for square in self.placed:
            if square.y < 0:
                self.game_over = True

    def restart(self):
        self.__init__(self.FPS)

    def get_pieces(self):
        self.level += 1
        polyominos = []
        for i in range(1, self.level + 1):
            polyominos += Polyomino.generate(i)
        random.shuffle(polyominos)
        return map(lambda polyomino: GamePiece.GamePiece(polyomino), polyominos)

    def update(self):
        if self.game_over:
            return

        self.time += 1

        real_speed = self.speed
        if self.is_down:
            real_speed = max(8, self.speed)

        if self.time >= self.FPS // real_speed:
            self.down()
            self.time = 0
