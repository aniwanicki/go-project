"""
Bots for Go
"""
import sys
from typing import Optional
from fakes import GoStub, GoFake
from go import Go, Board
import click

#sidestr = sys.argv[1]
#num_games = int(sidestr)
@click.command("banner")
@click.option("-n", "--num-games", default = 20)
@click.option("-s", "--size", default = 6)
@click.option("-1", "--player1", default = True)
@click.option("-2", "--player2", default = True)
def cmd(num_games, size, player1, player2):
    bots: dict[str, BotPlayer]
    bots = {}
    go = Go(size, 2, False)
    if player1:
        #go = GoFake(size, num_players, True)
        bots["1"] = BotPlayer("random", go, "1")
        print("yes")
    elif not player1:
        bots["1"] = BotPlayer("smart", go, "1")
        print("no")
    if player2:
        print("yes2")
        bots["2"] = BotPlayer("random", go, "2")
    elif not player2:
        print("no2")
        bots["2"] = BotPlayer("smart", go, "2")

    play(num_games, bots)
####################
#gostub = GoStub(6,2)
#gofake = GoFake(9,2)
#gofake = Go(9,2)
import random
from base import GoBase, BoardGridType, ListMovesType
BoardGridType: list[list[Optional[int]]]

#
# BOTS
#

class RandomBot:
    """
    Simple Bot that just picks a move at random
    """

    gotype: Go
    #_color: 1
    #_opponent_color: 2

    def __init__(self, gotype: Go, color: int): 

        self.gotype = gotype
        self.color = color

    def suggest_move(self) -> tuple[int,int]:
        random_move: tuple[int,int]
        possible_move = self.gotype.available_moves
        corner = (0,0)
        #if corner in possible_move: #For GoFake
        #    possible_move.remove((0,0))
        random_move = random.choice(possible_move)
        return random_move

class SmartBot:
    "smart bot implementing simplified minimize to optimize chance of winning in next moves"
    gotype: Go
    color: 2

    def __init__(self, gotype: Go, color: int):
        self.gotype = gotype
        self.color = color
    
    def suggest_move(self) -> tuple[int,int]:
        """"Suggests a move"""
        best_list = []
        best_move = []
        available_M = self.gotype.available_moves
        #print(available_M, "available moves")

        #if available_M[0] == (0,0): #Needed for GoFake implementation, not Go
        #    del available_M[0]

        available_M.append(None) #for passing a move
        for t_move in available_M:
            if self.gotype.legal_move(t_move):
                new_gofake = self.gotype.simulate_move(t_move) #simulate taking M
                new_gomoves = new_gofake.available_moves #all available moves after M, = Next(M); that taken by player 1
                #if new_gomoves[0] == (0,0): #For GoFake
                #    del new_gomoves[0]
                new_gomoves.append(None)
                total = 0
                for nextmove in new_gomoves: #go through each move one by one
                    if new_gofake.legal_move(nextmove):
                        each_gofake = new_gofake.simulate_move(nextmove) #simulate next
                        test_grid = each_gofake.grid
                        for row in test_grid:
                            for col in row:
                                if col == 2:
                                    total = total + 1
                average_tot = total/len(new_gomoves)
                #print(average_tot, "average pieces from", t_move, "move")
                if len(best_list) == 0:
                    best_list.append(average_tot)
                    best_move.append(t_move)
                else:
                    if average_tot > best_list[0]:
                        best_list[0] = average_tot
                        best_move[0] = t_move
                    if average_tot == best_list[0]:
                        best_move.append(t_move)
        
        random_best = random.choice(best_move)
        #print(random_best, "CHOSEN MOVE")
        return random_best #set the move that gives the maximum pieces 2 moves away as final M
    
class BotPlayer:

    name: str
    bot: RandomBot | SmartBot
    color: int
    wins: int
    go: Go
    def __init__(self, name: str, go: Go, color: str): #, opponent_color: int):
        self.name = name
        self.color = color
        #self.go = go
        self.go = go
        self.wins = 0
    
    def connect_suggested_move(self, go: Go) -> tuple[int,int]:
        self.go = go
        if self.name == "random":
            bot = RandomBot(self.go, int(self.color))
            sugg_move = bot.suggest_move()
            return sugg_move
        else:
            if self.name == "smart":
                bot = SmartBot(self.go, int(self.color))
                sugg_move = bot.suggest_move()
                return sugg_move


def simulate(gof: Go, num_games: int, bots: dict[str, BotPlayer]) -> None:
    n = num_games
    tie_count = 0
    avg_moves = []
    for i in range(n):
        print(i)
        #gof = GoFake(6,2,False)
        gof = Go(6,2,False)
        turn = "1"
        move_count = 0

        while not gof.done:
            player = bots[turn]
            move = player.connect_suggested_move(gof)
            #print(player, "player", move, "move")
            gof.apply_move(move)

            #int_scores = gof.scores()
            #b1 = int_scores[1]
            #b2 = int_scores[2]
            #print(b1, "bot 1 scores", b2, "bot2 scores")
            move_count += 1
            if move_count < 256:
                if turn == "1":
                    turn = "2"
                elif turn == "2":
                    turn = "1"
            else:
                break
        avg_moves.append(move_count)
        if not gof.done:
            final_scores = gof.scores()
            bot1 = final_scores[1]
            print(bot1, "bot1 final")
            bot2 = final_scores[2]
            print(bot2, "bot2final")
            if bot1> bot2:
                bots["1"].wins += 1
            elif bot2 > bot1:
                bots["2"].wins += 1
            else:
                tie_count += 1
        else:
            winner_list = gof.outcome
            if len(winner_list) == 1:
                winner = winner_list[0]
                #print(winner, "WINNER")
                bots[str(winner)].wins = bots[str(winner)].wins + 1
            else:
                tie_count = tie_count + 1

    total_moves = sum(avg_moves)
    avg_move = total_moves/ len(avg_moves)
    tie_perc = (tie_count / n)
    tie_result = "Ties: {:%}".format(tie_perc)
    bot1_win_perc = (bots["1"].wins / n)
    bot2_win_perc = (bots["2"].wins / n)
    bot1_result = "Player 1 wins: {:%}".format(bot1_win_perc)
    bot2_result = "Player 2 wins: {:%}".format(bot2_win_perc)
    avg_num_move = "Average Moves: {}".format(avg_move)

    print(bot1_result)
    print(bot2_result)
    print(tie_result)
    print(avg_num_move)



def play(n: int, bots:dict[str,BotPlayer]):
    num_games = n
    #gof = GoFake(6,2,False)
    gof = Go(6,2,False)
    #bots: dict[str, BotPlayer]
    #bots = {}
    #bots["1"] = BotPlayer("random", gof, "1")
    #bots["2"] = BotPlayer("smart", gof, "2")
    simulate(gof, num_games, bots)

#play(num_games)

if __name__ == "__main__":
    cmd()
        

#add cmd and test smart bot line by line
        




            
                
