import typing

from locators.transaction_details import TransactionDetails as td


class OrbTransactionParser:

    """
    "This class is used to parse each listing on the page after we've selected which orbs we're looking for.
    Example page: http://currency.poe.trade/search?league=Blight&online=x&stock=&want=4&have=6
    """

    def __init__(self, parent):
        self.parent = parent
        self.username = parent.attrs[td.USERNAME]
        self.want_amount = parent.attrs[td.WANT_AMOUNT]
        self.want_id = parent.attrs[td.WANT_ID]
        self.have_amount = parent.attrs[td.HAVE_AMOUNT]
        self.have_id = parent.attrs[td.HAVE_ID]

    def __repr__(self):
        return f'user {self.username} is selling {self.want_amount} orbs of' \
            f'ID:{self.want_id} for {self.have_amount} ' \
            f'orbs of ID:{self.have_id}'

    @property
    def price_ratio(self) -> float:
        return float(self.want_amount)/float(self.have_amount)

    @property
    def want(self):
        return self.want_id

    @property
    def have(self):
        return self.have_id

