import GameWindow
import GameManager

class Polyis:
    UPDATE_SPEED = 50
    
    def __init__(self):
        self.gm = GameManager.GameManager(self.UPDATE_SPEED)
        
        self.window = GameWindow.GameWindow()
        self.window.bind('<Key>', self.key_pressed)
        self.window.bind('<KeyRelease>', self.key_released)
        self.window.set_update(self.update, self.UPDATE_SPEED)
        self.window.draw(self.gm)
        self.window.start()

    def update(self):
        self.gm.update()

    def key_pressed(self, event):
        {
            'Up': self.gm.clockwise,
            'Down': self.gm.down_pressed,
            'Left': self.gm.left,
            'Right': self.gm.right,
            'z': self.gm.counterclockwise,
            'x': self.gm.clockwise,
            'c': self.gm.hold,
            'space': self.gm.drop,
            'Shift_L': self.gm.hold,
            'r': self.gm.restart,
        }[event.keysym]()

    def key_released(self, event):
        if event.keysym == 'Down':
            self.gm.down_released()

if __name__ == '__main__':
    Polyis()
