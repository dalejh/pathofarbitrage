from locators.transaction_details import TransactionDetails as TD


class OrbTransactionParser:

    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        return f'user {self.parent.attrs[TD.USERNAME]} is selling {self.parent.attrs[TD.WANT_AMOUNT]} orbs of' \
            f'ID:{self.parent.attrs[TD.WANT_CURRENCY]} for {self.parent.attrs[TD.HAVE_AMOUNT]} ' \
            f'orbs of ID:{self.parent.attrs[TD.HAVE_CURRENCY]}'

