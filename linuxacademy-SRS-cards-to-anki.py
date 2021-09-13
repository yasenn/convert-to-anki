#!/usr/bin/env python3
import random
import genanki
import json
import sys
import os


def get_model():
    model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
        ],
        templates=[
          {
             'name': 'Card 1',
             'qfmt': '<div id="front">{{Front}}</div>',
             'afmt': '{{FrontSide}}<hr id="back"><div id="back">{{Back}}</div>',
          },
        ])
    return model


def new_deck(deck_name):
    random.seed(hash(deck_name))
    deck_id = random.randrange(1 << 30, 1 << 31)
    return genanki.Deck(deck_id, deck_name)


class Card(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


def new_card(model, front, back):
    return Card(model=model, fields=[front, back])


def main():
    if len(sys.argv) < 3:
        sys.exit('Usage: %s input.json output.apkg' % sys.argv[0])
    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: input file %s was not found!' % sys.argv[1])

    with open(sys.argv[1]) as input_data:
        cards = json.load(input_data)

    decks = []
    model = get_model()
    for card in cards:
        deck_name = card['deck_name']
        deck = new_deck(deck_name)
        card = new_card(model, card['front'], card['back'])
        deck.add_note(card)
        decks.append(deck)
    genanki.Package(decks).write_to_file(sys.argv[2])

    if os.path.exists(sys.argv[2]):
        print('File %s successfully written', sys.argv[2])
        exit(0)
    else:
        sys.exit('ERROR writing file %s' % sys.argv[2])


if __name__ == "__main__":
    main()
