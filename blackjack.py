import random

class Shuffler: # stack implementation
    def __init__(self):
        self.deck = []
        for card_num in range(1, 11):
            self.add_card(card_num)
            
        self.shuffled_deck = self.deck.copy()

    def reset(self):
        self.shuffled_deck = self.deck.copy()

    def shuffle(self):
        random.shuffle(self.shuffled_deck)
    
    def add_card(self, card): # push stack
        self.deck.append(card)

    def draw(self): # pop stack
        if self.is_empty():
            return None
        card = self.shuffled_deck.pop()
        return card
    
    def is_empty(self): # is stack empty?
        return len(self.shuffled_deck) == 0

    def top_card(self): # peek stack
        if self.is_empty():
            return None
        return self.shuffled_deck[-1]
    
    def count(self): # stack size
        return len(self.shuffled_deck)

class Character:
    def __init__(self, shuffler):
        self.shuffler = shuffler
        self.hand = []
        self.hearts = 5

    def draw_card(self):
        card = self.shuffler.draw()
        if card is not None:
            self.hand.append(card)
    
    def reset_hand(self):
        self.hand.clear()

    def show_hand(self, hide_first_card=False):
        if hide_first_card:
            return ["?", *self.hand[1:]]
        else:
            return self.hand

    def hand_value(self):
        return sum(self.hand)

    def lose_heart(self):
        self.hearts -= 1

    def has_hearts(self):
        return self.hearts > 0
    
    def make_decision(self):
        pass

class Player(Character):
    def __init__(self, shuffler):
        super().__init__(shuffler)
    
    def make_decision(self):
        while True:
            decision = input("Do you want to 'hit' or 'stand'?: ").strip().lower()

            if decision.lower() in ["hit", "stand"]:
                return decision.lower()
            else:
                print("Invalid input. Please enter 'hit' or 'stand'.")

class Bot(Character):
    def __init__(self, shuffler):
        super().__init__(shuffler)
    
    def make_decision(self):
        if self.get_hand_value() < 17:
            return "hit"
        else:
            return "stand"

class BlackJack:
    def __init__(self):
        self.shuffler = Shuffler()
        self.player = Player(self.shuffler)
        self.bot = Bot(self.shuffler)
    
    def get_hand_value(self, character):
        if isinstance(character, Player):
            return character.hand_value()
        else:
            return sum(character.hand[1:])
    
    def check_winner(self):
        player_score = self.get_hand_value(self.player)
        bot_score = self.get_hand_value(self.bot)
        
        if player_score == 21:
            return "player"
        elif bot_score == 21:
            return "bot"
        elif player_score > 21 or (bot_score <= 21 and abs(21 - player_score) > abs(21 - bot_score)):
            return "bot"
        elif bot_score > 21 or (player_score <= 21 and abs(21 - player_score) < abs(21 - bot_score)):
            return "player"
        else:
            return "It's a tie"
    
    def shuffle_and_draw(self):
        self.shuffler.reset()
        self.shuffler.shuffle()
        
        for _ in range(2):
            self.player.draw_card()
            self.bot.draw_card()

    def next_round(self, loser):
        loser.lose_heart() 
        self.player.reset_hand()
        self.bot.reset_hand()
        
        self.shuffle_and_draw()
            
        if loser == self.player:
            print("bot wins this round.")
        else:
            print("player wins this round.")
            
        print(f"Player hearts[{self.player.hearts}]:", "❤️" * self.player.hearts)
        print(f"Bot hearts[{self.bot.hearts}]:", "❤️" * self.bot.hearts)
        print()
        
    def charactor_decide(self):
        while True:
            print("Player hand:", self.player.show_hand(), "-->", self.get_hand_value(self.player))
            print("Bot hand:", self.bot.show_hand(True), "--> ? +", self.get_hand_value(self.bot))
            decision = self.player.make_decision()
            if decision == "hit":
                self.player.draw_card()
            else:
                break
            
        while True:
            print("bot hand:", self.bot.show_hand(), "--> ?+", self.get_hand_value(self.bot))
            decision = self.bot.make_decision()
            if decision == "hit":
                self.bot.draw_card()
            else:
                break
        print()
        
    def play(self):
        self.player.hearts = 5
        self.bot.hearts = 5
        self.shuffle_and_draw()
        
        while self.player.has_hearts() and self.bot.has_hearts():
            self.charactor_decide()
            
            winner = self.check_winner()
            
            if winner == "player":
                self.next_round(loser=self.bot)
            elif winner == "bot":
                self.next_round(loser=self.player)
    
    def start(self):
        self.play()
        while True:
            if self.player.hearts == 0 or self.bot.hearts == 0:
                decision = input("Did you want to re-play? (y/n) ").strip().lower()
                if decision.lower() in ["y", "yes"]:
                    self.play()
                else:
                    break
            else:
                break
        
if __name__ == "__main__":
    blackjackgame = BlackJack()
    blackjackgame.start()