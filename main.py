from visual import*
import players as pl
import objects as ob
import weapons as wp
import random as rd
import account
import communicate_client
import practice_mode
import team_mode
import FFA_mode
import os

scene = display(x = 0, y = 0, width = 1200, height = 700, center = vector(0, 7, 2), background = color.black, title = "FPS", dt = 0.01, lights = [], range = 2.5, autoscale = False)#, userzoom = False)
shade = cylinder(pos = vector(0, 5.5, 0), radius = 5, length = 4, axis = vector(0, 1, 0), color = color.black)
scene.forward = vector(0, -0.3, -1)
lights = [local_light(pos = vector(0, 8, 0), color = color.gray(0.5))]

gameroom = [ob.unbreakable_walls(POS = vector(-20.5, 2, 0), X_LENGTH = 1, Z_LENGTH = 50, HEIGHT = 4),
            ob.unbreakable_walls(POS = vector(20.5, 2, 0), X_LENGTH = 1, Z_LENGTH = 50, HEIGHT = 4),
            ob.unbreakable_walls(POS = vector(0, 2, -20.5), X_LENGTH = 50, Z_LENGTH = 1, HEIGHT = 4),
            ob.unbreakable_walls(POS = vector(0, 2, 20.5), X_LENGTH = 50, Z_LENGTH = 1, HEIGHT = 4),
            ob.unbreakable_walls(POS = vector(0, 4.5, 0), X_LENGTH = 50, Z_LENGTH = 50, HEIGHT = 1),
            ob.unbreakable_walls(POS = vector(0, -0.5, 0), X_LENGTH = 50, Z_LENGTH = 50, HEIGHT = 1)]
lights += [local_light(pos = vector(i*6, 4, j*6), color = color.gray(0.2)) for i in range(-3, 4) for j in range(-3, 4)]
light_bulbs = [sphere(pos = vector(i*6, 4, j*6), radius = 0.1, color = color.yellow, material = materials.glass) for i in range(-3, 4) for j in range(-3, 4)]


account_info = account.account()
player_ID = account_info.ID
player_name = account_info.name
print "Hello! " + player_name + "(" + str(player_ID) + ")\n"
SELF = pl.players(ID = player_ID, NAME = player_name, SCENE = scene, POS = vector(0, 6, 0), AXIS = vector(0, 0, 1), WEAPON = "shotgun", dT = scene.dt)
SELF_pos = vector(rd.random()*20-10, 0, rd.random()*20-10)

multiplayer = raw_input("multiplayer?(y/n)")
while not (multiplayer == "y" or multiplayer == "Y" or multiplayer == "n" or multiplayer == "N"):
    multiplayer = raw_input("multiplayer?(y/n)")
if multiplayer == "n" or multiplayer == "N":
    multiplayer = False
    gamemode = "practice"

elif multiplayer == "y" or multiplayer == "Y":
    multiplayer = True

    msg_queue = communicate_client.connect()
    msg = "p " + str(player_ID) + player_name
    msg_queue.join()
    msg_queue.put(msg)

    new_room = raw_input("create new room?(y/n)")
    while not (new_room == "y" or new_room == "Y" or new_room == "n" or new_room == "N"):
        new_room = raw_input("multiplayer?(y/n)")
    if new_room == "n" or new_room == "N":
        room_ID = raw_input("roomID : ")
        msg = "join " + room_ID
        msg_queue.join()
        msg_queue.put(msg)
        msg_queue.join()
        msg = msg_queue.get()
        msg = msg.split(" ")
        if msg[0] == "accepted":
            gamemode = msg[1]
            msg_queue.task_done()
        else:
            print "Join gameroom %d failed." % (room_ID)
            communicate_client.disconnect()

    elif new_room == "y" or new_room == "Y":
        gamemode = raw_input("gamemode : ")
        while not (gamemode == "practice" or gamemode == "FFA" or gamemode == "team"):
            gamemode = raw_input("gamemode : ")
        msg = "create " + gamemode
        msg_queue.join()
        msg_queue.put(msg)
        msg_queue.join()
        msg = msg_queue.get()
        msg = msg.split(" ")
        if msg[0] == "accepted":
            room_ID = msg[1]
            msg_queue.task_done()
        else:
            print "Create gameroom failed.\n"
            communicate_client.disconnect()
    print gamemode, room_ID

scene.range = 0.3

if gamemode == "practice":
    if multiplayer:
        gaming = practice_mode.practice_mode(scene, multiplayer, msg_queue)
    else:
        gaming = practice_mode.practice_mode(scene, multiplayer)
