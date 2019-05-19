from visual import*

class guns():
	def __init__(self):
		pass

class pistol(guns):
    def __init__(self, FRAME):
        super().__init__()
        self.damage = 10
        self.obj = extrusion(frame = FRAME, pos = [(0, 0, 0.02), (0, 0, -0.04)], shape = Polygon([(0.25, 0.04), (0.6, 0.04), (0.6, -0.04), (0.35, -0.04), (0.3, -0.23), (0.2, -0.2)]),
                             color = color.gray(0.4), material = materials.rough)

    def __del__(self):
        self.obj.visible = False
        del self.obj

class rifle(guns):
    def __init__(self, FRAME):
        super().__init__()
        self.damage = 15
        self.obj = extrusion(frame = FRAME, pos = [(0, 0, 0.02), (0, 0, -0.04)], shape = Polygon([(0.15, 0.05), (0.4, 0.05), (0.4, 0.08), (0.75, 0.08), (0.75, 0.03), (1, 0.03), (1, 0), (0.75, 0), (0.75, -0.03), (0.6, -0.07), (0.65, -0.25), (0.55, -0.27), (0.5, -0.05), (0.4, -0.05), (0.35, -0.27), (0.3, -0.25), (0.35, -0.05), (0.15, -0.15)]),
                             color = color.gray(0.4), material = materials.rough)

    def __del__(self):
        self.obj.visible = False
        del self.obj

class shotgun(guns):
    def __init__(self, FRAME):
        super().__init__()
        self.damage = 5
        self.obj = extrusion(frame = FRAME, pos = [(0, 0, 0.02), (0, 0, -0.04)], shape = Polygon([(0.15, 0.08), (0.8, 0.08), (0.8, 0.05), (1, 0.05), (1, 0), (0.7, 0), (0.7, -0.03), (0.35, -0.03), (0.15, -0.15)]),
                             color = color.gray(0.4), material = materials.rough)

    def __del__(self):
        for obj in self.obj.objects:
            obj.visible = False
            del obj

gun_list = {"pistol":pistol, "rifle":rifle, "shotgun":shotgun}

class bullets():
    def __init__(self, POS, DAMAGE):
        self.obj = sphere(pos = POS, radius = 0.005, color = color.gray(0.7), make_trail = True, retain = 50)
        self.damage = DAMAGE

    def __del__(self):
        self.obj.visible = False
        del self.obj
