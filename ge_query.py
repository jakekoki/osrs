import requests
import argparse
from tabulate import tabulate

from bs4 import BeautifulSoup as bs

def _ge_query_parser(item):
    """
    Handles search strings with spaces and in case-insensitive way. 
    TODO: Make this less stupid eventually.
    """
    # Make all caps chars lower-case
    item = item.lower()
    return item 

def get_ge_data(item):
    """
    Returns GP value of item on Grand Exchange.
    """
    item = _ge_query_parser(item)
    exchange_url = "https://oldschool.runescape.wiki/w/Exchange:{}".format(item)
    try:
        r = requests.get(exchange_url)
        soup = bs(r.text, 'html.parser').find("div", {"id": "content"})

        ge_attributes = ["id", "GEPrice", "members", "limit", "highalch", "lowalch", "volume", "value"]
        properties = []
        properties.append(["Item Name", item]) # append title
        for attr in ge_attributes:
            # GE price exists in different div for some reason
            if attr == "GEPrice":
                price = soup.find(id=attr).text
                properties.append([attr, price])
                continue
            item = soup.find("div", {"class": "gemw-property gemw-{}".format(attr)})
            prop_key = item.find('dt').text
            prop_val = item.find('dd').text
            property_pair = [prop_key, prop_val]
            properties.append(property_pair)

        return properties
    except Exception as e:
        print("Cannot find item!")
        return

def display_ge_data(properties):
    return tabulate(
        properties, 
        tablefmt="grid", 
        numalign='left', 
        headers="firstrow"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Command line args for GE price checker.') 
    parser.add_argument('--item', help='Item you want to look up.')
    args = parser.parse_args()
    print(display_ge_data(get_ge_data(args.item)))
