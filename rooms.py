

class rooms(object):
    def __init__(self):
        self.start = False
        self.playernum = 0
        self.player_IDs = []
        self.player_socks = {}
        self.msg_queue = {}

    def join(self, PLAYER_ID, PLAYER_NAME, PLAYER_SOCK = None):
        self.playernum += 1
        self.player_IDs.append(PLAYER_ID)
        self.player_socks[PLAYER_ID] = PLAYER_SOCK
        self.msg_queue[PLAYER_ID] = Queue.Queue()

    def leave(self, PLAYER_ID):
        self.playernum -= 1
        del self.player_IDs[self.player_IDs.index(PLAYER_ID)]
        del self.player_socks[PLAYER_ID]
        del self.msg_queue[PLAYER_ID]
        return self.playernum

    def loop(self):
        self.start = True
        pass