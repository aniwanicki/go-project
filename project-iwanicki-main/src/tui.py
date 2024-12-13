import sys
#import time
from typing import Optional

import click
from colorama import Fore, Style
from fakes import GoStub, GoFake
from base import GoBase
from go import Go

#print(sys.argv)
#sidestr = sys.argv[1]
#BOARDSIZE = int(sidestr)
trygrid = []
#gotype = GoFake(BOARDSIZE,2, False)
#players = 2

#for _ in range(BOARDSIZE):
    #trygrid.append([None]*BOARDSIZE)



def print_board(grid: list[list[Optional[int]]]) -> None:
    """ Prints the board to the screen
    """
    nrows = len(grid)
    ncols = len(grid[0])
    colors = [Fore.BLACK, Fore.WHITE, Fore.BLUE, Fore.YELLOW, Fore.RED, Fore.GREEN, Fore.MAGENTA, Fore.CYAN, Fore.LIGHTBLUE_EX]

    for r in range(nrows):
        crow = ""
        for c in range(ncols):
            v = grid[r][c]
            if v is None:
                if c == 0:
                    if r ==0:
                        crow += Fore.BLACK + "┌"
                    elif r == nrows-1:
                        crow += Fore.BLACK + "└"
                    else:
                        crow += Fore.BLACK + "├"
                elif c == ncols - 1:
                    if r == 0:
                        crow += Fore.BLACK + "─┐"
                    elif r == nrows-1:
                        crow += Fore.BLACK + "─┘"
                    else:
                        crow += Fore.BLACK + "─┤"
                if r == 0 and (c!= 0 and c!= ncols -1):
                    crow += Fore.BLACK + "─┬"
                elif r == nrows-1 and (c!= 0 and c!= ncols -1):
                    crow += Fore.BLACK + "─┴"
                if r != 0 and r!= nrows-1 and c!= 0 and c!= ncols-1:
                    crow += Fore.BLACK + "─┼"
            elif v != 0 and c!= 0:
                color = colors[v-1]
                crow += Fore.BLACK + "-"
                crow += color + Style.BRIGHT + "●"
            elif v !=0 and c == 0:
                color = colors[v-1]
                crow += color + Style.BRIGHT + "●"

        print(crow)

@click.command("banner")
@click.option("-n", "--num-players", default = 2)
@click.option("-s", "--size", default = 19)
@click.option("--simple-ko/--super-ko", is_flag = True)
def cmd(num_players, size, simple_ko):
    super_ko = not simple_ko
    if super_ko:
        gotype = Go(size, num_players, True)
    if simple_ko or not super_ko:
        gotype = Go(size, num_players, False)
    print()
    print_board(gotype.grid)
    print()
    while not gotype.done:
        print()
        print(f"Player {gotype.turn}'s turn.")
        input_move = input("Please enter your move as x and y coordinates separated by a space; i.e: 2 4")
        if input_move != "":
            values = input_move.split(" ")
            x = values[0]
            y = values[1]
            piece = (int(x), int(y))
            potential_moves = gotype.available_moves
            #print(potential_moves, "potentials")
            if piece in potential_moves:
                try:
                    move_bool = gotype.legal_move(piece)
                    print(move_bool, piece)
                    if move_bool:
                        gotype.apply_move(piece)
                        #turn2 = gotype.turn
                        print_board(gotype.grid)
                    else:
                        print("invalid move, try again")

                except ValueError as ve:
                    print(ve)
        else:
            gotype.apply_move(None)
        print()
        if gotype.done:
            print("Game Over!")
            winner = gotype.outcome
            num_winners = len(winner)
            if num_winners == 1:
                winner_string = "Winner: Player {}".format(str(winner[0]))
                print(winner_string)
            else:
                winner_string = "Winners: Player {}".format(str(winner[0]))
                for i in range(num_winners-1):
                    winners_string = "{} and Player {}".format(winner_string, str(winner[i+1]))
                    winner_string = winners_string
                print(winner_string)


if __name__ == "__main__":
    cmd()
        
    
    
