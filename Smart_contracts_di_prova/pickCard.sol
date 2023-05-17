// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;
contract CardDeck {
    enum Suit { Spades, Clubs, Diamonds, Hearts}
    enum Value {
        Two, Three, Four, Five, Six,
        Seven, Eight, Nine, Ten,
        Jack, King, Queen, Ace
    }
    struct Card {
        Suit suit;
        Value value;
    }

    Card public myCard;

    function pick_a_card(Suit _suit, Value _value) public returns (Suit, Value) {
        myCard.suit = _suit;
        myCard.value = _value;
        return (myCard.suit, myCard.value);
    }
}