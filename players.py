import visual as vpy

class players():
    def __init__(self, id, name, pos, team = None):
        self.id = id
        self.name = name
        self.pos = pos
        self.health = 100
        if team:
            self.team = team
        self.moving_speed = 1.0
        self.body = vpy.frame(pos = pos, head = sphere(pos = vector(0, 1.6, 0), radius = 0.15, color = ))
