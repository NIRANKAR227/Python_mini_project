import random

class card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards=[]
        suits=["Spades","Club","Heart","diamond"]

        ranks=[{"rank":"A","value":11},
            {"rank":"2","value":2},
            {"rank":"3","value":3},
            {"rank":"4","value":4},
            {"rank":"5","value":5},
            {"rank":"6","value":6},
            {"rank":"7","value":7},
            {"rank":"8","value":8},
            {"rank":"9","value":9}, 
            {"rank":"10","value":10},
            {"rank":"J","value":10},
            {"rank":"Q","value":10},
            {"rank":"K","value":10},]
        
        for suit in suits:
            for rank in ranks:
                self.cards.append([suit,rank])
        print("Length:",len(self.cards))


    def shuffle(self):
        if len(self.cards)>1:
            random.shuffle(self.cards)

    def deal(self,number):
        cards_dealt=[]
        for x in range(number):
            if len(self.cards)>0:
                card=self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt


class Hand:
    def __init__(self,dealer=False):
        self.cards=[]
        self.value=0
        self.dealer=dealer
    
    def add_Card(self,card_list):
        self.cards.extend(card_list)


    def calculate_value(self):
        self.value=0  
        has_ACE=False
        for card in self.cards:
            card_value=int(card[1]["value"])
            self.value+=card_value
            if card[1]['rank']=="A":
                has_ACE=True

        if has_ACE and self.value>21:
            self.value-=10

    def get_value(self):
        self.calculate_value()
        return self.value
    
    def is_blackjack(self):
        return self.value==21
    
    def display(self,show_All_dealer_card=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index,card in enumerate(self.cards):
            if index==0 and self.dealer and not show_All_dealer_card and not self.is_blackjack():
                print("hidden")
            else:
                print(card)
        if not self.dealer:
            print("Value:",self.get_value())
        print()

class Game:
    def play(self):
        gamenumber=0
        gamestoplay=0
        
        while gamestoplay<=0:
            try:
                gamestoplay=int(input("How many games do you want to play? "))
            except:
                print("You must enter a number:") 
        
        while gamenumber<gamestoplay:
            gamenumber+=1

            deck=Deck()
            deck.shuffle()

            player_hand=Hand()
            dealer_hand=Hand(dealer=True)
            
            for i in range(2):
                player_hand.add_Card(deck.deal(1))
                dealer_hand.add_Card(deck.deal(1))

            print()
            print("*"*30)
            print(f"Game {gamenumber} of {gamestoplay}")
            print("*"*30)
            player_hand.display()
            dealer_hand.display()

            if self.check_Winner(player_hand,dealer_hand):
                continue
            
            choice=""
            while player_hand.get_value()<21 and choice not in ["s","stand"]:
                choice=input("Please enter 'Hit' or 'Stand' (or H/S)").lower()
                print()
                if choice in ["hit","h"]:
                    player_hand.add_Card(deck.deal(1))
                    player_hand.display()
            if self.check_Winner(player_hand,dealer_hand):
                continue

            player_hand_value=player_hand.get_value()
            dealer_hand_value=dealer_hand.get_value()

            while dealer_hand_value<17:
                dealer_hand.add_Card(deck.deal(1))
                dealer_hand_value=dealer_hand.get_value()

            dealer_hand.display(show_All_dealer_card=True)

            if self.check_Winner(player_hand,dealer_hand):
                continue

            print("Final Results")
            print("Your hand:",player_hand_value)
            print("Dealer's hand:",dealer_hand_value)

            self.check_Winner(player_hand,dealer_hand,True)

        print("\n Thanks For Playing")

    def check_Winner(self,player_hand,dealer_hand,game_over=False):
        if not game_over:
            if player_hand.get_value()>21:
                print("You Busted! Dealer Win")
                return True
            elif dealer_hand.get_value()>21:
                print("Dealer Busted! you Win")
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack:
                print("Both Player Have Blackjack! Tie!")
                return True
            elif player_hand.is_blackjack():
                print("Dealer Busted! you Win")
                return True
            elif dealer_hand.is_blackjack():
                print("You Busted! Dealer Win")
                return True
        else:
            if player_hand.get_value()>dealer_hand.get_value():
                print("You Win !")
            elif player_hand.get_value()==dealer_hand.get_value():
                print("Tie !")
            else:
                print("Dealer Win!")
            return True
        return False


g=Game()
g.play()
