from pelita import datamodel
from pelita.graph import AdjacencyList, NoPathException, diff_pos as diffPos
from pelita.player import AbstractPlayer, SimpleTeam
import numpy as np
import ipdb

class EatingPlayerUpper(AbstractPlayer):
    
    def set_initial(self):
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.tolerance = 5
        self.range = range(7,15)
     
    def gotoPos(self,aim):
        return(self.adjacency.a_star(self.current_pos,aim))[-1]

    def choose_strategy(self):
        if self.me.is_harvester:
            minDist2Bot = self.chooseClosestEnemy()
            strategy = 'run' if minDist2Bot[0] <= self.tolerance else 'eat'
        else:
            strategy = 'eat'
        return(strategy)
        
    def chooseClosestEnemy(self):
        dist2bot = np.array([len(self.adjacency.a_star(self.current_pos,j.current_pos)) if j.is_destroyer else 1000 for j in self.enemy_bots])
        minDist  = dist2bot.min()
        minPos = [x.current_pos for x in self.enemy_bots][dist2bot.argmin()]
        return(minDist,minPos)

    def eatMaxSafety(self,enemy_pos):
        next_step = np.zeros(len(self.enemy_food))
        for i,j in enumerate(self.enemy_food):
            next_step[i] = len(self.adjacency.a_star(self.adjacency.a_star(self.current_pos,j)[-1],enemy_pos))
        max_safe  = next_step.max()
        max_pos   = self.enemy_food[next_step.argmax()]
        return(max_safe, max_pos)
    
    def get_move(self):
        if len(self.enemy_food) > 0:
            strategy = self.choose_strategy()
            nextPos = self.chooseNextPos(strategy)
            move  = diffPos(self.current_pos,nextPos)
            if not move in self.legal_moves.keys():
                move = self.rnd.choice(list(self.legal_moves.keys()))
        else:
            move = (0,0)
        return(move)        

    def chooseNextPos(self,strategy):
        if strategy == 'eat':
            minFoodDist, aim = self.chooseClosestFood()
            nextPos = self.gotoPos(aim)
        elif strategy == 'run':
            dummy, aim = self.chooseClosestEnemy()
            dummy2,aim2    = self.eatMaxSafety(aim)
            nextPos = self.gotoPos(aim2)
        return(nextPos)

    def chooseClosestFood(self):
        dist2food  = np.array([len(self.adjacency.a_star(self.current_pos,(x,y))) if y in self.range else 1000 for x,y in self.enemy_food]) 
        # for i,j in enumerate(self.enemy_food):
        #    dist2food[i] = len(self.adjacency.a_star(self.current_pos,j)) if j[2] in self.range else 1000 
        minDist = dist2food.min()
        minPos  = self.enemy_food[dist2food.argmin()]
        return(minDist,minPos)

class EatingPlayerLower(AbstractPlayer):
    
    def set_initial(self):
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.tolerance = 5
        self.range = range(1,9)
     
    def gotoPos(self,aim):
        return(self.adjacency.a_star(self.current_pos,aim))[-1]

    def choose_strategy(self):
        if self.me.is_harvester:
            minDist2Bot = self.chooseClosestEnemy()
            strategy = 'run' if minDist2Bot[0] <= self.tolerance else 'eat'
        else:
            strategy = 'eat'
        return(strategy)
        
    def chooseClosestEnemy(self):
        dist2bot = np.array([len(self.adjacency.a_star(self.current_pos,j.current_pos)) if j.is_destroyer else 1000 for j in self.enemy_bots])
        minDist  = dist2bot.min()
        minPos = [x.current_pos for x in self.enemy_bots][dist2bot.argmin()]
        return(minDist,minPos)

    def eatMaxSafety(self,enemy_pos):
        next_step = np.zeros(len(self.enemy_food))
        for i,j in enumerate(self.enemy_food):            
            next_step[i] = len(self.adjacency.a_star(self.adjacency.a_star(self.current_pos,j)[-1],enemy_pos)) 
        max_safe  = next_step.max() 
        max_pos   = self.enemy_food[next_step.argmax()]
        return(max_safe, max_pos)
     
    def get_move(self):
        strategy = self.choose_strategy()
        nextPos = self.chooseNextPos(strategy)
        move  = diffPos(self.current_pos,nextPos)
        if not move in self.legal_moves.keys():
            move = self.rnd.choice(list(self.legal_moves.keys()))  
        return(move)        
 
    def chooseClosestFood(self):
        dist2food  = np.array([len(self.adjacency.a_star(self.current_pos,(x,y))) if y in self.range else 1000 for x,y in self.enemy_food]) 
        minDist = dist2food.min()
        minPos  = self.enemy_food[dist2food.argmin()]
        return(minDist,minPos)

    def chooseNextPos(self,strategy):
        if strategy == 'eat':
            minFoodDist, posMinFood = self.chooseClosestFood()
            aim = posMinFood
            nextPos = self.gotoPos(aim)
        elif strategy == 'run':
            dummy, aim   = self.chooseClosestEnemy()
            dummy2, aim2 = self.eatMaxSafety(aim)
            nextPos = self.gotoPos(aim2)
        return(nextPos)


def factory():
    return(SimpleTeam("Upper Lower Split",EatingPlayerUpper(),EatingPlayerLower()))

