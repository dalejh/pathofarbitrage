from bs4 import BeautifulSoup

from locators.transaction_page import TransactionPageLocator
from parsers.orb_transaction_parser import OrbTransactionParser


class TransactionPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def transactions(self):
        return [OrbTransactionParser(e) for e in self.soup.select(TransactionPageLocator.PAGE)]


