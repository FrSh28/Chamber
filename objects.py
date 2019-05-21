from visual import*

class objects(object):
    def __init__(self):
        pass

class unbreakable_walls(objects):
    def __init__(self, POS, X_LENGTH, Z_LENGTH, HEIGHT = 3):
        super(unbreakable_walls, self).__init__()
        self.obj = box(pos = POS, length = X_LENGTH, width = Z_LENGTH, height = HEIGHT, color = color.gray(0.6), material = materials.marble)

    def set_invisible(self):
        self.obj.visible = False

    def __del__(self):
        self.set_invisible()
        del self.obj

class breakable_walls(objects):
    def __init__(self, POS, X_LENGTH, Z_LENGTH, HEIGHT = 3):
        super(breakable_walls, self).__init__()
        self.obj = box(pos = POS, length = X_LENGTH, width = Z_LENGTH, height = HEIGHT, color = color.gray(0.8), material = materials.plastic)
        self.strength = 50

    def damaged(self, AMOUNT):
        self.strength -= AMOUNT
        if self.strength <= 0:
            self.destroyed()

    def destroyed(self):
        self.__del__()

    def set_invisible(self):
        self.obj.visible = False

    def __del__(self):
        self.set_invisible()
        del self.obj

class targets(objects):
    def __init__(self, POS, RADIUS, AXIS = vector(1, 0, 0)):
        super(targets, self).__init__()
        self.obj = sphere(pos = POS, radius = RADIUS, axis = AXIS, color = color.red, material = materials.rough)

    def damaged(self, AMOUNT):
        self.strength -= AMOUNT
        if self.strength <= 0:
            self.destroyed()

    def destroyed(self):
        self.__del__()

    def set_invisible(self):
        self.obj.visible = False

    def __del__(self):
        self.set_invisible()
        del self.obj

class windows(objects):
    def __init__(self, POS, X_LENGTH, Z_LENGTH, HEIGHT):
        super(windows, self).__init__()
        self.obj = box(pos = POS, length = X_LENGTH, width = Z_LENGTH, height = HEIGHT, color = color.gray(0.6), material = materials.ice)
        self.strength = 20

    def damaged(self, AMOUNT):
        self.strength -= AMOUNT
        if self.strength <= 0:
            self.destroyed()

    def destroyed(self):
        self.__del__()

    def set_invisible(self):
        self.obj.visible = False

    def __del__(self):
        self.set_invisible()
        del self.obj
