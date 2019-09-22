from typing import Dict

from pages.all_orb_page import OrbPage


class IdNameConverter:

    """
        This class takes an Bs4 object (requests.get('x').content as a parent and provides two dictionaries.
        Each league new orbs are introduced, so we need to populate lookup dictionaries dynamically.
    """

    def __init__(self, parent):
        self.parent = OrbPage(parent)
        self.name_to_id_dict = {}
        self.id_to_name_dict = {}

    def __repr__(self):
        print(type(self.parent))

    @property
    def id_to_name(self) -> Dict[int, str]:
        for orb in self.parent.orbs:
            self.id_to_name_dict[int(orb.id)] = orb.name
        return self.id_to_name_dict

    @property
    def name_to_id(self) -> Dict[str, int]:
        for orb in self.parent.orbs:
            self.name_to_id_dict[orb.name] = int(orb.id)
        return self.name_to_id_dict

    @property
    def url_numbers(self):
        return list(self.id_to_name.keys())
