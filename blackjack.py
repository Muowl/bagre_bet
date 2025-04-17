import random

class Blackjack:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_bet = 0

    def create_deck(self):
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        hand.append(self.deck.pop())

    def calculate_score(self, hand):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        score = sum(values[card['rank']] for card in hand)
        aces = sum(1 for card in hand if card['rank'] == 'A')
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def start_new_round(self, bet):
        self.player_hand = []
        self.dealer_hand = []
        self.player_bet = bet
        self.deal_card(self.player_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        self.deal_card(self.dealer_hand)

    def determine_winner(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        if player_score > 21:
            return 'dealer'
        elif dealer_score > 21 or player_score > dealer_score:
            return 'player'
        elif player_score < dealer_score:
            return 'dealer'
        else:
            return 'tie'