import pygame
from pygame.locals import *
import sys
from pgui import *
from blackjack import *

class Game(BlackJack):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption("Blackjack 21")
        self.surface = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.init_components()
        self.player_turn = True
    
    def init_components(self):
        self.lbl_playerI = Label("Player:", font_size=30, x=1100, y=50)
        self.lbl_botI = Label("Bot:", font_size=30, x=1100, y=150)
        self.lbl_playerII = Label("Player:", font_size=30, x=120, y=120)
        self.lbl_botII = Label("Bot:", font_size=30, x=120, y=350)
        self.lbl_player_hand = Label(f"[{self.get_hand_value(self.player)}]", font_size=30, x=1200, y=50)
        self.lbl_bot_hand = Label(f"? + [{sum(self.bot.hand[1:])}]", font_size=30, x=1160, y=150)
        self.lbl_player_hearts = Label("❤️" * self.player.hearts, font="seguiemj.ttf", font_size=30, x=1100, y=100)
        self.lbl_bot_hearts = Label("❤️" * self.bot.hearts, font="seguiemj.ttf", font_size=30, x=1100, y=200)
        self.lbl_announcer = Label("", font_size=30, x=self.surface.get_width()//2-80, y=560)
        self.lbl_decision = Label("Hit or Stand?", font_size=30, x=self.surface.get_width()//2-80, y=50)
        
        self.btn_hit = Button("Hit", font_size=30, width=100, height=50, x=500, y=620)
        self.btn_stand = Button("Stand", font_size=30, width=100, height=50, x=650, y=620)
        
        self.lbl_playagain = Label("Re-Play?", font_size=30, x=1100, y=350)
        self.btn_replay = Button("YES", font_size=30, width=100, height=50, x=1100, y=400)
        
        self.labels = (self.lbl_playerI, self.lbl_botI, self.lbl_playerII, self.lbl_botII, 
                       self.lbl_player_hand, self.lbl_bot_hand, self.lbl_player_hearts, 
                       self.lbl_bot_hearts, self.lbl_announcer, self.lbl_decision, self.lbl_playagain
        )

    def render_card(self, number, x, is_bot=False, is_hidden=False):
        card_number = f"{number:02d}"
        if is_hidden:
            card_number = " ? "
        card = BlackJackCard(card_number)
        card.pos_x = x
        card.pos_y = 400 if is_bot else 170
        card.background_color = "#000000"
        card.text_color = "#FFFFFF"
        card.draw()
    
    def render_hand(self, hand, is_bot=False):
        x = 120
        for card_number in hand:
            if hand.index(card_number) == 0 and is_bot:
                self.render_card(card_number, x, is_bot=is_bot, is_hidden=True)
            else:
                self.render_card(card_number, x, is_bot=is_bot)
            x += 120
    
    def get_hand_value(self, character):
        if isinstance(character, Player):
            return character.hand_value()
        else:
            return sum(character.hand[1:])
    
    def next_round(self, loser=None):
        if loser != None:
            loser.lose_heart()
            print(f"\nPlayer hearts[{self.player.hearts}]:", "❤️" * self.player.hearts)
            print(f"Bot hearts[{self.bot.hearts}]:", "❤️" * self.bot.hearts)
            print()
        
        self.player.reset_hand()
        self.bot.reset_hand()
        self.shuffle_and_draw()

        self.player_turn = True
        
    def wining_dicide(self):
        if self.player.hearts > 0 and self.bot.hearts > 0:
            winner = self.check_winner()
            if winner == "player":
                self.lbl_announcer.text = "You win!"
                self.next_round(loser=self.bot)
            elif winner == "bot":
                self.lbl_announcer.text = "Bot wins!"
                self.next_round(loser=self.player)
            else:
                self.lbl_announcer.text = "Draw!"
                self.next_round(loser=None)
            pygame.time.delay(1000)
        elif self.player.hearts == 0 or self.bot.hearts == 0:
            winner = "player" if self.player.hearts > 0 else "bot"
            self.lbl_announcer.text = f"{winner} wins!"
    
    def reset(self):
        self.player.hearts = 5
        self.bot.hearts = 5
        self.player.reset_hand()
        self.bot.reset_hand()
        self.shuffle_and_draw()
        self.player_turn = True
        print("\n New Game \n")
        print(f"\nPlayer hearts[{self.player.hearts}]:", "❤️" * self.player.hearts)
        print(f"Bot hearts[{self.bot.hearts}]:", "❤️" * self.bot.hearts)
        print()
    
    def start(self):
        self.reset()
        while True:
            if self.player.hearts == 0 or self.bot.hearts == 0:
                self.wining_dicide()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if self.btn_replay.clicked():
                            self.reset()
                
                self.surface.fill("#35654D")
                self.lbl_announcer.draw()
                self.lbl_playagain.draw()
                self.btn_replay.draw()            
            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if self.btn_replay.clicked():
                            self.reset()
                        
                        if self.btn_hit.clicked() and self.player_turn:
                            if not self.shuffler.is_empty():
                                self.player.draw_card()
                                print("\nPlayer hand:", self.player.show_hand(), "-->", self.get_hand_value(self.player))
                                if self.get_hand_value(self.player) > 21:
                                    self.lbl_announcer.text = "You busted!"
                                    self.lbl_announcer.draw()
                            else:
                                self.wining_dicide()
                        elif self.btn_stand.clicked() and self.player_turn:
                                self.player_turn = False 
                            
                if not self.player_turn:
                    self.lbl_decision.text = "Bot's turn"
                    if not self.shuffler.is_empty():
                        if self.get_hand_value(self.bot) <= 17:
                            self.bot.draw_card()
                            print("\nBot hand:", self.bot.show_hand(True), "-->", self.get_hand_value(self.bot))
                            pygame.time.delay(250)
                        elif self.get_hand_value(self.bot) > 21:
                            self.lbl_announcer.text = "Bot busted!"
                            self.lbl_announcer.draw()
                            self.wining_dicide()
                        else:
                            self.lbl_announcer.text = "Bot stands"
                            self.lbl_announcer.draw()
                            self.wining_dicide()                
                    else:
                        self.wining_dicide()
                else:
                    self.lbl_decision.text = "Hit or Stand?"  
                
                self.surface.fill("#35654D")
                
                for lbl in self.labels:
                    lbl.draw()
                
                self.btn_hit.draw()
                self.btn_stand.draw()
                self.btn_replay.draw()
                
                self.lbl_bot_hand.text = f"? + [{sum(self.bot.hand[1:])}]"
                self.lbl_player_hand.text = f"[{self.get_hand_value(self.player)}]"
                self.lbl_bot_hearts.text = "❤️" * self.bot.hearts
                self.lbl_player_hearts.text = "❤️" * self.player.hearts
                
                self.render_hand(self.player.hand)
                self.render_hand(self.bot.hand, is_bot=True)
            
            pygame.display.update()
            self.clock.tick(self.fps)
         
if __name__ == "__main__":
    blackjackgame = Game()
    blackjackgame.start()