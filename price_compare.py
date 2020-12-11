import argparse
import math 

from ge_query import get_ge_data

def parse_ge_data(item_data):
    '''
    Converts item_data list of lists into dictionary.
    '''
    item_dict = {}
    for datum in item_data:
        item_dict[datum[0]] = datum[1]

    return item_dict

def price_compare(item1, item2):
    '''
    Args item1 and item2 are get_ge_data returns.
    '''
    item1 = parse_ge_data(get_ge_data(item1))
    item2 = parse_ge_data(get_ge_data(item2))
    p1 = int(item1['GEPrice'].replace(",", ""))
    p2 = int(item2['GEPrice'].replace(",", ""))

    price_diff = abs(p1 - p2)
    return_str = "{} is worth {} GP {} than {}."

    if p1 < p2:
        return return_str.format(
            item1['Item Name'], 
            price_diff,
            "less", 
            item2['Item Name']
        )
    elif p1 > p2:
        return return_str.format(
            item1['Item Name'], 
            price_diff,
            "more", 
            item2['Item Name']
        )
    else:
        return "These items are equal price!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool for comparing price of two items.') 
    parser.add_argument('--item1', help='First item to compare.')
    parser.add_argument('--item2', help='Second item to compare.')
    args = parser.parse_args()
    print(price_compare(args.item1, args.item2))