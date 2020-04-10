import random
import numpy as np
import time

def rules():
    'Explain rules here'
    print("""\n\n\nIn this game you are will be playing blackjack against a highly advanced AI system that
leverages Googles quantum API's to try to predict the future, convolutional fourier deep
learning networks to achieve strategic perfection, and bit-crypto-blockchain (BCB) algorithms
to pass information as efficiently as possible.

The rules of the game are as follows:

1. Each round you may choose the bet/pot amount. For instance, if you choose $100, both you
   and the AI will place $50 in the pot.
2. Each turn you may choose to hit or stand. If you hit, you are dealt a card. Your goal is
   to accumulate enough cards that you get close to a score of 21, but you will lose if you
   go over 21.
3. Every numbered card is worth its face value. Aces are worth either 1 or 11 depending on
   what is convenient to you. Jacks, Queens, and Kings are all worth 10.
4. Both you and the AI start with $1000.
""")

class Game:
    def __init__(self,start_balance,player,ai):
        self.cards = ['A','1','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.printable_cards = {}
        for card in self.cards:
            if card != '10':
                self.printable_cards[card] = ' ___ \n|   |\n| {} |\n|___|'.format(card)
            else:
                self.printable_cards[card] = ' ___ \n|   |\n|{} |\n|___|'.format(card)
        self.set_deck()
        self.player_class = player
        self.ai_class = ai
        self.player_balance = start_balance
        self.ai_balance = start_balance

    def set_deck(self):
        self.deck = self.cards*4

    def player_move_func(self):
        player_move = self.player.action(self.deck)
        return player_move

    def ai_move_func(self):
        ai_move = self.ai.action(self.deck)
        return ai_move

    def player_wins(self):
        self.player_balance += self.pot
        self.ai_balance -= self.pot
        print('\nYou win this round! Your new balance is: {}, The AI new balance is: {}\n'.format(self.player_balance,
                                                                                                 self.ai_balance))

    def ai_wins(self):
        self.player_balance -= self.pot
        self.ai_balance += self.pot
        print('\nYou lose this round... Your new balance is: {}, The AI new balance is: {}\n'.format(self.player_balance,
                                                                                                    self.ai_balance))
    def nobody_wins(self):
        print('\nScores are the same, nobody wins.\n')

    def start(self):
        go = 'YES'
        count = 1
        while go.lower() != 'no':
            print('\n' + 'ROUND {} '.format(count)* 10 + '\n')
            self.game_round()
            go = str(input('\nWould you like to keep playing? yes/no\n> '))
            count += 1
        quit()


    def game_round(self):
        self.pot = None
        while type(self.pot) != int:
            self.pot = input('How much would you like to bet this round?\n> ')
            try:
                self.pot = int(float(self.pot))
            except:
                pass
        self.set_deck()
        self.ai = self.ai_class()
        self.player = self.player_class()
        player_move = None
        ai_move = None
        while player_move != 'stand' or ai_move != 'stand':
            player_move = self.player_move_func()
            player_score = self.player.calc_score()
            for i in range(3):
                time.sleep(0.4)
                print('.')
            time.sleep(0.8)
            ai_move = self.ai_move_func()
            ai_score = self.ai.calc_score()
            print('\nYour Cards:\n')
            for card in self.player.cards:
                print(self.printable_cards[card])
            if player_score > 21:
                print('\nYour score went over 21, you lose.')
                self.ai_wins()
                return None
            if ai_score > 21:
                print('\nThe AI score went over 21, you win.')
                self.player_wins()
                return None
            #print('AI Score: {}'.format(ai_score))
        print('\nAI Cards:\n')
        for card in self.ai.cards:
            print(self.printable_cards[card])
        player_score = self.player.calc_score()
        ai_score = self.ai.calc_score()
        if player_score > ai_score:
            self.player_wins()
        elif ai_score > player_score:
            self.ai_wins()
        else:
            self.nobody_wins()

class Player:
    def __init__(self):
        self.cards = []
        self.scoresheet = {'1':1, '2':2,'3':3,'4':4,
                           '5':5,'6':6,'7':7,
                           '8':8,'9':9,'10':10,
                           'J':10,'Q':10,'K':10}

    def draw_card(self,deck):
        random.shuffle(deck)
        card = deck.pop()
        self.cards.append(card)

    def calc_score(self):
        score = 0
        for i in self.cards:
            try:
                score += self.scoresheet[i]
            except:
                pass
        # after working through a long algorithm I figure out
        # it could be shortened to this
        As = self.cards.count('A')
        if As != 0:
            score1 = score + As
            score2 = score + As + 10
            if score2 > 21:
                return score1
            else:
                return score2
        else:
            return score

    def hit(self,deck):
        self.draw_card(deck)
        print('\nYou choose to HIT')

    def stand(self):
        print('\nYou choose to STAND')

    def action(self,deck):
        player_action = None
        while player_action != 'hit'and player_action != 'stand':
            player_action = str(input('\nWould you like to hit or stand?\n> ')).lower()
        if player_action == 'hit':
            self.hit(deck)
            return 'hit'
        else:
            self.stand()
            return 'stand'


class AI:
    def __init__(self):
        self.cards = []
        self.risk = int(np.random.uniform(12,20))
        self.scoresheet = {'1':1, '2':2,'3':3,'4':4,
                           '5':5,'6':6,'7':7,
                           '8':8,'9':9,'10':10,
                           'J':10,'Q':10,'K':10}

    def calc_score(self):
        score = 0
        for i in self.cards:
            try:
                score += self.scoresheet[i]
            except:
                pass
        # after working through a long algorithm I figure out
        # it could be shortened to this
        As = self.cards.count('A')
        if As != 0:
            score1 = score + As
            score2 = score + As + 10
            if score2 > 21:
                return score1
            else:
                return score2
        else:
            return score

    def action(self,deck):
        if self.calc_score() <= self.risk:
            self.hit(deck)
            return 'hit'
        else:
            self.stand()
            return 'stand'

    def draw_card(self,deck):
        random.shuffle(deck)
        card = deck.pop()
        self.cards.append(card)

    def hit(self,deck):
        self.draw_card(deck)
        print('The AI chooses to HIT\n')
        return 'hit'

    def stand(self):
        print('The AI chooses to STAND\n')
        return 'stand'


if __name__ == '__main__':
    rules()
    # print starting balance here
    game = Game(1000,Player,AI)
    game.start()
