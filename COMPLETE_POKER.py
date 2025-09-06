import random

deck = []
dealt_cards = []
player_buyin_amount = 100
community = None

class Card:
    def __init__(self, number, value, suite, weight):
        self.number = number
        self.value = value
        self.suite = suite
        self.weight = weight

    def __str__(self):
        return f"{self.value:>2}-{self.suite}"

class Deck:
    def __init__(self):
        self.deck = []
        self.deck.append(Card(1, 'A', 'S', 2653))
        self.deck.append(Card(2, '2', 'S', 157))
        self.deck.append(Card(3, '3', 'S', 365))
        self.deck.append(Card(4, '4', 'S', 573))
        self.deck.append(Card(5, '5', 'S', 781))
        self.deck.append(Card(6, '6', 'S', 989))
        self.deck.append(Card(7, '7', 'S', 1197))
        self.deck.append(Card(8, '8', 'S', 1405))
        self.deck.append(Card(9, '9', 'S', 1613))
        self.deck.append(Card(10, '10', 'S', 1821))
        self.deck.append(Card(11, 'J', 'S', 2029))
        self.deck.append(Card(12, 'Q', 'S', 2237))
        self.deck.append(Card(13, 'K', 'S', 2445))
        self.deck.append(Card(14, 'A', 'H', 2601))
        self.deck.append(Card(15, '2', 'H', 105))
        self.deck.append(Card(16, '3', 'H', 313))
        self.deck.append(Card(17, '4', 'H', 521))
        self.deck.append(Card(18, '5', 'H', 729))
        self.deck.append(Card(19, '6', 'H', 937))
        self.deck.append(Card(20, '7', 'H', 1145))
        self.deck.append(Card(21, '8', 'H', 1353))
        self.deck.append(Card(22, '9', 'H', 1561))
        self.deck.append(Card(23, '10', 'H', 1769))
        self.deck.append(Card(24, 'J', 'H', 1977))
        self.deck.append(Card(25, 'Q', 'H', 2185))
        self.deck.append(Card(26, 'K', 'H', 2393))
        self.deck.append(Card(27, 'A', 'C', 2549))
        self.deck.append(Card(28, '2', 'C', 53))
        self.deck.append(Card(29, '3', 'C', 261))
        self.deck.append(Card(30, '4', 'C', 469))
        self.deck.append(Card(31, '5', 'C', 677))
        self.deck.append(Card(32, '6', 'C', 885))
        self.deck.append(Card(33, '7', 'C', 1093))
        self.deck.append(Card(34, '8', 'C', 1301))
        self.deck.append(Card(35, '9', 'C', 1509))
        self.deck.append(Card(36, '10', 'C', 1717))
        self.deck.append(Card(37, 'J', 'C', 1925))
        self.deck.append(Card(38, 'Q', 'C', 2133))
        self.deck.append(Card(39, 'K', 'C', 2341))
        self.deck.append(Card(40, 'A', 'D', 2497))
        self.deck.append(Card(41, '2', 'D', 1))
        self.deck.append(Card(42, '3', 'D', 209))
        self.deck.append(Card(43, '4', 'D', 417))
        self.deck.append(Card(44, '5', 'D', 625))
        self.deck.append(Card(45, '6', 'D', 833))
        self.deck.append(Card(46, '7', 'D', 1041))
        self.deck.append(Card(47, '8', 'D', 1249))
        self.deck.append(Card(48, '9', 'D', 1457))
        self.deck.append(Card(49, '10', 'D', 1665))
        self.deck.append(Card(50, 'J', 'D', 1873))
        self.deck.append(Card(51, 'Q', 'D', 2081))
        self.deck.append(Card(52, 'K', 'D', 2289))

    def deal_card():
        global deck
        global dealt_cards
        value = random.randint(1, len(deck))

        while (deck[value - 1]) in dealt_cards:
            value = random.randint(1,52)
        
        dealt_card = deck[value - 1]
        dealt_cards.append(dealt_card)
        deck.remove(dealt_card)
        
        return dealt_card
    
    class Community:
        def __init__(self):
            self.flop1 = None
            self.flop2 = None
            self.flop3 = None
            self.turn = None
            self.river = None
    
        def deal_flop(self):
            self.flop1 = Deck.deal_card()
            self.flop2 = Deck.deal_card()
            self.flop3 = Deck.deal_card()

        def deal_turn(self):
            self.turn = Deck.deal_card()

        def deal_river(self):
            self.river = Deck.deal_card()

        def __str__(self):
            final_str = 'Community Cards:\n'
            
            if (self.flop1 != None):
                final_str += 'Flop:    ' + str(self.flop1) + '   ' + str(self.flop2) + '   ' + str(self.flop3) + '\n'
            if (self.turn != None):
                final_str += 'Turn:    ' + str(self.turn) + '\n'
            if (self.river != None):
                final_str += 'River:   ' + str(self.river) + '\n'
            final_str += '\n'

            return final_str

