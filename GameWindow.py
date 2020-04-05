import tkinter
from PIL import Image, ImageTk

class GameWindow:
    
    SQUARE_SIZE = 30
    BOX_SIZE = 4 * SQUARE_SIZE
    BOARD_WIDTH = 10 * SQUARE_SIZE
    BOARD_HEIGHT = 20 * SQUARE_SIZE
    FPS = 50

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.configure(bg='light gray')
        
        frame = tkinter.Frame(
            self.window,
            bg='light gray',
        )
        frame.pack(anchor='center')

        left = tkinter.Frame(
            frame,
            bg='light gray',
        )
        left.pack(side='left', fill='y', padx=50, pady=50)

        held_label = tkinter.Label(
            left,
            text='Held',
            font=('Helvetica', 20),
            fg='black',
            bg='light gray',
            anchor='w',
        )
        held_label.pack(fill='x')

        held = tkinter.Canvas(
            left,
            width=self.BOX_SIZE,
            height=self.BOX_SIZE,
            bg='black',
            highlightthickness=0,
        )
        held.pack()

        score = tkinter.Label(
            left,
            text='Score: 0',
            font=('Helvetica', 16),
            fg='black',
            bg='light gray',
            anchor='w',
        )
        score.pack(fill='x', pady=50)

        center = tkinter.Frame(
            frame,
            bg='light gray',
        )
        center.pack(side='left', pady=50)
        
        board = tkinter.Canvas(
            center,
            width=self.BOARD_WIDTH,
            height=self.BOARD_HEIGHT,
            bg='black',
            highlightthickness=0,
        )
        board.pack()

        overlay = Image.new(
            'RGBA',
            (self.BOARD_WIDTH, self.BOARD_HEIGHT),
            (128, 128, 128, 192),
        )
        self.overlay = ImageTk.PhotoImage(overlay)

        right = tkinter.Frame(
            frame,
            bg='light gray',
        )
        right.pack(side='left', fill='y', padx=50, pady=50)

        next_label = tkinter.Label(
            right,
            text='Next',
            font=('Helvetica', 20),
            fg='black',
            bg='light gray',
            anchor='w',
        )
        next_label.pack(fill='x')

        next = tkinter.Canvas(
            right,
            width=self.BOX_SIZE,
            height=self.BOX_SIZE,
            bg='black',
            highlightthickness=0,
        )
        next.pack()
        
        preview = tkinter.Canvas(
            right,
            width=self.BOX_SIZE,
            height=3*self.BOX_SIZE,
            bg='black',
            highlightthickness=0,
        )
        preview.pack(pady=25)

        self.held = held
        self.score = score
        self.board = board
        self.next = next
        self.upcoming = preview

    def bind(self, event, handler):
        self.window.bind(event, handler)

    def update(self):
        pass

    def set_update(self, update, speed):
        def _update():
            update()
            self.window.after(1000 // speed, _update)
        self.update = _update

    def draw(self, gm):
        self.board.delete('all')
        self.held.delete('all')
        self.next.delete('all')
        self.upcoming.delete('all')
        
        for square in gm.placed:
            self.draw_square(self.board, square, self.SQUARE_SIZE)

        if gm.current is not None:
            for square in gm.current.squares():
                self.draw_square(self.board, square, self.SQUARE_SIZE)

        if gm.held is not None:
            self.preview(self.held, 0, gm.held)

        self.score['text'] = 'Score: ' + str(gm.score)

        self.preview(self.next, 0, gm.upcoming[0])
        for i in range(1, 4):
            self.preview(self.upcoming, i - 1, gm.upcoming[i])

        if gm.game_over:
            self.board.create_image(0, 0, image=self.overlay, anchor='nw')
            
            self.board.create_text(
                self.BOARD_WIDTH / 2,
                self.BOARD_HEIGHT / 2 - 24,
                anchor='center',
                font=('Helvetica', 32),
                fill='white',
                text='Game Over',
            )
            self.board.create_text(
                self.BOARD_WIDTH / 2,
                self.BOARD_HEIGHT / 2 + 24,
                anchor='center',
                font=('Helvetica', 16),
                fill='white',
                text='Press <R> to restart',
            )
        
        self.window.after(1000 // self.FPS, self.draw, gm)

    def draw_square(self, canvas, square, size):
        canvas.create_rectangle(
            square.x * size, square.y * size,
            (square.x + 1) * size, (square.y + 1) * size,
            fill=square.color
        )

    def preview(self, canvas, position, game_piece):
        margin = 10
        size = max(game_piece.polyomino.width, game_piece.polyomino.height)
        square_size = min((self.BOX_SIZE - 2 * margin) / size, self.SQUARE_SIZE)
        width = square_size * game_piece.polyomino.width
        height = square_size * game_piece.polyomino.height
        x = (self.BOX_SIZE - width) / 2
        y = (self.BOX_SIZE - height) / 2 + position * self.BOX_SIZE
        for square in game_piece.squares():
            self.preview_square(canvas, x, y, square, square_size)

    def preview_square(self, canvas, x, y, square, size):
        canvas.create_rectangle(
            square.x * size + x, square.y * size + y,
            (square.x + 1) * size + x, (square.y + 1) * size + y,
            fill=square.color
        )

    def start(self):
        self.update()
        self.window.mainloop()
