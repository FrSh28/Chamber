from visual import*

class objects():
    def __init__(self):
        pass

class unbreakable_walls(objects):
    def __init__(self, POS, LENGTH, WIDTH):
        super().__init__()
        self.obj = box(pos = POS, length = LENGTH, width = WIDTH, height = 3, color = color.gray(0.4), material = materials.marble)

    def __del__(self):
        self.obj.visible = False
        del self.obj

class breakable_walls(objects):
    def __init__(self, POS, LENGTH, WIDTH):
        super().__init__()
        self.obj = box(pos = POS, length = LENGTH, width = WIDTH, height = 3, color = color.gray(0.6), material = materials.plastic)
        self.strength = 50

    def damaged(self, AMOUNT):
        self.strength -= AMOUNT
        if self.strength <= 0:
            self.destroyed()

    def destroyed(self):
        self.__del__()

    def __del__(self):
        self.obj.visible = False
        del self.obj

class targets(objects):
    def __init__(self, POS, RADIUS, AXIS):
        super().__init__()
        self.obj = cylinder(pos = POS, radius = RADIUS, axis = AXIS, color = color.red, material = materials.rough)

    def __del__(self):
        self.obj.visible = False
        del self.obj

class windows(objects):
    def __init__(self, POS, LENGTH, WIDTH, HEIGHT):
        super().__init__()
        self.obj = box(pos = POS, length = LENGTH, width = WIDTH, height = 3, color = color.gray(0.6), material = materials.ice)
        self.strength = 20

    def damaged(self, AMOUNT):
        self.strength -= AMOUNT
        if self.strength <= 0:
            self.destroyed()

    def destroyed(self):
        self.__del__()

    def __del__(self):
        self.obj.visible = False
        del self.obj