class Player:
    def __init__(self, order, name):
        self.order = order
        self.name = name
        self.card1 = None
        self.card2 = None
        self.balance = player_buyin_amount
        self.position = ''
        self.hand = None
        
    def deal_cards_to_player(self):
        self.card1 = Deck.deal_card()
        self.card2 = Deck.deal_card()

    def print_player_cards(self):
        print(self.name + ':' + (' ' * (12 - len(self.name))) + str(self.card1) + '   ' + str(self.card2))

    def evaluate_hand(self):
        self.hand = Hand(self.card1, self.card2)

    def __str__(self):
        return self.name + ':' + (' ' * (17 - len(self.name))) + str(self.hand)

class Hand:
    def __init__(self, player_card1, player_card2):
        global community
        self.all_cards = [player_card1, player_card2, community.flop1, community.flop2, community.flop3, community.turn, community.river]
        self.hand_cards = []
        self.name = ''
        self.determine_hand()

    def sort_cards(card_list, ace_low):
        value_ranking = {'2'  :  1,
                         '3'  :  2,
                         '4'  :  3,
                         '5'  :  4,
                         '6'  :  5,
                         '7'  :  6,
                         '8'  :  7,
                         '9'  :  8,
                         '10' :  9,
                         'J'  : 10,
                         'Q'  : 11,
                         'K'  : 12,
                         'A'  : 13}
        
        ace_low_value_ranking = {'A'  :  1,
                                 '2'  :  2,
                                 '3'  :  3,
                                 '4'  :  4,
                                 '5'  :  5,
                                 '6'  :  6,
                                 '7'  :  7,
                                 '8'  :  8,
                                 '9'  :  9,
                                 '10' : 10,
                                 'J'  : 11,
                                 'Q'  : 12,
                                 'K'  : 13}
        
        suite_ranking = {'D' : 1,
                         'C' : 2,
                         'H' : 3,
                         'S' : 4}
        
        for i in range(1, len(card_list)):
            key = card_list[i]
            j = i - 1

            if (ace_low):
                while (j >= 0 and ace_low_value_ranking[key.value] > ace_low_value_ranking[card_list[j].value]):
                    card_list[j + 1] = card_list[j]
                    j -= 1
            
            else:
                while (j >= 0 and value_ranking[key.value] > value_ranking[card_list[j].value]):
                    card_list[j + 1] = card_list[j]
                    j -= 1
                
            if (key.value == card_list[j].value):
                if (suite_ranking[key.suite] > suite_ranking[card_list[j].suite]):
                    temp = key
                    key = card_list[j]
                    card_list[j] = temp
            
            card_list[j + 1] = key

        return card_list
    
    def get_high_card(self):
        self.hand_cards = Hand.sort_cards(self.all_cards, False)[:5]
        self.name = 'High Card'

    def determine_hand(self):
        if (self.name == ''):
            self.get_high_card()

    def __str__(self):
        return self.name + (' ' * (17 - len(self.name))) + str(self.hand_cards[0]) + '   ' + str(self.hand_cards[1]) + '   ' + str(self.hand_cards[2]) + '   ' + str(self.hand_cards[3]) + '   ' + str(self.hand_cards[4])

def test():
    global deck
    global dealt_cards
    global community

    deck = Deck().deck
    
    player1 = Player(0, 'Vishwa')
    player2 = Player(1, 'Vishnu')
    player3 = Player(2, 'Prakash')
    player4 = Player(3, 'Kavitha')

    player1.deal_cards_to_player()
    player2.deal_cards_to_player()
    player3.deal_cards_to_player()
    player4.deal_cards_to_player()

    player1.print_player_cards()
    player2.print_player_cards()
    player3.print_player_cards()
    player4.print_player_cards()
    print()
    
    community = Deck.Community()
    community.deal_flop()
    community.deal_turn()
    community.deal_river()
    print(community)

    player1.evaluate_hand()
    player2.evaluate_hand()
    player3.evaluate_hand()
    player4.evaluate_hand()

    print(player1)
    print(player2)
    print(player3)
    print(player4)
    print()


test()
