import os
import sys 
import pygame
import numpy as np
import click
from typing import Union
from fakes import GoStub, GoFake, BoardGridType
from base import GoBase
from go import Go
from bot import SmartBot



#board_size = sys.argv[1]
#size = int(board_size)
#gogo = GoFake(size, 2, False)
#import click
#screen = pygame.display.set_mode((1280,720))
#clock = pygame.time.Clock()
#running = True
#dt = 0
@click.command("banner")
@click.option("-n", "--num-players", default = 2)
@click.option("-s", "--size", default = 19)
@click.option("--simple-ko/--super-ko", is_flag = True)
def cmd(num_players, size, simple_ko):
    super_ko = not simple_ko
    if super_ko:
        #go = GoFake(size, num_players, True)
        go = Go(size, num_players, True)
    if simple_ko or not super_ko:
        #go = GoFake(size, num_players, False)
        go = Go(size, num_players, False)
    height = 600
    border = 5
    input_go = GUIGeneralGo(go, height, border)
    play_go(go)

class GUIGeneralGo:
    grid: BoardGridType
    def __init__(self, go: Go|GoFake, height: int = 600, border: int = 5):
        self.height = height
        self.go = go
        self.border = border
        self.surface = pygame.display.set_mode((self.height + self.border,self.height+self.border))
        ###### add in variable u dont have
        self.gridd: BoardGridType
        self.gridd = self.go.grid
        self.piece_colors: dict[int, tuple[int,int,int]]
        self.piece_colors = {}
        self.players = go.num_players

        self.piece_colors[1] = (0,0,0) #117, 2, 2
        self.piece_colors[2] = (255, 255, 255) #224, 114, 210
        if self.players > 2:
            self.piece_colors[3] = (255, 51, 153) 
        if self.players > 3:
            self.piece_colors[4] = (51, 135, 255)
        if self.players > 4:
            self.piece_colors[5] = (153, 51, 255)
        if self.players > 5:
            self.piece_colors[6] = (51, 51, 255)
        if self.players > 6:
            self.piece_colors[7] = (255, 51, 255)
        if self.players > 7:
            self.piece_colors[8] = (255, 153, 51)
        if self.players > 8:
            self.piece_colors[9] = (255, 255, 51)

        self.side = go.size
        self.rh = (self.height - 200) // self.side
        self.cw = (self.height - 200) // self.side
        self.rect_list: list[list[pygame.Rect]]
        self.rect_list = []
        self.inner_rect_list: list[pygame.Rect]
        self.inner_rect_list = []
        self.reccd = False

        for row in range(self.side):
            for col in range(self.side):
                r = (row * self.rh) + (self.border) + 1
                c = (col * self.cw) + (self.border) + 1
                new = pygame.Rect(r,c, self.cw, self.rh)
                self.inner_rect_list.append(new)

            self.rect_list.append(self.inner_rect_list)
            self.inner_rect_list = []
        self.play_gui = False
        self.start = False

        self.music = False #music not started


        
    
    def draw_board(self) -> None:
        """ Draws the current state of the board in the window to initialize

        Args:
            surface: Pygame surface to draw the board on
            board: The board to draw

        Returns: None

        """
        full_width, full_height = self.surface.get_size() #610x610, border = 5
        self.surface.fill((195, 217, 247)) #background blue color
        board_width = full_width - 200 - self.border
        board_height = full_height - 200 - self.border
        # Compute the row height and column width
        rh = board_height // self.side #600
        cw = board_width // self.side

        # Draw the borders around each cell
        for row in range(self.side-1):
            for col in range(self.side-1):
                left = col*rh + self.border + rh//2
                top = row*cw  + self.border + cw//2
                rect = (left, top, cw, rh)
                pygame.draw.rect(self.surface, color=(35, 35, 48),
                             rect=rect, width=2) #width is width of inner grid
                outer_rect = (self.border,self.border,400-4,400-4)
                pygame.draw.rect(self.surface, color = (35,35,48), rect = outer_rect, width=4)
                board_boundary = (self.border+ rh//2 -2, self.border + rh//2 -2, rh*(self.side-1), rh*(self.side-1))
                pygame.draw.rect(self.surface, color = (35,35,48), rect = board_boundary, width = 2)
        # Draw the Turn Counter
        turn_left = board_width + 2*self.border +10
        turn_top = self.border
        turn_width = 180
        turn_height = 180
        turn_rect =  (turn_left, turn_top, turn_width, turn_height)
        pygame.draw.rect(self.surface, color= (255, 250, 250), rect=turn_rect)
        turn_text = pygame.font.SysFont("freesansbold.ttf", 40).render("Player Turn", True, (0,0,0))
        self.surface.blit(turn_text, (turn_left+self.border, turn_top+self.border))
        pygame.draw.rect(self.surface, color= (35,35,48), rect=turn_rect, width=4)
        pl = self.go.turn
        pygame.draw.circle(self.surface, color=self.piece_colors[pl], center=(turn_left + turn_width // 2, turn_top + turn_height//2 + 2*self.border), radius = 50)

        #pass button
        #pass_height = (self.side//2)*rh + (2*self.border)
        self.pass_rect = pygame.Rect(turn_left, turn_height+(2*self.border), turn_width, 80) ### edit this
        pygame.draw.rect(self.surface, color = (255,250,250), rect = self.pass_rect)
        pygame.draw.rect(self.surface, color = (35,35,48), rect = self.pass_rect, width = 4)
        pass_text = pygame.font.SysFont("freesansbold.ttf", 25).render("Press to Pass Turn", True, (0,0,0))
        self.surface.blit(pass_text, (turn_left+4, turn_height+(2*self.border)+4))
        

    
    def draw_move(self) -> None:
        """ Draws the current state of the board in the window

        Args:
            surface: Pygame surface to draw the board on
            board: The board to draw

        Returns: None

        """

        ### draw board grid
        full_width, full_height = self.surface.get_size() #610x610, border = 5
        self.surface.fill((195, 217, 247)) #background blue color

        if not self.start:
            go_text = pygame.font.SysFont("freesansbold.ttf", 100).render("Go", True, (0,0,0))
            self.surface.blit(go_text, (250, 100))
            start_string = "Press to Start"
            self.start_text = pygame.font.SysFont("freesansbold.ttf", 50).render(start_string, True, (0,0,0))
            self.start_rect = pygame.Rect(175, 275, 275, 85)
            pygame.draw.rect(self.surface, color = (255,250,250), rect = self.start_rect)
            pygame.draw.rect(self.surface, color= (35,35,48), rect=self.start_rect, width=4)
            self.surface.blit(self.start_text, (200,300))
        elif self.start:

            
            board_width = full_width - 200 - self.border
            board_height = full_height - 200 - self.border
            # Compute the row height and column width
            rh = board_height // self.side #600
            cw = board_width // self.side
            #width, height = self.surface.get_size() #610x610, border = 5
        
            #draw whose turn it is
            turn_left = board_width + 2*self.border + 10
            turn_top = self.border
            turn_width = 180
            turn_height = 180
        
            #for player turn image
            turn_rect =  (turn_left, turn_top, turn_width, turn_height)
            pygame.draw.rect(self.surface, color= (255, 250, 250), rect=turn_rect)
            turn_text = pygame.font.SysFont("freesansbold.ttf", 40).render("Player Turn", True, (0,0,0))
            self.surface.blit(turn_text, (turn_left+self.border + 10, turn_top+self.border))
            pygame.draw.rect(self.surface, color= (35,35,48), rect=turn_rect, width=4)
            pl = self.go.turn
            color=self.piece_colors[pl]
            center=(turn_left + turn_width // 2, turn_top+ turn_height//2 + 10)
            pygame.draw.circle(self.surface, color, center, radius = 50)
            pygame.draw.circle(self.surface, color=(35,35,48), center=center, radius = 50, width = 4)
        
            #for pass rect button
            pass_height = (self.side//2) * rh + (2*self.border)
            self.pass_rect = pygame.Rect(turn_left, turn_height+(2*self.border), turn_width, 80)
            pygame.draw.rect(self.surface, color = (255,250,250), rect = self.pass_rect)
            pygame.draw.rect(self.surface, color = (35,35,48), rect = self.pass_rect, width=4)
            pass_text = pygame.font.SysFont("freesansbold.ttf", 25).render("Press to Pass Turn", True, (0,0,0))
            self.surface.blit(pass_text, (self.pass_rect.centerx - 75, self.pass_rect.centery-10))
        
            # for scores
            score_dict = self.go.scores()
            score_list = []
            num_players = len(score_dict)
            player: int
            for player in score_dict:
                if len(score_dict) == 2:
                    player_width = 120
                    player_top = self.height - 200 + 20
                    player_left = self.border+((player-1)*(player_width+50))
                    player_rect = pygame.Rect(player_left,player_top, player_width, player_width)
                    pygame.draw.rect(self.surface, color = (255,250,250), rect = player_rect)
                    pygame.draw.rect(self.surface, color = (35,35,48), rect = player_rect, width = 4)
                    player_string = "Player {}".format(str(player))
                    player_text = pygame.font.SysFont("freesansbold.ttf", 20).render(player_string, True, (0,0,0))
                    score_string = "Score: {}".format(str(score_dict[player]))
                    score_text = pygame.font.SysFont("freesansbold.ttf", 20).render(score_string, True, (0,0,0))
                    self.surface.blit(player_text, (player_left + 40, player_top + 10))
                    self.surface.blit(score_text, (player_left + 40, player_top + 100))
                    pygame.draw.circle(self.surface, color=self.piece_colors[player], center= player_rect.center, radius = 20)
                    pygame.draw.circle(self.surface, color=(35,35,48), center=player_rect.center, radius = 20, width = 4)
                if num_players > 2 and num_players < 5:
                    player_width = (board_width - ((num_players-1)*10)) / num_players
                    player_top = self.height - 200 + 20
                    player_left = self.border+((player-1)*(player_width)+((player-1)*(10)))
                    player_rect = pygame.Rect(player_left,player_top, player_width, player_width)
                    pygame.draw.rect(self.surface, color = (255,250,250), rect = player_rect)
                    pygame.draw.rect(self.surface, color = (35,35,48), rect = player_rect, width = 4)
                    player_string = "Player {}".format(str(player))
                    player_text = pygame.font.SysFont("freesansbold.ttf", 20).render(player_string, True, (0,0,0))
                    score_string = "Score: {}".format(str(score_dict[player]))
                    score_text = pygame.font.SysFont("freesansbold.ttf", 20).render(score_string, True, (0,0,0))
                    self.surface.blit(player_text, (player_left + player_width//2 - 25, player_top + 15))
                    self.surface.blit(score_text, (player_left + player_width//2 -25, player_top + player_width//2+30))
                    pygame.draw.circle(self.surface, color=self.piece_colors[player], center= player_rect.center, radius = 20)
                    pygame.draw.circle(self.surface, color=(35,35,48), center=player_rect.center, radius = 20, width = 4)
                elif num_players > 2 and num_players < 10:
                    if player <= 4:
                        player_width = ((board_width - (40)) // 5)
                        player_top = self.height - 200 + 20
                        player_left = self.border+((player-1)*(player_width)+((player-1)*(10)))
                        player_rect = pygame.Rect(player_left,player_top, player_width, player_width)
                        pygame.draw.rect(self.surface, color = (255,250,250), rect = player_rect)
                        pygame.draw.rect(self.surface, color = (35,35,48), rect = player_rect, width = 4)
                        player_string = "Player {}".format(str(player))
                        player_text = pygame.font.SysFont("freesansbold.ttf", 20).render(player_string, True, (0,0,0))
                        score_string = "Score: {}".format(str(score_dict[player]))
                        score_text = pygame.font.SysFont("freesansbold.ttf", 20).render(score_string, True, (0,0,0))
                        self.surface.blit(player_text, (player_left + player_width//2 - 25, player_top + 5))
                        self.surface.blit(score_text, (player_left + player_width//2 -25, player_top + player_width//2+20))
                        pygame.draw.circle(self.surface, color=self.piece_colors[player], center= player_rect.center, radius = 15)
                        pygame.draw.circle(self.surface, color=(35,35,48), center=player_rect.center, radius = 15, width = 4)
                    if player > 4:
                        row2 = player-5
                        player_width = (board_width - (40)) // (5)
                        player_top = self.height - 10 - player_width 
                        player_left = self.border+((row2)*(player_width)+((row2)*(10)))
                        player_rect = pygame.Rect(player_left,player_top, player_width, player_width)
                        pygame.draw.rect(self.surface, color = (255,250,250), rect = player_rect)
                        pygame.draw.rect(self.surface, color = (35,35,48), rect = player_rect, width = 4)
                        player_string = "Player {}".format(str(player))
                        player_text = pygame.font.SysFont("freesansbold.ttf", 20).render(player_string, True, (0,0,0))
                        score_string = "Score: {}".format(str(score_dict[player]))
                        score_text = pygame.font.SysFont("freesansbold.ttf", 20).render(score_string, True, (0,0,0))
                        self.surface.blit(player_text, (player_left + player_width//2 - 25, player_top + 5))
                        self.surface.blit(score_text, (player_left + player_width//2 -25, player_top + player_width//2+20))
                        pygame.draw.circle(self.surface, color=self.piece_colors[player], center= player_rect.center, radius = 15)
                        pygame.draw.circle(self.surface, color=(35,35,48), center=player_rect.center, radius = 15, width = 4)

            
            #FOR SUGGESTIONS

            self.suggest_rect = pygame.Rect(turn_left, turn_height+(2*self.border) + 85, turn_width, 130)
            pygame.draw.rect(self.surface, color = (255,250,250), rect = self.suggest_rect)
            pygame.draw.rect(self.surface, color = (35,35,48), rect = self.suggest_rect, width = 4)
            suggest_string = "Suggest Move?"
            suggest_text = pygame.font.SysFont("freesansbold.ttf", 25).render(suggest_string, True, (0,0,0))
            self.bot_rect = pygame.Rect(turn_left+15, turn_height+(2*self.border) + 120, turn_width-30, 30)
            pygame.draw.rect(self.surface, color = (35,35,48), rect = self.bot_rect, width = 4)
            bot_string = "BOT RECOMMENDATION"
            bot_text = pygame.font.SysFont("freesansbold.ttf", 15).render(bot_string, True, (0,0,0))
            self.surface.blit(suggest_text, (self.suggest_rect.centerx - 60, self.suggest_rect.centery-55))
            self.surface.blit(bot_text, (self.bot_rect.centerx-60, self.bot_rect.centery))
            if self.reccd:
                self.surface.blit(self.move_text, (self.bot_rect.centerx-40, self.bot_rect.centery+20))

            
        
            # Draw the borders around each cell
            current_grid = self.go.grid
            for row in range(self.side-1):
                for col in range(self.side-1):
                    left = col*rh + self.border + rh//2
                    top = row*cw  + self.border + cw//2
                    rect = (left, top, cw, rh)
                    pygame.draw.rect(self.surface, color=(35, 35, 48),
                             rect=rect, width=2) #width is width of inner grid
                    outer_rect = (self.border,self.border,400,400)
                    pygame.draw.rect(self.surface, color=(35,35,48), rect=outer_rect, width=4)
                    board_boundary = (self.border+ rh//2 +2, self.border + rh//2+2, rh*(self.side-1), rh*(self.side-1))
                    pygame.draw.rect(self.surface, color = (35,35,48), rect = board_boundary, width = 2)

            for row in range(self.side):
                for col in range(self.side):
                    if current_grid[row][col] is not None:
                        #print("row", row, "col,", col)
                        left2 = ((row*rh) + self.border) + (rh // 2) + 1
                        right2 = ((col*rh) + self.border) + (rh // 2) + 1
                        center2 = (right2,left2)
                        radius2 = (rh // 2) - 2
                        turn = current_grid[row][col]
                        piece_color = self.piece_colors[turn]
                        pygame.draw.circle(self.surface, piece_color,
                                        center=center2, radius=radius2)
                        pygame.draw.circle(self.surface, piece_color,
                                        center=center2, radius=radius2, width=2)
            # for winner screen
            if self.go.done:
                self.play_gui = False
                self.winner_screen()

    def suggest_move(self):
        self.reccd = True
        helper = SmartBot(self.go, self.go.turn)
        suggested_move = helper.suggest_move()
        print(suggested_move)
        move_string = "{}".format(suggested_move)
        self.move_text = pygame.font.SysFont("freesansbold.ttf", 40).render(move_string, True, (0,0,0))
        #self.surface.blit(self.move_text, (self.suggest_rect.centerx - 60, self.suggest_rect.centery-75))


    
    def valid_move(self,coord: tuple[int,int]):
        for row in range(self.side):
            for col in range(self.side):
                rec = self.rect_list[row][col]
                if rec.collidepoint(coord):
                    trymove = (col,row)
                    if trymove in self.go.available_moves:

                        move_bool = self.go.legal_move(trymove)
                        if move_bool:
                            pygame.draw.circle(self.surface, (0, 250,0), center = rec.center, radius = (self.rh //2) -2)
                        elif not move_bool:
                            pygame.draw.circle(self.surface, (250,0,0), center = rec.center, radius = (self.rh //2) -2)
                    


    def winner_screen(self):
        if self.go.done:
            winner = self.go.outcome
            num_winners = len(winner)
            one_font = 100
            if num_winners == 1:
                winner_string = "Winner: Player {}".format(str(winner[0]))
                winner_text = pygame.font.SysFont("freesansbold.ttf", one_font).render(winner_string, True, (0,0,0))
            else:
                mult_font = one_font//num_winners
                winner_string = "Winners: Player {}".format(str(winner[0]))
                for i in range(num_winners-1):
                    winners_string = "{} and Player {}".format(winner_string, str(winner[i+1]))
                    winner_string = winners_string
                winner_text = pygame.font.SysFont("freesansbold.ttf", mult_font).render(winner_string, True, (0,0,0))
                    

            done_height = self.height- (2*self.border)
            done_rect = pygame.Rect(self.border, self.border, done_height+self.border, done_height+self.border)
            over_text = pygame.font.SysFont("freesansbold.ttf", 120).render("Game Over!", True, (0,0,0))
            #winner_text = pygame.font.SysFont("freesansbold.ttf", 100).render(winner_string, True, (0,0,0))
            over_height = 50
            over_rect = pygame.Rect(self.height//2 - done_height//2 + 4, self.border +4, done_height-4, over_height)
            winner_rect = winner_text.get_rect(center = (300, 160))
            #winner_rect = pygame.Rect(self.border*2, self.border*2 + over_height, done_height-4, over_height)
            pygame.draw.rect(self.surface, color = (255,250,250), rect = done_rect)
            pygame.draw.rect(self.surface, color = (35,35,48), rect = done_rect, width=4)
            pygame.draw.rect(self.surface, color = (255,250,250), rect = over_rect)
            pygame.draw.rect(self.surface, color = (255,250,250), rect = winner_rect)
            self.surface.blit(over_text, (60, over_height))
            #self.surface.blit(winner_text, (2*self.border + 60, self.border*2 + 2*over_height+20))
            self.surface.blit(winner_text, winner_rect)

            lwpiece = self.height//2
            rwpiece = 4*over_height + 25
            cwpiece = (lwpiece, rwpiece)
            pieceradius = 30
            if num_winners == 1:
                piece_color = self.piece_colors[winner[0]]
                pygame.draw.circle(self.surface, piece_color,
                                        center=cwpiece, radius=pieceradius)
                pygame.draw.circle(self.surface, color=(35,35,48), center=cwpiece, radius = pieceradius, width = 4)
            else:
                for i in range(len(winner)):
                    piece_color = self.piece_colors[winner[i]]
                    lwpiece = (self.height // len(winner))//2 + (self.height//num_winners)*i
                    cwpiece = (lwpiece, rwpiece)
                    pygame.draw.circle(self.surface, piece_color,
                                        center=cwpiece, radius=pieceradius)
                    pygame.draw.circle(self.surface, color=(35,35,48), center=cwpiece, radius = pieceradius, width = 4)
            score_board_text = pygame.font.SysFont("freesansbold.ttf", 25).render("Scoreboard", True, (0,0,0))
            #scoreboard_rect = score_board_text.get_rect(center = (300, 250))
            scoreboard_rect = pygame.Rect(self.border*2+50, self.border*2 + 5*over_height, 480, 50)
            pygame.draw.rect(self.surface, color = (255,250,250), rect = scoreboard_rect)
            pygame.draw.rect(self.surface, color = (35,35,48), rect = scoreboard_rect, width=4)
            self.surface.blit(score_board_text, (250, 5*over_height+18))
            #self.surface.blit(score_board_text, scoreboard_rect)
            score_dict = self.go.scores()
            num_players = len(score_dict)
            for players in range(num_players):
                players = players + 1
                playerfinal_rect = pygame.Rect(self.border*2+50, self.border*2 + 5*over_height + players*28 -(4*players), 480, 28)
                player_text = "Player {} Score: {}".format(players, score_dict[players])
                finalscore_text = pygame.font.SysFont("freesansbold.ttf", 20).render(player_text, True, (0,0,0))
                #playerfinal_rect = finalscore_text.get_rect(center = (300, 250 + players*28-4*(players)))
                if players in winner:
                    pygame.draw.rect(self.surface, color = (0,204,0), rect = playerfinal_rect)
                else:
                    pygame.draw.rect(self.surface, color = (255,250,250), rect = playerfinal_rect)
                pygame.draw.rect(self.surface, color = (35,35,48), rect = playerfinal_rect, width=4)
                self.surface.blit(finalscore_text, (250, 300 + players*28-32 - 4*(players)))
                #self.surface.blit(finalscore_text, playerfinal_rect)


            exit_text = pygame.font.SysFont("freesansbold.ttf", 50).render("EXIT", True, (0,0,0))
            self.exit_rect = pygame.Rect(self.height//2-50, self.height-60, 100, 50)
            pygame.draw.rect(self.surface, color = (255,0,0), rect = self.exit_rect)
            pygame.draw.rect(self.surface, color = (35,35,48), rect = self.exit_rect, width=4)
            self.surface.blit(exit_text, (self.height//2 - 50+ self.border, self.height-50))

    def leave_gui(self,coord):
        if self.exit_rect.collidepoint(coord):
            pygame.quit()
            sys.exit()


def play_go(go: Go|GoFake) -> None:
    move: tuple[int,int]
    go_setup = GUIGeneralGo(go, 600, 5)
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Go")
    pygame.mixer.init
    pygame.mixer.music.load("gamemusic.mp3")
    pygame.mixer.music.set_volume(0.6)
    #go_setup.draw_board()
    go_setup.draw_move()
    clock = pygame.time.Clock()


    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.mouse.set_visible(True)
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))
            
            if event.type == pygame.MOUSEBUTTONUP:
                (mousex, mousey) = pygame.mouse.get_pos()
                mouse = (mousex, mousey)
                if go_setup.start and not go_setup.play_gui :
                    go_setup.leave_gui(mouse)
                if go_setup.start and go_setup.play_gui:
                    go_setup.reccd = False
                    move = ((mousey // go_setup.rh),(mousex // go_setup.rh))
                    if move in go_setup.go.available_moves:
                        move_bool = go_setup.go.legal_move(move)
                        if move_bool:
                            go_setup.go.apply_move(move)
                            #print(move, "CHOSEN MOVE IN GAME")
                            go_setup.draw_move()
                    ## if hit the pass button
                    pass_coord = (mousex,mousey)
                    if go_setup.pass_rect.collidepoint(pass_coord):
                        move = None
                        go_setup.go.apply_move(move)
                        go_setup.draw_move()
                    if go_setup.bot_rect.collidepoint(pass_coord):
                        go_setup.suggest_move()
                        #print("clicked")
                        #go_setup.surface.blit(go_setup.move_text, (go_setup.suggest_rect.centerx - 60, go_setup.suggest_rect.centery-75))
                    #coord = pygame.mouse.get_pos()
                    #go_setup.valid_move(coord)
                    #go_setup.draw_move()
                if go_setup.start_rect.collidepoint(coord) and not go_setup.music:
                    pygame.mixer.music.play(-1,0.0)
                    go_setup.play_gui = True
                    go_setup.start = True
                    go_setup.music = True
                    pygame.display.update()
        if go_setup.play_gui:
            go_setup.draw_move()
            coord = pygame.mouse.get_pos()
            go_setup.valid_move(coord)
            if go_setup.bot_rect.collidepoint(coord):
                pygame.draw.rect(go_setup.surface, color = (190,255,204), rect = go_setup.bot_rect)

        if not go_setup.start:
            go_setup.draw_move()
            coord = pygame.mouse.get_pos()
            if go_setup.start_rect.collidepoint(coord):
                pygame.draw.rect(go_setup.surface, color = (190,255,204), rect = go_setup.start_rect)
                go_setup.surface.blit(go_setup.start_text, (200,300))

        
                
        pygame.display.update()
        clock.tick(24)
if __name__ == "__main__":
    cmd()
#play_go(gogo)

    
