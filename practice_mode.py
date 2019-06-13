from visual import*
import players as pl
import objects as ob
import weapons as wp
import random as rd
import practice_mode
import os

class practice_mode(object):
    def __init__(self, SCENE, MULTIPLAYER, MSG_QUEUE = None):
        self.scene = SCENE
        self.scene.select()
        self.start = False
        self.playernum = 0
        self.players = {}
        self.player_IDs = []
        self.log = {"exp": 0,
                    "kill": 0,
                    "death": 0,
                    "score": 0}
        self.multiplayer = MULTIPLAYER
        if self.multiplayer:
            self.msg_queue = MSG_QUEUE

    def join(self, PLAYER, SELF = False):
        self.playernum += 1
        if SELF:
            self.self_ID = PLAYER.ID
        self.player_IDs.append(PLAYER.ID)
        self.players[PLAYER.ID] = PLAYER

    def leave(self, PLAYER_ID):
        self.playernum -= 1
        del self.player_IDs[self.player_IDs.index(PLAYER.ID)]
        del self.players[PLAYER.ID]
        if self.playernum == 0:
            self.__del__()

    def loop(self):
        self.start = True
        self.scene.select()
        bullets_list = []
        targets_list = []
        self.scene.bind("keydown", self.players[self.self_ID].moving_method_down)
        self.scene.bind("keyup", self.players[self.self_ID].moving_method_up)
        self.scene.bind("click", self.players[self.self_ID].mouse_method, bullets_list)

        while True:
            rate(1/self.scene.dt)
            self.scene.center = (self.players[self.self_ID].body).frame_to_world(self.players[self.self_ID].body.head.pos)
            self.players[self.self_ID].set_vision_axis(self.scene.mouse.ray)

            if rd.random() < 0.005 and len(targets_list) < 10:
                targets_list.append(ob.targets(POS = vector(rd.random()*40-20, 2.5, rd.random()*40-20), RADIUS = 0.5, AXIS = vector(1, 0, 0)))

            for obj in self.scene.objects:
                if hasattr(obj, "v"):
                    obj.pos += obj.v * self.scene.dt
                    if type(obj) == pl.players:
                        obj.body.pos = obj.pos

            for bul in bullets_list:
                if bul.time_left <= 0:
                    bul.hit()
                    bul.set_invisible()
                    try:
                        del bullets_list[bullets_list.index(bul)]
                    except:
                        pass
                else:
                    bul.time_left -= self.scene.dt
                    for item in gameroom:
                        tmp = bul.obj.pos - item.obj.pos 
                        if (abs(tmp.x) <= (item.obj.length / 2) and
                            abs(tmp.y) <= (item.obj.height / 2) and
                            abs(tmp.z) <= (item.obj.width / 2)):
                            bul.hit()
                            bul.set_invisible()
                            try:
                                del bullets_list[bullets_list.index(bul)]
                            except:
                                pass
                    for item in targets_list:
                        tmp = bul.obj.pos - item.obj.pos 
                        if mag(tmp) <= (item.obj.radius):
                            self.log["exp"] += 1
                            item.set_invisible()
                            try:
                                del targets_list[targets_list.index(item)]
                            except:
                                pass
                            bul.hit()
                            bul.set_invisible()
                            try:
                                del bullets_list[bullets_list.index(bul)]
                            except:
                                pass

    def get_result(self):
        return self.log

    #def __del__(self):
    #    pass


