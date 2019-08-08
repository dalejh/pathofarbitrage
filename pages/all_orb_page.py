from bs4 import BeautifulSoup

from locators.all_currency_page import AllCurrencyPageLocator
from parsers.available_orbs_parser import AvailableOrbParser


class OrbPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def orbs(self):
        return [AvailableOrbParser(e) for e in self.soup.select(AllCurrencyPageLocator.ORB_DIRECTORY)]


