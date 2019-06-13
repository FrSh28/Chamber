from visual import*
from PIL import Image
import weapons as wp

team_color = [(25/255.0, 175/255.0, 55/255.0), color.red, color.blue]
dying = []

class players():
    def __init__(self, ID = 0, NAME = "Anonymous", SCENE = None, POS = vector(0, 0, 0), AXIS = vector(1, 0, 0), HEALTH = 100, TEAM = 0, WEAPON = "pistol", dT = 0.01):
        self.ID = ID
        self.name = NAME
        self.scene = SCENE
        self.pos = POS
        self.axis = AXIS
        self.horizontal_axis = vector(self.axis.x, 0, self.axis.z)
        self.health = HEALTH
        self.team = TEAM
        self.moving_speed = 30.0
        self.v = vector(0, 0, 0)
        self.key_pressed = {"w":0, "a":0, "s":0, "d":0}
        self.body = frame(pos = self.pos, axis = self.horizontal_axis, frames = (), head = None, torso = None, hands = None, right_leg = None, left_leg = None, visible = False)
        self.body.head = sphere(frame = self.body, pos = vector(0, 1.45, 0), radius = 0.25, axis = vector(1, 0, 0), color = (255/255.0, 204/255.0, 77/255.0), material = materials.texture(data = Image.open("images\\face.tga"), mapping = "sign"))
        self.body.torso = box(frame = self.body, pos = vector(0, 0.85, 0), length = 0.25, width = 0.5, height = 0.7, color = team_color[self.team], material = materials.rough)
        self.body.hands = frame(frame = self.body, pos = vector(0, 1.25, 0.15), frames = (self.body,) + self.body.frames)
        right_hand = sphere(frame = self.body.hands, pos = vector(0.3, -0.1, 0), radius = 0.08, color = (255/255.0, 168/255.0, 80/255.0), material = materials.diffuse)
        left_hand = sphere(frame = self.body.hands, pos = vector(0.45, -0.05, -0.1), radius = 0.08, color = (255/255.0, 168/255.0, 80/255.0), material = materials.diffuse)
        self.body.right_leg = box(frame = self.body, pos = vector(0, 0.3, 0.13), length = 0.6, width = 0.2, height = 0.2, axis = vector(0, -1, 0), color = team_color[self.team], material = materials.rough)
        self.body.left_leg = box(frame = self.body, pos = vector(0, 0.3, -0.13), length = 0.6, width = 0.2, height = 0.2, axis = vector(0, -1, 0), color = team_color[self.team], material = materials.rough)
        self.collision_box = box(frame = self.body, pos = vector(0, 0.85, 0), length = 0.3, width = 0.5, height = 1.7, frames = (self.body,) + self.body.frames, visible = False)
        self.weapon_name = WEAPON
        self.weapon = wp.gun_list[WEAPON](SCENE = self.scene, FRAME = self.body.hands)
        self.body.visible = True
        self.dt = dT

    def set_vision_axis(self, AXIS):
        self.axis = AXIS
        self.horizontal_axis = vector(self.axis.x, 0, self.axis.z)
        tmp_angle = diff_angle(self.body.axis, self.horizontal_axis)
        if tmp_angle > radians(60):
            self.body.axis = rotate(vector = self.body.axis, angle = tmp_angle-radians(60), axis = cross(self.body.axis, self.horizontal_axis))
        self.body.head.axis = (self.body).world_to_frame(self.axis) - (self.body).world_to_frame(vector(0,0,0))
        self.body.hands.axis = self.body.head.axis
        self.body.hands.up = rotate(vector = self.body.hands.axis, angle = radians(90), axis = cross(self.body.hands.axis, (-self.body.hands.axis+vector(0, 1, 0))))

    def set_body_axis(self, AXIS):
        self.body.axis = vector(AXIS.x, 0, AXIS.z)

    def mouse_method(self, evt, bullets_list):
        b = evt.button
        if b == "left":
            self.scene.select()
            bullets_list += self.weapon.fire(scene.mouse.ray)

    def kb_method(self, evt):
        k = evt.key
        if k == "escape":
            pass
        elif k == "r":
            self.weapon.reload(100)

    def moving_method_down(self, evt):
        k = evt.key
        print k
        if k == "w":
            self.key_pressed["w"] = 1
            self.key_pressed["s"] = 0
        elif k == "s":
            self.key_pressed["s"] = 1
            self.key_pressed["w"] = 0
        elif k == "a":
            self.key_pressed["a"] = 1
            self.key_pressed["d"] = 0
        elif k == "d":
            self.key_pressed["d"] = 1
            self.key_pressed["a"] = 0
        self.set_moving()

    def moving_method_up(self, evt):
        k = evt.key
        if k == "w":
            self.key_pressed["w"] = 0
        elif k == "s":
            self.key_pressed["s"] = 0
        elif k == "a":
            self.key_pressed["a"] = 0
        elif k == "d":
            self.key_pressed["d"] = 0
        self.set_moving()

    def set_moving(self):
        tmp_dir = vector(0, 0, 0)
        if self.key_pressed["w"]:
            tmp_dir += vector(1, 0, 0)
        elif self.key_pressed["s"]:
            tmp_dir += vector(-1, 0, 0)
        if self.key_pressed["a"]:
            tmp_dir += vector(0, 0, -1)
        elif self.key_pressed["d"]:
            tmp_dir += vector(0, 0, 1)
        forward = vector(self.scene.forward.x, 0, self.scene.forward.z)
        tmp_dir = rotate(vector = forward, angle = diff_angle(vector(1, 0, 0), tmp_dir), axis = cross(vector(1, 0, 0), tmp_dir))
        self.v = self.moving_speed * norm(tmp_dir)
        self.set_body_axis(forward)

    def damaged(self, AMOUNT):
        self.health -= AMOUNT
        if self.health <= 0:
            self.health = 0
            self.die()

    def healed(self, AMOUNT):
        self.health += AMOUNT
        if self.health > 100:
            self.health = 100

    def die(self):
        self.__del__()

    def set_invisible(self):
        self.weapon.set_invisible()
        self.body.visible = False

    def __del__(self):
        del self.weapon
        for obj in self.body.hands.objects:
            obj.visible = False
            del obj
        for obj in self.body.objects:
            obj.visible = False
            del obj

