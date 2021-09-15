#!/usr/bin/env python3
import random
import genanki
import sys
import os
from bs4 import BeautifulSoup


def get_model():
    model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
        ],
        templates=[{
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

    decks = []
    model = get_model()

    with open(sys.argv[1]) as fileDescriptor:
        html = fileDescriptor.read()
    bs = BeautifulSoup(html, "html.parser")
    deck_name = bs.select('h1.UIHeading')[0].text.strip()
    cards = bs.findAll('div', class_='SetPageTerms-term')
    for card in cards:
        bs_sides = BeautifulSoup(str(card), "html.parser")
        sides = bs_sides.findAll('div', {"class": [
                                        "SetPageTerm-smallSide",
                                        "SetPageTerm-largeSide"
                                        ]
                                    })
        deck = new_deck(deck_name)
        card = new_card(model, sides[0].get_text(), sides[1].get_text())
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