elif gamemode == "FFA":
    gaming = FFA_mode.FFA_mode(scene, multiplayer, msg_queue)
elif gamemode == "team":
    gaming = team_mode.team_mode(scene, multiplayer, msg_queue)

gaming.join(SELF, True)
if multiplayer:
    msg_queue.join()
    msg = msg_queue.get()
    msg = msg.split(" ")
    if msg[0] == "players":
        msg_queue.task_done()
        while True:
            msg_queue.join()
            msg = msg_queue.get()
            msg = msg.split(" ")
            if msg[0] == "p":
                tmp_player = pl.players(ID = eval(msg[1]), NAME = eval(msg[2]), SCENE = scene, POS = vector(eval(msg[3]), eval(msg[4]), eval(msg[5])), AXIS = vector(eval(msg[6]), eval(msg[7]), eval(msg[8])), WEAPON = msg[9], dT = scene.dt)
                gaming.join(tmp_player)
                msg_queue.task_done()
                msg = "next"
                msg_queue.join()
                msg_queue.put(msg)
            elif msg[0] == "end":
                msg_queue.task_done()
                msg = "p %s %s %s %s %s %s %s %s %s" % (str(SELF.ID), str(SELF.name), str(SELF_pos.x), str(SELF_pos.y), str(SELF_pos.z), str(SELF.axis.x), str(SELF.axis.y), str(SELF.axis.z), str(SELF.weapon_name))
                msg_queue.join()
                msg_queue.put(msg)
                break
    else:
        print "Getting players failed."
    while scene.kb.keys:
        scene.kb.getkey()
    while True:
        rate(1/scene.dt)
        if scene.kb.keys:
            k = scene.kb.getkeys()
            if k == "s":
                msg = "start"
                msg_queue.join()
                msg_queue.put(msg)
        msg_queue.join()
        msg = msg_queue.get()
        msg = msg.split(" ")
        if msg[0] == "start":
            msg_queue.task_done()
            break

SELF.pos = SELF_pos
SELF.body.pos = SELF_pos
SELF.body.head.visible = False
gaming.loop()

results = gaming.get_result()

account_info.update_exp(results["exp"])
account_info.save_account_info()

os.system("pause")

'''key_pressed = {"w":0, "a":0, "s":0, "d":0, "i":0, "k":0, "j":0, "l":0}

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
        key_pressed["w"] = 0
    elif k == "s":
        key_pressed["s"] = 0
    elif k == "a":
        key_pressed["a"] = 0
    elif k == "d":
        key_pressed["d"] = 0
scene.bind("keyup", keyup_handler)


def keydown_handler(evt):
    global key_pressed, OTHER
    k = evt.key
    if k == "escape":
        pass
    elif k == "r":
        pass
    elif k == "i" or k == "k" or k == "j" or k == "l":
        if k == "i":
            key_pressed["i"] = 1
            key_pressed["k"] = 0
        elif k == "k":
            key_pressed["k"] = 1
            key_pressed["i"] = 0
        elif k == "j":
            key_pressed["j"] = 1
            key_pressed["l"] = 0
        elif k == "l":
            key_pressed["l"] = 1
            key_pressed["j"] = 0
        tmp_dir = vector(0, 0, 0)
        if key_pressed["i"]:
            tmp_dir += vector(1, 0, 0)
        elif key_pressed["k"]:
            tmp_dir += vector(-1, 0, 0)
        if key_pressed["j"]:
            tmp_dir += vector(0, 0, -1)
        elif key_pressed["l"]:
            tmp_dir += vector(0, 0, 1)
        forward = vector(scene.forward.x, 0, scene.forward.z)
        tmp_dir = rotate(vector = forward, angle = diff_angle(vector(1, 0, 0), tmp_dir), axis = cross(vector(1, 0, 0), tmp_dir))
        OTHER.set_moving_dir(tmp_dir)
        OTHER.move(forward)
scene.bind("keydown", keydown_handler)

def keyup_handler(evt):
    global key_pressed
    k = evt.key
    if k == "i":
        key_pressed["i"] = 0
    elif k == "k":
        key_pressed["k"] = 0
    elif k == "j":
        key_pressed["j"] = 0
    elif k == "l":
        key_pressed["l"] = 0
scene.bind("keyup", keyup_handler)


def mouse_handler(evt):
    global bullets_list, scene
    b = evt.button
    if b == "left":
        bullets_list += MYSELF.weapon.fire(scene.mouse.ray)
scene.bind("click", mouse_handler)'''