from pelita.datamodel import stop
from pelita.player import AbstractPlayer, SimpleTeam

import networkx as nx

class BasePlayer(AbstractPlayer):

    def set_initial(self):
        univ = self.current_uni
        self.graph = nx.Graph()
        for pos, nbs in univ.free_positions():
            for n in nbs:
                self.graph.add_edge(pos, n)

        self.food = self.enemy_food
        self.food.sort(key=lambda x: x[1])
        if self.me.index < 2:
            self.food = self.food[::-1]

        self.curindex = 0
        self.chose_strategy()

    def chose_strategy(self):
        self.strategy = 'feed'

    def move_towards(self, target):
        path = nx.shortest_path(self.graph, self.current_pos, target)
        pos = path[1]
        pos2move = {v: k for k, v in self.legal_moves.items()}
        return pos2move[pos]

    def get_move(self):

        dangerous_enemy_pos = [bot.current_pos for bot in self.enemy_bots if bot.is_destroyer]

        if self.strategy == 'feed':
            if self.current_pos == self.food[self.curindex]:
                self.curindex +=1

            if self.curindex > len(self.food):
                self.curindex -=1
                nextpos = stop
            else:
                nextpos = self.move_towards(self.food[self.curindex])
        else:
            nextpos = stop

        #avoid enemies. this is just a quick hack and for now doesn't work properly anyway
        for pos in dangerous_enemy_pos:
            if nextpos == pos:
                for move in legal_moves:
                    if (move != nextpos) and (move != pos):
                        nextpos = move

        return nextpos

def factory():
    return SimpleTeam("The Base Players", BasePlayer(), BasePlayer())
