from locators.all_orb_data import AllOrbData

class AvailableOrbParser:
    """
    This file is to scrape the main currency.poe.trade page and find which orbs are available for trading.
    It provides the name and data-id for each orb.
    """
    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        return f'{self.name} : {self.id}'

    @property
    def name(self) -> str:
        return self.parent.attrs[AllOrbData.ORB_TITLE]

    @property
    def id(self) -> str:
        return self.parent.attrs[AllOrbData.ORB_ID]

    @property
    def make_dict(self) -> {str, str}:
        return {self.name: self.id}

