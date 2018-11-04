import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
          "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}
playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "Card: %s of %s" % (self.rank, self.suit)


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        remaining_deck = ""
        for card in self.deck:
            remaining_deck += "\n " + card.__str__()
        return "The Deck has:" + remaining_deck

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        if len(self.deck) > 0:
            hand_out_card = self.deck.pop(0)
            return hand_out_card
        else:
            print("Deck empty")
            return False


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.balance = 100
        self.bet = 0

    def win_bet(self):
        self.balance += self.bet

    def lose_bet(self):
        self.balance -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Your current balance is {}. How much do you want to bet? ".format(chips.balance)))
        except ValueError:
            print("Please enter a integer value for the bet")
        else:
            if chips.bet > chips.balance:
                print("Bet too high, not enough funds ({})!".format(chips.balance))
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_aces()


def hit_or_stand(deck, hand):
    global playing
    go_on = ""
    while go_on != "hit" and go_on != "stand":
        go_on = input("Decision time! Do you want to hit or stand? ").lower()
        if go_on == "hit":
            hit(deck, hand)
            print("Player hits.")
        elif go_on == "stand":
            print('Player stands. Dealer is playing.')
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        break


def show_cards(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_final_cards(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(chips):
    print("Player busts")
    chips.lose_bet()


def player_wins(chips):
    print("Player wins")
    chips.win_bet()


def dealer_busts(chips):
    print("Dealer busts")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins")
    chips.lose_bet()


def push():
    print("It's a tie!")


player_chips = Chips()

if __name__ == "__main__":
    while True:
        print("Welcome to BlackJack!")

        my_deck = Deck()
        my_deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        for i in range(0, 2):
            player_hand.add_card(my_deck.deal())
            dealer_hand.add_card(my_deck.deal())
        player_hand.adjust_aces()

        take_bet(player_chips)

        show_cards(player_hand, dealer_hand)

        while playing:

            hit_or_stand(my_deck, player_hand)

            show_cards(player_hand, dealer_hand)

            if player_hand.value > 21:
                player_busts(player_chips)
                break

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(my_deck, dealer_hand)

            show_final_cards(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_chips)
            elif player_hand.value > dealer_hand.value:
                player_wins(player_chips)
            elif player_hand.value < dealer_hand.value:
                dealer_wins(player_chips)
            else:
                push()

        print("Your current balance is {}.".format(player_chips.balance))

        play_on = ''
        while play_on != "yes" and play_on != "no":
            play_on = input("Do you want to play again? Yes / No? ").lower()
            playing = True
        if play_on == "no":
            print("Thanks for playing. See you again!")
            break
        else:
            continue
