from visual import*
from PIL import Image
import guns

team_color = [(25/255.0, 175/255.0, 55/255.0), color.red, color.blue]

class players():
    def __init__(self, ID = 0, NAME = "Anonymous", POS = vector(0, 0, 0), AXIS = vector(1, 0, 0), HEALTH = 100, TEAM = 0, GUN = "pistol", dT = 0.01):
        self.id = ID
        self.name = NAME
        self.pos = POS
        self.axis = AXIS
        self.health = HEALTH
        self.team = TEAM
        self.moving_speed = 1.0
        self.body = frame(pos = self.pos, axis = vector(self.axis.x, 0, self.axis.z), v = vector(0, 0, 0), head = None, torso = None, hands = None, right_leg = None, left_leg = None, visible = False)
        self.body.head = sphere(frame = self.body, pos = vector(0, 1.45, 0), radius = 0.25, axis = vector(1, 0, 0), color = (255/255.0, 204/255.0, 77/255.0), material = materials.texture(data = Image.open("images\\face.tga"), mapping = "sign"))
        self.body.torso = box(frame = self.body, pos = vector(0, 0.85, 0), length = 0.25, width = 0.5, height = 0.7, color = team_color[self.team], material = materials.rough)
        self.body.hands = frame(frame = body, pos = vector(0, 1.1, 0.2))
        sphere(frame = body.hands, pos = vector(0.3, -0.1, 0), radius = 0.08, color = (255/255.0, 168/255.0, 80/255.0), material = materials.diffuse)
        sphere(frame = body.hands, pos = vector(0.45, -0.05, -0.1), radius = 0.08, color = (255/255.0, 168/255.0, 80/255.0), material = materials.diffuse)
        self.body.right_leg = box(frame = self.body, pos = vector(0, 0.3, 0.13), length = 0.6, width = 0.2, height = 0.2, axis = vector(0, -1, 0), color = team_color[self.team], material = materials.rough)
        self.body.left_leg = box(frame = self.body, pos = vector(0, 0.3, -0.13), length = 0.6, width = 0.2, height = 0.2, axis = vector(0, -1, 0), color = team_color[self.team], material = materials.rough)
        self.collision_box = box(frame = self.body, pos = vector(0, 0.85, 0), length = 0.3, width = 0.5, height = 1.7, opacity = 0)
        self.gun = guns.gun_list[GUN](FRAME = self.body.hands)
        self.body.visible = True
        self.dt = dT

    def set_axis(self, AXIS):
        self.axis = AXIS
        horizontal_forward = vector(self.axis.x, 0, self.axis.z)
        tmp_angle = diff_angle(self.body.axis, horizontal_forward)
        if tmp_angle > radians(75):
            self.body.axis = rotate(vector = self.body.axis, angle = dif_angle, axis = cross(self.body.axis, horizontal_forward))
        self.body.head.axis = (self.body).world_to_frame(self.axis) - (self.body).world_to_frame(vector(0,0,0))
        self.body.hands.axis = self.body.head.axis

    def move(self, DIR):
        self.pos += self.moving_speed * norm(DIR) * self.dt
        self.body.pos = self.pos

    def damaged(self, AMOUNT):
        self.health -= AMOUNT

    def healed(self, AMOUNT):
        self.health += AMOUNT

    def fire(self, TARGET):
        self.gun.fire(TARGET)

