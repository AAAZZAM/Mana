import bs4
import requests
import re
import time
import random
import retrying

def mtggoldfish(deck_id, header = None):
    """ Retrieves decklist from mtggoldfish.com with user provided deck_id.

    Parameters
    ----------

    deck_id: String of integers corresponding to valid deck on mtggoldfish.com.

    Returns
    -------

    maindeck: Dictionary, key:value pairs correspond to {card : number of copies in maindeck.}

    sidedeck: Dictionary, key:value pairs correspond to {card : number of copies in sidedeck.}

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
        maindeck[line.split(" ",maxsplit = 1)[1]] = line.split(" ",maxsplit = 1)[0]

    for line in re.split(r'\r|\n',sidedeck_doc)[1:-1]:
        sidedeck[line.split(" ",maxsplit = 1)[1]] = line.split(" ",maxsplit = 1)[0]

    return(maindeck,sidedeck)

if __name__ == "__main__":
