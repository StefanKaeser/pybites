import requests

STOCK_DATA = 'https://bit.ly/2MzKAQg'

# pre-work: load JSON data into program

with requests.Session() as s:
    data = s.get(STOCK_DATA).json()


# your turn:

def _cap_str_to_mln_float(cap):
    """If cap = 'n/a' return 0, else:
       - strip off leading '$',
       - if 'M' in cap value, strip it off and return value as float,
       - if 'B', strip it off and multiple by 1,000 and return
         value as float"""
    if cap == 'n/a':
        return 0
    # Strip leading '$'
    cap = cap[1:]
    if cap[-1] == 'M':
        return float(cap[:-1])
    if cap[-1] == 'B':
        return 1000 * float(cap[:-1])

def get_industry_cap(industry):
    """Return the sum of all cap values for given industry, use
       the _cap_str_to_mln_float to parse the cap values,
       return a float with 2 digit precision"""
    selected_stocks = [stock for stock in data if stock['industry']==industry] 
    industry_caps = [_cap_str_to_mln_float(stock['cap']) \
                     for stock in selected_stocks] 
    # The round function is only here, because pythons sum function returns
    # 243295.36000000002, which is kinda buggy.
    industry_cap = round(sum(industry_caps), 2)
    return industry_cap

def get_stock_symbol_with_highest_cap():
    """Return the stock symbol (e.g. PACD) with the highest cap, use
       the _cap_str_to_mln_float to parse the cap values"""
    get_cap_from_stock = lambda stock : _cap_str_to_mln_float(stock['cap'])
    stocks_descending_by_cap = sorted(data, reverse=True,
                                     key=get_cap_from_stock) 
    stock_symbol_with_highest_cap = stocks_descending_by_cap[0]['symbol']
    return stock_symbol_with_highest_cap

from collections import Counter

def get_sectors_with_max_and_min_stocks():
    """Return a tuple of the sectors with most and least stocks,
       discard n/a"""
    sectors = [stock['sector'] for stock in data if stock['sector'] != 'n/a']
    number_of_stocks_in_sector = Counter(sectors)
    max_common_sector = number_of_stocks_in_sector.most_common()[0][0]
    min_common_sector = number_of_stocks_in_sector.most_common()[-1][0]
    return max_common_sector, min_common_sector
