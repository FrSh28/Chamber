from visual import*
import players as pl
import objects as ob
import weapons as wp
import random as rd
import communicate_client as com_cli
#import practice_mode
import team_mode
import FFA_mode
import os, json

#建構基本環境
scene = display(x = 0, y= 0, width = 1200, height = 700, center = vector(0, 2, 0), background = color.black, title = "FPS", dt = 0.01, lights = [], range = 0.3, autoscale = False, userzoom = False)

chamber = [ob.unbreakable_walls(POS = vector(-20.5, 2, 0), X_LENGTH = 1, Z_LENGTH = 50, HEIGHT = 4),
           ob.unbreakable_walls(POS = vector(20.5, 2, 0), X_LENGTH = 1, Z_LENGTH = 50, HEIGHT = 4),
           ob.unbreakable_walls(POS = vector(0, 2, -20.5), X_LENGTH = 50, Z_LENGTH = 1, HEIGHT = 4),
           ob.unbreakable_walls(POS = vector(0, 2, 20.5), X_LENGTH = 50, Z_LENGTH = 1, HEIGHT = 4),
           ob.unbreakable_walls(POS = vector(0, 4.5, 0), X_LENGTH = 50, Z_LENGTH = 50, HEIGHT = 1),
           ob.unbreakable_walls(POS = vector(0, -0.5, 0), X_LENGTH = 50, Z_LENGTH = 50, HEIGHT = 1)]
lights = [local_light(pos = (i*6, 4, j*6), color = color.gray(0.2)) for i in range(-3, 4) for j in range(-3, 4)]
light_bulbs = [sphere(pos = (i*6, 4, j*6), radius = 0.1, color = color.yellow, material = materials.glass) for i in range(-3, 4) for j in range(-3, 4)]

#載入玩家資料
f_account = open("account.txt", "r")
user_account = json.loads(f_account.read())


#建立連線
if multiplayer:
    com_cli.connect()
    count = 0
    roomnum = keyboard_input(enter_roomnum)
    com_cli.send("join " + str(roomnum))
    while not (com_cli.receive() == "OK"):
        if count > 3:
            print "jion room faile"
            break
        com_cli.send("join " + str(roomnum))
        count += 1
    count = 0
    com_cli.send("id: " + user_account.id)
        count += 1
    while not (com_cli.receive() == "OK"):
        if count > 3:
            print "connection faile"
            break
        com_cli.send("id: " + user_account.id)
        count += 1
    
    


gamemode_list[gamemode]()


#temp = ?
if scene.mouse.events:
    mou = scene.mouse.getevent()
    if not(temp == None):
        if mou.click == "left" and (cur == None or temp > cur):
            if not(temp == 35):
                cur = temp
                for k in range(temp+1):
                    buttons[k].color = color.gray(0.4)
            callmess = texts[temp].text
            break

enter_password = frame(visible = False)
enter_password_background = label(frame = enter_password, text = "", border = 60, height = 40, pos = scene.center, background = color.gray(0.7), color = color.black, xoffset = 0, yoffset = 0, line = False, box = False)
enter_password_type = label(frame = enter_password, text = "", font = "monospace", height = 30, pos = scene.center, background = color.gray(0.2), color = color.gray(0.5), xoffset = 0, yoffset = -30, line = False, box = False)
def keyboard_input(TYPING_ZONE):
    while scene.kb.keys:
        scene.kb.getkey()
    text = ""
    while True:
        ev = scene.waitfor("keydown")
        if ev.key == "backspace":
            if len(text) > 0:
                text[-1] = ""
                TYPING_ZONE.text = text
        elif len(ev.key) == 1:
            text = text + str(ev.key)
            TYPING_ZONE.text = text
        elif ev.key == "\n":
            return text


#選擇遊戲模式
gamemode, multiplayer = choose_gamemode()
gamemode_list = {"practice":practice_mode.gameloop, "team":team_mode.gameloop, "FFA":FFA_mode.gameloop}

def choose_gamemode():
    gamemode_choice = [box(mode = "practice"), box(mode = "team"), box(mode = "FFA")] #省略GUI相關參數
    while True:
        evt = scene.waitfor("click")
        if evt.button == "left":
            obj = scene.mouse.pick
            try:
                gamemode_choice.index(obj)
                mode =  obj.mode
            except:
                pass
    for obj in gamemode_choice:
        obj.visible = False
        del gamemode_choice[gamemode_choice.index(obj)]

    if mode != "practice":
        return mode , True #multiplayer
    else:
        multiplayer_choice = [box(multi = True), box(multi = False)] #省略GUI相關參數
        while True:
            evt = scene.waitfor("click")
            if evt.button == "left":
                obj = scene.mouse.pick
                try:
                    multiplayer_choice.index(obj)
                    return mode, obj.multi
                except:
                    pass