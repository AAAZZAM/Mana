import bs4
import requests
import re
import time
import random
import retrying
import sys
from dateutil import parser

def mtggoldfish(deck_id, header = None):
    """ Retrieves decklist from mtggoldfish.com with user provided deck_id.

    Parameters
    ----------

    deck_id: String of integers corresponding to valid deck on mtggoldfish.com.

    Returns
    -------

    deck: JSON object containing deck_id, maindeck, and sidedeck. In main deck, a dictionary object,
    key:value pairs correspond to {card : number of copies in maindeck.} Likewise, sidedeck is a
    dictionary object, key:value pairs correspond to {card : number of copies in sidedeck.}

    """

    # Instantiate the url by appending the deck_id to the usual stem.
    url = 'https://www.mtggoldfish.com/deck/'+str(deck_id)

    # Request the url and extract its raw html.
    html = requests.get(url).content

    # Convert raw html to BeautifulSoup object.
    soup = bs4.BeautifulSoup(html,features="lxml")

    # Fetch the deck list from the BeautifulSoup object.

    decklist = soup.find(id = "deck_input_deck").get('value')

    maindeck_doc, sidedeck_doc = re.split(r'sideboard',decklist)

    # Now we convert our document into our desired dictionary output.

    maindeck, sidedeck = {}, {}

    for line in re.split(r'\r|\n',maindeck_doc)[:-1]:
        maindeck[line.split(" ",maxsplit = 1)[1]] = int(line.split(" ",maxsplit = 1)[0])

    for line in re.split(r'\r|\n',sidedeck_doc)[1:-1]:
        sidedeck[line.split(" ",maxsplit = 1)[1]] = int(line.split(" ",maxsplit = 1)[0])

    # We'll instantiate our output and collect some metadata about the deck.
    deck = {}
    deck['deck_id'] = deck_id

    deck['player'] = next(iter(re.findall(r'(?<=\/player\/)\w+',str(soup))),'')
    deck['format'] = next(iter(re.findall(r'(?<=Format:\s)\w+',str(soup))),'')
    deck['date'] = next(iter(re.findall(r'\w+\s\d+\,\s\d+',str(soup))),'')
    deck['tournament_id']= next(iter(re.findall(r'(?<=\/tournament\/)\d+',str(soup))),'')
    deck['source'] = 'mtggoldfish'

    # We now include the maindeck and sidedeck into our output.
    deck['maindeck'] = maindeck
    deck['sidedeck'] = sidedeck
    print(deck)
    return(deck)

if __name__ == "__main__":
    mtggoldfish(*sys.argv[1:])
