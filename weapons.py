from visual import*
import random

class guns(object):
	def __init__(self):
		pass

class pistol(guns):
    def __init__(self, FRAME, AMMUNITION = 100):
        super(pistol, self).__init__()
        self.damage = 7
        self.ammunition = AMMUNITION
        self.obj = extrusion(frame = FRAME, pos = [(0, 0, 0.02), (0, 0, -0.04)], shape = Polygon([(0.25, 0.04), (0.6, 0.04), (0.6, -0.04), (0.35, -0.04), (0.3, -0.23), (0.2, -0.2)]),
                             color = color.gray(0.4), material = materials.rough, frames = (FRAME,) + FRAME.frames)

    def fire(self, DIR):
        tmp_pos = vector(0.6, 0, -0.01)
        for f in self.obj.frames:
            tmp_pos = f.frame_to_world(tmp_pos)
        #self.ammunition -= 1
        return [bullets(POS = tmp_pos, DAMAGE = self.damage, DIR = norm(DIR)+vector(0, 0.003, 0))]

    def set_invisible(self):
        self.obj.visible = False

    def __del__(self):
        self.set_invisible()
        del self.obj

class rifle(guns):
    def __init__(self, FRAME, AMMUNITION = 100):
        super(rifle, self).__init__()
        self.damage = 10
        self.ammunition = AMMUNITION
        self.obj = extrusion(frame = FRAME, pos = [(0, 0, 0.02), (0, 0, -0.04)], shape = Polygon([(0.15, 0.05), (0.4, 0.05), (0.4, 0.08), (0.75, 0.08), (0.75, 0.03), (1, 0.03), (1, 0), (0.75, 0), (0.75, -0.03), (0.6, -0.07), (0.65, -0.25), (0.55, -0.27), (0.5, -0.05), (0.4, -0.05), (0.35, -0.27), (0.3, -0.25), (0.35, -0.05), (0.15, -0.15)]),
                             color = color.gray(0.4), material = materials.rough, frames = (FRAME,) + FRAME.frames)

    def fire(self, DIR):
        tmp_pos = vector(1, 0, -0.01)
        for f in self.obj.frames:
            tmp_pos = f.frame_to_world(tmp_pos)
        #self.ammunition -= 1
        return [bullets(POS = tmp_pos, DAMAGE = self.damage, DIR = norm(DIR)+vector(0, 0.003, 0))]

    def set_invisible(self):
        self.obj.visible = False

    def __del__(self):
        self.set_invisible()
        del self.obj

class shotgun(guns):
    def __init__(self, FRAME, AMMUNITION = 100):
        super(shotgun, self).__init__()
        self.damage = 1
        self.ammunition = AMMUNITION
        self.obj = extrusion(frame = FRAME, pos = [(0, 0, 0.02), (0, 0, -0.04)], shape = Polygon([(0.15, 0.08), (0.8, 0.08), (0.8, 0.05), (1, 0.05), (1, 0), (0.7, 0), (0.7, -0.03), (0.35, -0.03), (0.15, -0.15)]),
                             color = color.gray(0.4), material = materials.rough, frames = (FRAME,) + FRAME.frames)

    def fire(self, DIR):
        tmp_pos = vector(1, 0, -0.01)
        for f in self.obj.frames:
            tmp_pos = f.frame_to_world(tmp_pos)
        #self.ammunition -= 1
        rd1, rd2 = random.random(), random.random()
        return [bullets(POS = tmp_pos, DAMAGE = self.damage, DIR = (norm(DIR)+vector(0, 0.003, 0)).rotate(angle = (rd1*i)%0.07, axis = vector((rd1*i)%(rd2/i), (rd2*rd1*i)%(rd1/i), (rd2+rd1)%((rd1-rd2+0.0000001)/i)))) for i in range(1, 11)]

    def set_invisible(self):
        self.obj.visible = False

    def __del__(self):
        self.set_invisible()
        del self.obj

gun_list = {"pistol":pistol, "rifle":rifle, "shotgun":shotgun}

class bullets(object):
    def __init__(self, POS, DAMAGE, DIR):
        self.obj = sphere(pos = POS, radius = 0.02, color = color.gray(0.7), v = norm(DIR) * 20, make_trail = True, retain = 10)
        self.damage = DAMAGE
        self.time_left = 5.0

    def hit(self):
        self.obj.v = vector(0, 0, 0)

    def set_invisible(self):
        self.obj.trail_object.visible = False
        self.obj.visible = False

    def __del__(self):
        self.set_invisible()
        del self.obj.trail_object, self.obj
