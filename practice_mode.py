from visual import*
import players as pl
import objects as ob
import weapons as wp
import random as rd
import practice_mode
import team_mode
import FFA_mode
import os

scene = display(x = 0, y= 0, width = 1200, height = 700, center = vector(0, 2, 0), background = color.black, title = "FPS", dt = 0.01, lights = [], range = 0.3, autoscale = False, userzoom = False)

gameroom = [ob.unbreakable_walls(POS = vector(-20.5, 2, 0), X_LENGTH = 1, Z_LENGTH = 50, HEIGHT = 4),
            ob.unbreakable_walls(POS = vector(20.5, 2, 0), X_LENGTH = 1, Z_LENGTH = 50, HEIGHT = 4),
            ob.unbreakable_walls(POS = vector(0, 2, -20.5), X_LENGTH = 50, Z_LENGTH = 1, HEIGHT = 4),
            ob.unbreakable_walls(POS = vector(0, 2, 20.5), X_LENGTH = 50, Z_LENGTH = 1, HEIGHT = 4),
            ob.unbreakable_walls(POS = vector(0, 4.5, 0), X_LENGTH = 50, Z_LENGTH = 50, HEIGHT = 1),
            ob.unbreakable_walls(POS = vector(0, -0.5, 0), X_LENGTH = 50, Z_LENGTH = 50, HEIGHT = 1)]
lights = [local_light(pos = (i*6, 4, j*6), color = color.gray(0.2)) for i in range(-3, 4) for j in range(-3, 4)]
light_bulbs = [sphere(pos = (i*6, 4, j*6), radius = 0.1, color = color.yellow, material = materials.glass) for i in range(-3, 4) for j in range(-3, 4)]

key_pressed = {"w":0, "a":0, "s":0, "d":0}

def keydown_handler(evt):
    global key_pressed, MYSELF
    k = evt.key
    if k == "escape":
        pass
    elif k == "r":
        pass
    elif k == "w" or k == "s" or k == "a" or k == "d":
        if k == "w":
            key_pressed["w"] = 1
            key_pressed["s"] = 0
        elif k == "s":
            key_pressed["s"] = 1
            key_pressed["w"] = 0
        elif k == "a":
            key_pressed["a"] = 1
            key_pressed["d"] = 0
        elif k == "d":
            key_pressed["d"] = 1
            key_pressed["a"] = 0
        tmp_dir = vector(0, 0, 0)
        if key_pressed["w"]:
            tmp_dir += vector(1, 0, 0)
        elif key_pressed["s"]:
            tmp_dir += vector(-1, 0, 0)
        if key_pressed["a"]:
            tmp_dir += vector(0, 0, -1)
        elif key_pressed["d"]:
            tmp_dir += vector(0, 0, 1)
        forward = vector(scene.forward.x, 0, scene.forward.z)
        tmp_dir = rotate(vector = forward, angle = diff_angle(vector(1, 0, 0), tmp_dir), axis = cross(vector(1, 0, 0), tmp_dir))
        MYSELF.set_moving_dir(tmp_dir)
        MYSELF.move(forward)
scene.bind("keydown", keydown_handler)

def keyup_handler(evt):
    global key_pressed
    k = evt.key
    if k == "w":
        if key_pressed["w"]:
            key_pressed["w"] = 0
    elif k == "s":
        if key_pressed["s"]:
            key_pressed["s"] = 0
    elif k == "a":
        if key_pressed["a"]:
            key_pressed["a"] = 0
    elif k == "d":
        if key_pressed["d"]:
            key_pressed["d"] = 0
scene.bind("keyup", keyup_handler)

def mouse_handler(evt):
    global bullets_list, scene
    b = evt.button
    if b == "left":
        bullets_list += MYSELF.weapon.fire(scene.mouse.ray)
scene.bind("click", mouse_handler)

MYSELF = pl.players(ID = 1, NAME = "SELF", POS = vector(0, 0, 0), AXIS = vector(0, 0, -1), WEAPON = "shotgun", dT = scene.dt)
MYSELF.body.head.visible = False
bullets_list = []
targets_list = []

while True:
    rate(1/scene.dt)

    scene.center = (MYSELF.body).frame_to_world(MYSELF.body.head.pos)
    MYSELF.set_vision_axis(scene.mouse.ray)

    if rd.random() < 0.005 and len(targets_list) < 10:
        targets_list.append(ob.targets(POS = vector(rd.random()*40-20, 2.5, rd.random()*40-20), RADIUS = 0.5, AXIS = vector(1, 0, 0)))

    for obj in scene.objects:
        if hasattr(obj, "v"):
            obj.pos += obj.v * scene.dt

    for bul in bullets_list:
        if bul.time_left <= 0:
            bul.hit()
            bul.set_invisible()
            try:
                del bullets_list[bullets_list.index(bul)]
            except:
                pass
        else:
            bul.time_left -= scene.dt
            for item in gameroom:
                tmp = bul.obj.pos - item.obj.pos 
                if (abs(tmp.x) <= (item.obj.length / 2) and
                    abs(tmp.y) <= (item.obj.height / 2) and
                    abs(tmp.z) <= (item.obj.width / 2)):
                    bul.hit()
                    try:
                        del bullets_list[bullets_list.index(bul)]
                    except:
                        pass
            for item in targets_list:
                tmp = bul.obj.pos - item.obj.pos 
                if mag(tmp) <= (item.obj.radius):
                    try:
                        del targets_list[targets_list.index(item)]
                    except:
                        pass
                    bul.hit()
                    try:
                        del bullets_list[bullets_list.index(bul)]
                    except:
                        pass
