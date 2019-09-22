import requests

from utils.id_name_converter import IdNameConverter
from utils.async_scraper import AsyncScraper
from utils import arbitrage

orbs_to_scrape = []

default_scrape = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 15, 16]  # TODO: Store this locally and allow users to set


def menu():
    global user_league
    global orbs_to_scrape
    page_content = requests.get('http://currency.poe.trade').content
    page = IdNameConverter(page_content)

    print('''
.-,--.     .  .                 ,.       .     .                  
 '|__/ ,-. |- |-.   ,-. ,"     / |   ,-. |-. . |- ,-. ,-. ,-. ,-. 
 ,|    ,-| |  | |   | | |-    /~~|-. |   | | | |  |   ,-| | | |-' 
 `'    `-^ `' ' '   `-' |   ,'   `-' '   ^-' ' `' '   `-^ `-| `-' 
                        '                                  ,|     
                                                          `'          
    ''')

    print('Hello! This is a currency scraper for Path of Exile. Currently it supports finding arbitrage '
          'opportunities on the currency.poe.trade website.\n')

    print('Some initial setup...')
    user_league = input('Enter which league you are playing in: ').title().strip()
    set_orbs_to_scrape(page)

    print('Please select one of the following options:')

    while True:
        print('''
        1. Find arbitrage! 
        2. Set orb comparison list.
        3. Display current orb comparison list.
        4. Exit.
        ''')

        choice = input().strip()

        if choice == '1':
            if len(orbs_to_scrape) <= 1:
                print('Computing arbitrage requires more than one orb!')
            else:
                print('Scraping the following pages:')
                compute_arbitrage(page.id_to_name, orbs_to_scrape)
        elif choice == '2':
            set_orbs_to_scrape(page)
            continue
        elif choice == '3':
            print(display_current_orb_list(page.id_to_name, orbs_to_scrape))
        elif choice == '4':
            print('Exiting...')
            break


def compute_arbitrage(pg, orbs_list):
    g = AsyncScraper(user_league, orbs_to_scrape).scrape_all_pages()
    start_currency_amount = int(input('How much currency are you trading? ').strip())

    for orb in orbs_list:
        print(f'{pg.get(int(orb))} ID: {orb}')

    start_currency_ID = int(input('Enter the ID of the currency you are trading ').strip())

    trade_depth = int(input('How many trades do you want to make? ').strip())
    arb = arbitrage.find_max(g, start_currency_amount, start_currency_ID, trade_depth)

    print('Highest return arbitrage:')

    for trade in arb:
        print()
        print(f'Trade {trade[0]:.2f} {pg.get(trade[1])}s for {trade[3]:.2f} {pg.get(trade[2])}s')

def set_orbs_to_scrape(page_data):
    global orbs_to_scrape
    orbs_to_scrape.clear()
    available_orbs = page_data.url_numbers

    for key, val in page_data.name_to_id.items():
        print(f'{key} : {val}')

    print('Enter the orb IDs you would like to scrape (separated by spaces)')

    user_input = input('input: ').strip().split(' ')
    scrubbed_input = [int(orb) for orb in user_input if int(orb) in available_orbs]
    orbs_to_scrape.extend(scrubbed_input)
    print('User list saved!')


def display_current_orb_list(page_data, orbs_list):
    print(f'You are currently ready to compute arbitrage between the following orbs: ')
    user_list = [page_data.get(int(orb)) for orb in orbs_list]
    return user_list


if __name__ == '__main__':
    menu()

