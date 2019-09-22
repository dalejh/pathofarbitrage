import numpy as np
from bs4 import BeautifulSoup
from typing import List, Union
# import logging

from locators.transaction_page import TransactionPageLocator
from parsers.orb_transaction_parser import OrbTransactionParser

# logging.basicConfig(format='%(message)s',
#                     level=logging.INFO,
#                     filename='fraud_logs.txt')
# logger = logging.getLogger('fraud_logger')


class TransactionPage:

    """
    This page calls beautiful soup to parse the individual page that is passed to it from our async scraper.
    There is also some data cleaning done in this class, and finally the start_end_weight function is used to
    feed our arbitrage computation
    """

    def __init__(self, page, outlier_constant=3, num_orbs_returned=5): # todo: more rigorous test as to whether these default values are optimal
        self.soup = BeautifulSoup(page, 'html.parser')
        self.outlier_const = outlier_constant
        self.num_orbs_returned = num_orbs_returned
        self.parser = [OrbTransactionParser(e) for e in self.soup.select(TransactionPageLocator.PAGE)]

    @property  # to see all transactions listed
    def transactions(self) -> List[OrbTransactionParser]:
        return self.parser

    # grab price ratio property for each transaction listed on currency.poe.trade for a
    # specific orb->orb trade (e.g. chaos to exalted orbs) and then return filtered list.
    def scrubbed_transactions(self) -> List[float]:
        raw_orbs = [orb.price_ratio for orb in self.parser]
        scrubbed_orbs = self._remove_fraud(raw_orbs)
        return scrubbed_orbs[:self.num_orbs_returned]

    # use inter quartile range to filter fraudulent outliers
    def _remove_fraud(self, raw_orbs) -> List[float]:
        raw_orbs = np.array(raw_orbs)
        upper_quartile = np.percentile(raw_orbs, 75)
        lower_quartile = np.percentile(raw_orbs, 25)
        iqr = (upper_quartile - lower_quartile) * self.outlier_const
        quartile_set = (lower_quartile - iqr, upper_quartile + iqr)
        scrubbed_orbs = []
        for orb_value in raw_orbs.tolist():
            if quartile_set[0] <= orb_value <= quartile_set[1]:
                scrubbed_orbs.append(orb_value)
            # else:  # TODO: Remove this or add file/debug logging to show filtered values
        return scrubbed_orbs

    # returns a list of 'have' orb ID, 'want' orb ID, and the average price of top 5 filtered transactions
    @property
    def start_end_weight(self) -> List[Union[int, float]]:
        ret = [0, 0, 0]
        if len(self.parser):
            ret = [int(self.parser[0].have), int(self.parser[0].want),
                   float(sum(self.scrubbed_transactions())/self.num_orbs_returned)]
        return ret

